# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 13:25:54 2019

*args

source = 'source name', startID = int(optional)

if no int is given, id's will start at 001
example: {'WebSource_001': ['feces', 'comes with the other hole']}

parse_html module searches for patterns of:
    <tag>word or words (2-3)</tag>
    <tag>paragraph</tag>

and returns a dictionary of:
    {'Source_UniqueID': ['frontface', 'backface']}
    

TODO:
    Separate gen function and parser
    Refactor and check is passing too much
    Add API interface specification

@author: vince
"""


import re
from bs4 import BeautifulSoup
from collections import namedtuple

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pmpstudy.settings')

import django
django.setup()

def searchDataType(**kwargs):
    dataInfo = kwargs
    dataFile = dataInfo['data']
    
    # read a line of input to assess type
    
    #html
    pattern = '<*>'
    rep = re.compile(pattern)
    if rep.search(dataFile):
        return {'type': 'html', 'file': dataFile}
    

def validateData(terms, descriptions):
    return len(terms) == len(descriptions)


def packData(**kwargs):
    
    terms = kwargs['terms']
    descriptions = kwargs['descriptions']
    source = kwargs['source']
    
    packed_data = {}
    for i in range(len(terms)):
        uid = '{0}_{1:03d}'.format(source, i)
        packed_data[uid] = [terms[i],descriptions[i]]
    return packed_data

def cleanTags(instring):
    replace_set = ["b'", "<p>", "</p>", "<em>", "</em>"]
    
    for pattern in replace_set:
        instring = instring.replace(pattern, '')
        
    return instring

def addCards():
    pass


if __name__ == "__main__":
    
    raw = open("Lexicon_Raw_HTML.html", "r") 
    firstLine = raw.readline()
    
    if searchDataType(data=firstLine)['type'] == 'html':
        soup = BeautifulSoup(firstLine, features='html.parser')
        
        ## Look for term and description tags
        if soup.dd:
            terms = soup.find_all('dt')
            descriptions = soup.find_all('dd')
            
            terms_cleaned = []
            for term in terms:
                if not term('a'):
                    terms_cleaned.append(term.string)
            
            descriptions_cleaned = []
            for description in descriptions:
                if not description.string:
                    for child in description.children:
                        descriptions_cleaned.append(cleanTags(str(child.encode('utf-8'))))
                else:
                    descriptions_cleaned.append(description.string)
                

    if validateData(terms_cleaned, descriptions_cleaned):
        print('Data validated')
    
    print(packData(terms=terms_cleaned, descriptions=descriptions_cleaned, source='PMP_Lexicon'))
    
    raw.close()
    