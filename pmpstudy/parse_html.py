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
from flashcard.models import FlashCard
from django.contrib.auth.models import User


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

def addCards(cardDict, **kwargs):
    '''
    Takes card dictionary of form {titlekey}:[frontface,backface] and creates objects for addition to DB.

    Must pass argument mode = dry-run or commit
    '''
    add_list = []
    Card = namedtuple('Card', ['title', 'frontface', 'backface', 'activated', 'owner'])
    
    ##common to all cards
    owner = User.objects.get(username='demouser')
    activated = True
    #pull the rest and assign
    for cardkey in cardDict.keys():
        card_info = Card(
            title = cardkey,
            frontface = cardDict[cardkey][0],
            backface = cardDict[cardkey][1],
            owner = owner,
            activated = activated
        )
        add_list.append(card_info)

    runType = kwargs
    if runType['mode'] == 'dry-run':
        print('Executing dry-run.  Examples:')
        for i in range(3):
            print(add_list[i])
        print('Total of {} cards to be added'.format(len(add_list)))
        
    elif runType['mode'] == 'commit':
        for card in add_list:
            new_card = FlashCard(
                title = card.title,
                frontface = card.frontface,
                backface = card.backface,
                activated = activated,
                owner = owner
            )
            new_card.save()
        print('Committing Changes')

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
    
    new_cards = packData(terms=terms_cleaned, descriptions=descriptions_cleaned, source='PMP_Lexicon')
    addCards(new_cards, mode='dry-run')
    
    raw.close()
    