# -*- coding: utf-8 -*-
"""
Created on Sat Nov 05 16:02:37 2016

@author: Rapssail
"""

from __future__ import unicode_literals

import requests
import json
import time
import codecs
import cPickle as pickle
import sys
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

API_KEY= "4c51686f384217641220306d2e721970"
members = []
members_id = []


def fetch_groups():
    groups = []
    
    # Get your key here https://secure.meetup.com/meetup_api/key/
    per_page = 200
    results_we_got = per_page
    offset = 0
    while (results_we_got == per_page):
        # Meetup.com documentation here: http://www.meetup.com/meetup_api/docs/2/groups/
        call = 'groups'        
        response=get_results(call, {"sign":"true", "zip":"33130", "radius": 15, "key":API_KEY, "page":per_page, "offset":offset })
        time.sleep(1)
        offset += 1
        results_we_got = response['meta']['count']
        for result in response['results']:
            group = {}
            group['id'] = result['id']
            group['name'] = result['name']            
            group['link'] = result['link']
            group['member_count'] = result['members']
            groups.append(group)
        print groups
        pickle.dump( groups, open( "Miami_meetup_groups.p", "wb" ) )
    time.sleep(1)

def fetch_members(group_id):
    global members
    global members_id
    # Get your key here https://secure.meetup.com/meetup_api/key/
    per_page = 200
    results_we_got = per_page
    offset = 0
    while (results_we_got == per_page):
        # Meetup.com documentation here: http://www.meetup.com/meetup_api/docs/2/members/
        call = 'members'        
        response=get_results(call, {"sign":"true", "group_id": group_id, "key":API_KEY, "page":per_page, "offset":offset })
        time.sleep(1)
        offset += 1
        results_we_got = response['meta']['count']
        for result in response['results']:
            member = {}
            member['id'] = result['id']
            if member['id'] not in members_id:
                if result['status'] != "prereg":                
                    if 'name' in result:                
                        member['name'] = result['name']
                    else:
                        member['name'] = 'unspecified'
                    member['topics'] = result['topics']
                    member['city'] = result['city']
                    member['link'] = result['link']
                    members.append(member)
                    members_id.append(member['id'])
                else:
                    print "User is not fully registered"                    
                    pass
        pickle.dump( members, open( "Miami_meetup_members.p", "wb" ) )
        
        print "%d members fetched" % len(members_id)
        
    time.sleep(1)

def get_groups():
    with open('Miami_meetup_groups.p', 'r') as p:
        groups = pickle.load(p)    
    print "%d groups found" % len(groups)    
    return groups
    
def get_results(call, params):

    request = requests.get("http://api.meetup.com/2/" + call, params=params)
    data = request.json()
	
    return data

def load_meetup_members():
    members_data = pickle.load(open( "Miami_meetup_members_save.p", "rb" ) )     
    return members_data
    
def main():  
    groups = get_groups()
#    for g in groups:
#        fetch_members(g['id'])
#        print "total number of members: %d" % len(members)
    
if __name__=="__main__":
        main()


## Run this script and send it into a csv:
## python meetup-pages-names-dates.py > meetup_groups.csv