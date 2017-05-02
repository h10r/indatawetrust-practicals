#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os.path
import json
import requests
import pickle
from unidecode import unidecode
from nltk.tokenize import sent_tokenize

# get a key at https://developer.gavagai.se/
GAVAGAI_API_KEY = "YOUR_KEY"

TEXT_LANGUAGE = "EN"
MINIMUM_LINE_LENGTH = 20

GAVAGAI_BASE_URL = "https://api.gavagai.se/v3"
GAVAGAI_TONALITY_ENDPOINT = GAVAGAI_BASE_URL + "/tonality"
GAVAGAI_TONALITY_ENDPOINT += "?apiKey=" + GAVAGAI_API_KEY

if len( sys.argv ) != 2:
    print "* Error: Not enough arguments"
    sys.exit(1)

def process_file_with_gavagai( filename ):   
    # prepare request
    headers = {'content-type': 'application/json'}

    req_params = {}
    req_params["language"] = TEXT_LANGUAGE
    req_params["texts"] = []

    # load file
    lines = sent_tokenize( unidecode( str( open( filename ).read() ) ) )

    used_lines = []

    for i,line in enumerate( lines ):
        if len( line ) > MINIMUM_LINE_LENGTH:
            req_params["texts"].append( { "id" : i, "body" : line.strip() } )
            used_lines.append( unidecode( line.strip() ) )

    r = requests.post(GAVAGAI_TONALITY_ENDPOINT, data=json.dumps(req_params), headers=headers)

    pickle.dump( [r, used_lines], open( filename + ".response", "wb" ) )
    
    return [r, used_lines]

file_path = sys.argv[1]

if os.path.isfile( file_path + ".response" ):
	r, used_lines = pickle.load( open( file_path + ".response", "rb" ) )
else:
	r, used_lines = process_file_with_gavagai( file_path )

j = json.loads(r.text)

for i,line in enumerate( j["texts"] ):
	scores = line["tonality"]
	print i,
	print ",",
	for t in scores:
		print t["tone"],
		print ",",
		print t["score"],
		print ",",
	print used_lines[i],
	print
