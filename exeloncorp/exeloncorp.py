import requests
import sys
import pandas as pd
import csv
import os
from threading import Thread
from queue import Queue
import datetime as datetime
#from account.models import ScrapingLog
from django.utils import timezone

queue = Queue(150)
dict_list = []
counter = 1


def to_string(s):
    """

    :param s:
    :return:
    """
    print('inside to_string....')
    try:
        print('inside try.printing str(s)..')
        print(str(s))
        return str(s)
        
    except:
        print('inside except.printing s.encode..')
        print(s.encode('utf-8'))
        # Change the encoding type if needed
        return s.encode('utf-8')

def travel_element_json(row_dict, key, value):
    """

    :param row_dict:
    :param key:
    :param value:
    :return:
    """
    print('inside travel_element_json()... ')
    # Reduction Condition 1
    if type(value) is list:
        print('inside reduction condition1...i.e type(value) is list...')
        # i=0
        for sub_item in value:
            print('inside reduction condition 1 calling travel_element_json() function itself...')
            travel_element_json(row_dict, key, sub_item)
    # Reduction Condition 2
    elif type(value) is dict:
        print('inside reduction condition2...i.e if type(value) is dict...')
        sub_keys = value.keys()
        print('checking sub_keys:')
        print(sub_keys)
        for sub_key in sub_keys:  
            print('inside for loop...')          
            if(sub_key!='talemetry_job_id' and sub_key!='permalink' and sub_key!='region_abbr' and sub_key!='phone' and sub_key!='email' and sub_key!='extra' and sub_key!='name'):
                print('inside reduction condition 2 , inside if() calling .... travel_element_json() function itself.... ')
                travel_element_json(row_dict, sub_key, value[sub_key])
                # travel_element_json(row_dict, key + '##' + to_string(sub_key), value[sub_key])

    # Base Condition
    else:
        print('inside base condition.......')
        if key not in row_dict.keys():
            print('inside base condition if not in row_dict.keys()....')
            row_dict[to_string(key)] = to_string(value)
            print(row_dict[to_string(key)])

        else:
            print('inside base condition else ')
            row_dict[to_string(key)] = row_dict[to_string(key)] + '||' + value
            print(row_dict[to_string(key)])

    print('return of json_travel_element'), print(row_dict)
    return row_dict



def parse_from_root(each_item, total_element, input_file_type, element):
    """

    :param each_item:
    :param total_element:
    :return:
    """
    print('inside parse_from_root()..........')
    row_dict = {}
    print('printing row_dict of parse_from_root:'), print(row_dict)
    global dict_list, counter
    if input_file_type == 'json':
        print('printing inside if of parse_from_root')
        print('calling travel_element_json() from if inside parse_from_root..')
        row_dict = travel_element_json(row_dict, element, each_item)
        print('printing row_dict inside if of parse_from_root:'),print(row_dict)

    print(">>>  Progress:  {} %   ".format(int((counter/total_element)*100)), end='\r')
    sys.stdout.flush()
    counter += 1
    dict_list.append(row_dict)
    print('printing dict_list inside of parse_from_root: ')
    print(dict_list)

class ProducerThread(Thread):

    print('inside ProducerThread class.................')

    def __init__(self, element_list):
        """

        :param element_list:
        """
        super(ProducerThread, self).__init__()
        self.element_list = element_list
        print('inside Producer thread __init__()'),print(element_list)

    def run(self):
        """

        :return:
        """
        global queue
        print('inside producer thread run()')
        while self.element_list:
            each_item = self.element_list.pop()
            print('printing each_item of while loop in producer thread'),print(each_item), print('putting each_item in queue:')
            queue.put(each_item)
            print(queue)


class ConsumerThread(Thread):

    print('inside ConsumerThread class..................')

    def __init__(self, total_element, input_file_type, element):
        """

        :param total_element:
        """
        super(ConsumerThread, self).__init__()
        self.total_element = total_element
        self.input_file_type = input_file_type
        self.element = element
        print('inside ConsumerThread __init__ (): ', total_element,input_file_type,element)

    def run(self):
        """

        :return:
        """
        global queue
        print('inside ConsumerThread run()')
        while not queue.empty():
            each_item = queue.get()
            print('printing each_item of while loop in consumer thread run()'),print(each_item), print('calling parse_from_root() from while loop in consumer thread run()...')
            parse_from_root(each_item, self.total_element, self.input_file_type, self.element)
            queue.task_done()

def parseJson(data):
    print('inside parseJason()......')
    element_list = data['entries']
    print('.............element_list................start'),print(element_list),print('.............element_list................end')
    print('total_element : ')
    total_element = len(element_list)
    print(total_element)

    p1 = ProducerThread(element_list)
    print('1 p1, p1 is a ProducerThread instance taking all element_list:  '), print(p1), print('So, producer thread creates only one producer \
        thread by taking all element_list i.e 1 producer thread = all element_list')
    producer_thread_list = list()
    print('2 producer thread list: '), print(producer_thread_list)
    producer_thread_list.append(p1)
    print('3 producer thread list with appended p1:  '), print(producer_thread_list)
    print('calling COnsumerThread().....')
    consumer_thread_list = [ConsumerThread(total_element, 'json', 'entries') for x in range(10)]
    print('4 consumer thread list after calling ConsumerThread class '), print(consumer_thread_list)
    print('..........................................................producer thread list................................................................... start !!!') 
    for each_producer in producer_thread_list:
        print('each_producer before start in main function: ', each_producer)
        each_producer.start()
        print('each_producer after start in main function: ', each_producer), print('each_producer after start in main function ends')
    print('..........................................................producer thread list.......................................................................end!!! ')
    print('...........................................................consumer thread list .................................................................. start !!!')     
    for each_consumer in consumer_thread_list:
        print('each_consumer before start in main function: ', each_consumer), print(each_consumer)
        each_consumer.start()
        print('each_consumer after start in main function'), print(each_consumer), print('each_consumer after start in main function ends')
    print('...........................................................consumer thread list .....................................................................end!!!')
    print('.......................................................producer thread list for join..............................................................start!!! ') 
    for each_producer in producer_thread_list:
        print('each_producer before join in main function'), print(each_producer)
        each_producer.join()
        print('each_producer after join in main function'), print(each_producer), print('each_producer after join in main function ends')
    print('.......................................................producer thread list for join.................................................................end!!! ') 
    print('........................................................consumer thread list for join..............................................................start!!! ')
    for each_consumer in consumer_thread_list:
        print('each_consumer before join in main function'), print(each_consumer)
        each_consumer.join()
    print('each_consumer after join in main function '), print(each_consumer), print('each_consumer after join in main function ends')
    print('........................................................consumer thread list for join................................................................end!!! ')
    main_df = pd.DataFrame(dict_list)
    totalDistList = len(dict_list)
    return main_df,totalDistList


def exeloncorp_start(current_page =1,perpage=2):
    startTime = datetime.datetime.now()
    url = 'https://jobs.exeloncorp.com/search/jobs.json?current_page='+ str(current_page)+'&per_page='+str(perpage)
    resp = requests.get(url=url)
    data = resp.json()
    print('.......calling parseJason().........') 
    main_df,totalDistList =parseJson(data=data)
    finalTime = datetime.datetime.now()
    time_taken_minutes = ((finalTime - startTime).seconds) / 60
    #ScrapingLog(source='ExelonCorp',
    #    time_taken_minutes=time_taken_minutes,
    #    rows_affected=totalDistList,
    #    scrap_date=timezone.now(),
    #    status=True).save()
    
    #main_df.to_csv('exeloncorp.csv',index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')

exeloncorp_start(current_page =1,perpage=2)
    