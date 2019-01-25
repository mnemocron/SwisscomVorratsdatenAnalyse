#!/usr/bin/python
#_*_ coding: utf-8 _*_

"""
@file           GoogleTakeoutConverter.py
@author         Simon Burkhardt - simonmartin.ch
@date           2018
@version        
@brief          Konvertiert die Vorratsdaten im JSON Format auf das Location History Format von Google
@details        Verschiedene Tools können die Google Location History importieren und beispielsweise eine Heatmap erzeugen
"""

try:
    import time
    import datetime
    import optparse
    import json
    import os
except Exception, ex:
	print str(ex)

parser = optparse.OptionParser('Google Takeout Converter')
parser.add_option('-i', '--input-file',     dest='infile',   type='string',  help='specify the source file.csv')
parser.add_option('-o', '--optut-file',     dest='outfile',  type='string',  help='[optional] specify the output file.json')

(opts, args) = parser.parse_args()

if ( opts.infile is None or opts.outfile is None):
    parser.print_help() 
    exit(0)

json_data = {}
json_data['locations'] = []

index = 0

try:
    with open(opts.infile, 'r') as infile:
        json_in = json.load(infile)
        index = 0
        for location in json_in['dat']:
            timestamp = location['timestamp']
            timestampMs = str(timestamp).split('.')[0] + '000'
            if('geometry' in location['location']):
                json_data['locations'].append({})
                json_data['locations'][index]['timestampMs'] = timestampMs
                # json_data['locations'][index]['latitudeE7']  = int(location['location']['results'][0]['geometry']['location']['lat']*pow(10, 7))
                # json_data['locations'][index]['longitudeE7'] = int(location['location']['results'][0]['geometry']['location']['lng']*pow(10, 7))
                json_data['locations'][index]['latitudeE7']  = int(location['location']['geometry']['lat']*pow(10, 7))
                json_data['locations'][index]['longitudeE7'] = int(location['location']['geometry']['lng']*pow(10, 7))
                index += 1



#    print json.dumps(json_data, indent=4, sort_keys=True)

    with open(opts.outfile, 'w') as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=True)

except KeyboardInterrupt, e:
    exit(0)


