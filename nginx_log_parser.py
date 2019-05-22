#!/usr/bin/env python3
'''This script takes one argument, the filepath to the nginx access log to be
parsed, and returns a list of how many of each status code is found per second'''
import re
from sys import argv


def new_item(dateandtime, statuscode, listname):
    '''Adds a new tuple to the list
    Args:
    dateandtime (string): the datetime stamp
    statuscode (string): the HTTP status code
    listname (list): the list containing the tuples
    '''
    if status[:1] == '2':
        list.append((time, {'2xx': 1, '3xx': 0, '4xx': 0}))
    elif status[:1] == '3':
        list.append((time, {'2xx': 0, '3xx': 1, '4xx': 0}))
    elif status[:1] == '4':
        list.append((time, {'2xx': 0, '3xx': 0, '4xx': 1}))

def increment(dateandtime, statuscode, listname):
    '''Updates the count of the status codes in the list
    Args:
    dateandtime (string): the datetime stamp
    statuscode (string): the HTTP status code
    listname (list): the list containing the tuples
    '''
    if time in item:
        if status[:1] == '2':
            item[1]['2xx'] = item[1]['2xx'] + 1
        elif status[:1] == '3':
            item[1]['3xx'] = item[1]['3xx'] + 1
        elif status[:1] == '4':
            item[1]['4xx'] = item[1]['4xx'] + 1


if __name__ == "__main__":
    lineformat = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)
    list = []

    with open(argv[1], 'r') as file:
        for line in file.readlines():
            try:
                # Use regex to put all fields into dict and pull date and status
                result = re.search(lineformat, line)
                result_dict = result.groupdict()
                time = result_dict["dateandtime"]
                status = result_dict["statuscode"]
            except AttributeError:
                pass
            # If list is empty, add first tuple to list
            if list == []:
                new_item(time, status, list)
            # If list is not empty...
            elif list != []:
                for item in list:
                    flag = False
                    # If timestamp exists in list, +1 appropriate status code
                    if time in item:
                        increment(time, status, list)
                        flag = True
                # If flag is false, timestamp was not found, so add new time to list
                if flag is False:
                    new_item(time, status, list)
                  
    for item in list:
        print("{} >>  2xx: {} req/s  3xx: {} req/s  4xx: {} req/s".format(item[0], item[1]['2xx'], item[1]['3xx'], item[1]['4xx']))