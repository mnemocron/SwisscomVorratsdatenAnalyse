#!/usr/bin/python
#_*_ coding: utf-8 _*_

"""
@file           csv2json.py
@author         Simon Burkhardt - simonmartin.ch
@date           2018
@version        
@brief          
@details        -
"""

try:
    import time
    import datetime
    import urllib
    import urllib2
    import optparse
    import json
    import csv
    import os
    from bs4 import BeautifulSoup
    from pprint import pprint
except Exception, ex:
	print str(ex)

parser = optparse.OptionParser('csv2json')
parser.add_option('-i', '--input-file',     dest='infile',   type='string',  help='specify the source file.csv')
parser.add_option('-o', '--optut-file',     dest='outfile',  type='string',  help='[optional] specify the output file.json')
parser.add_option(      '--api-key',        dest='apikey',   type='string',  help='[optional] google maps api key')

(opts, args) = parser.parse_args()

if ( opts.infile is None or opts.outfile is None):
    parser.print_help() 
    exit(0)

'''
+41796069692, 10.54.226.78, P-GW, 28/03/2018 18:37:55, 32, 3594060816520107, Fraumünsterstr. 16 - Zürich - 8001, ? , ?

[0] phone number
[1] ip address
[2] (TYPE?)
[3] date/time
[4] (RSSI?)
[5] ?
[6] physical address
[7] ?
[8] ?

'''

addressDictionary = {}

json_data = {}
json_data['filename'] = opts.infile
json_data['dat'] = {}

index = 0

try:
    with open(opts.infile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            try:
                dat_phonenr  = row[0]
                dat_ipaddr   = row[1]
                dat_TYPE     = row[2]
                dat_datetime = row[3]
                dat_RSSI     = row[4]
                dat_UNKN1    = row[5]
                dat_physaddr = row[6]
                dat_UNKN2    = row[7]
                dat_UNKN3    = row[8]

                dat_timestamp = time.mktime(datetime.datetime.strptime(dat_datetime, '%d/%m/%Y %H:%M:%S').timetuple())
            except Exception, ex:
                print ex
            
            if (opts.apikey is not None):
                # getting the exact coordinates from Google maps
                # https://maps.google.com/maps/api/geocode/json?address=Fraum%C3%BCnsterstr.%2016%20-%20Z%C3%BCrich%20-%208001
                url = 'https://maps.google.com/maps/api/geocode/json?' + urllib.urlencode({'address' : dat_physaddr, 'key' : str(opts.apikey)})
            
                if (url in addressDictionary):
                    json_resp = addressDictionary[url]
                else:                
                    response = urllib2.urlopen(url).read()
                    json_resp = json.loads(response)
                    addressDictionary[url] = json_resp
                    # print json_resp
            else:
                json_resp = ''

            json_data['dat'][index] = {}
            json_data['dat'][index]['phone']     = dat_phonenr
            json_data['dat'][index]['ip']        = dat_ipaddr
            json_data['dat'][index]['type']      = dat_TYPE
            json_data['dat'][index]['datetime']  = dat_datetime
            json_data['dat'][index]['timestamp'] = dat_timestamp
            json_data['dat'][index]['rssi']      = dat_RSSI
            json_data['dat'][index]['unkn1']     = dat_UNKN1
            json_data['dat'][index]['address']   = dat_physaddr
            json_data['dat'][index]['location']  = json_resp
            json_data['dat'][index]['unkn2']     = dat_UNKN2
            json_data['dat'][index]['unkn3']     = dat_UNKN3
            index += 1

        csvfile.close()
#    print json.dumps(json_data, indent=4, sort_keys=True)

    with open(opts.outfile, 'w') as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=True)

except KeyboardInterrupt, e:
    exit(0)


