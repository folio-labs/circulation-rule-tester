#! /bin/python3 

"""
Declare modules that are needed for the script.
"""

import requests
import csv
import sys
from datetime import datetime
import ../../folioFunctions as ff
import configparser
import argparse

"""
Use configparser to open config-template.ini and read in
applicable configuration values to use with all of the requesting calls.
"""

envConfig = configparser.ConfigParser()
envConfig.read('config-template.ini')

"""
Next, we call a function to check the script command to find out
what server we are testing on, and what the filename is for our test
file.
"""

parser = argparse.ArgumentParser()
parser.add_argument('servername', type=str)
parser.add_argument('filename', type=str)
argsServer = parser.parse_args()
whichServer = argsServer.servername
inputFilename = argsServer.filename

"""
Now we know which server, so we can pull the relevant values from config-template.ini.
"""

testServer = envConfig[whichServer]['okapi_url']

fetchHeaders = {
    'x-okapi-tenant': envConfig[whichServer]['tenant_id'],
    'x-okapi-token': envConfig[whichServer]['password']
}
postHeaders = {
    'x-okapi-tenant': envConfig[whichServer]['tenant_id'],
    'x-okapi-token': envConfig[whichServer]['password'],
    'Content-Type': 'application/json'
}


"""
Next, we capture the start time of the script and print it on screen. 
We will also use the start time as part of the filename for the
output file; this can be helpful when running this script a lot
in a short amount of time.
"""

# Print start time for script - 
startTime = datetime.now()
print("Script starting at: %s" % startTime)

# fetch settings files to help generate the output; makes things faster

# fetch patron groups
patronGroupsJson = ff.fetchpatrongroups(testServer, fetchHeaders)

# fetch loan types
loanTypesJson = ff.fetchloantypes(testServer, fetchHeaders)

# fetch material types
materialTypesJson = ff.fetchmaterialtypes(testServer, fetchHeaders)

# fetch locations
locationsJson = ff.fetchlocations(testServer, fetchHeaders)

# fetch libraries
librariesJson = ff.fetchlibraries(testServer, fetchHeaders)

# fetch loan policies
loanPoliciesJson = ff.fetchloanpolicies(testServer, fetchHeaders)

# fetch notice policies
noticePoliciesJson = ff.fetchnoticepolicies(testServer, fetchHeaders)

# fetch request policies
requestPoliciesJson = ff.fetchrequestpolicies(testServer, fetchHeaders)

# fetch overdue policies
overduePoliciesJson = ff.fetchoverduepolicies(testServer, fetchHeaders)

# fetch lost item policies
lostItemPoliciesJson = ff.fetchlostpolicies(testServer, fetchHeaders)

"""
Open the file with your loan testing information (name 'loan_tester.csv' by default) and
then load it into a python CSV Dictionary object called "testLoanScenarios."

The encoding = 'utf-8-sig' tells Python to compensate for Excel encoding when parsing
the CSV.
"""

initialFile = open(inputFilename, newline='', encoding='utf-8-sig')
testLoanScenarios = csv.DictReader(initialFile, dialect='excel')

"""
Next, you create a Python dictionary called "friendlyResults" where the test loop code
will store the results. At the end, this object will be spit out into your
CSV file output.
"""

friendlyResults = {}

"""
Finally, the actual script that runs through your scenarios.
"""


for count, row in enumerate(testLoanScenarios):
    # provides a simple counter and output on the screen to know the script is still running
    print(count, row)
    
    # first thing is to pull the row from testLoanScenarios, and assign the UUID values to
    # the associated variables.
    patron_type_id, loan_type_id, item_type_id, location_id = row["patron_type_id"], row["loan_type_id"],  row["item_type_id"], row["location_id"]

    # then, you're going to take each value, pull the human readable name, and put
    # it into "friendlyResults" to make the output easier to read.

    # pull patron_type_id friendly name
    for i in patronGroupsJson['usergroups']:
        if i['id'] == patron_type_id:
            friendlyResults['patron_group'] = i['group']
    if not 'patron_group' in friendlyResults:
        friendlyResults['patron_group'] = "Patron group not found"
    # pull loan type friendly name
    for i in loanTypesJson['loantypes']:
        if i['id'] == loan_type_id:
            friendlyResults['loan_type'] = i['name']
    if not 'loan_type' in friendlyResults:
        friendlyResults['loan_type'] = "Loan type not found"
    

    # pull material type friendly name (remember, the API calls it 'item_type') 
    for i in materialTypesJson['mtypes']:
        if i['id'] == item_type_id:
            friendlyResults['material_type'] = i['name']
    if not 'material_type' in friendlyResults:
        friendlyResults['material_type'] = "Material type not found"

    # Pull location code - this reduces the odds of running into a 
    # comma in the location name which can break the CSV file.
    # We also add the library name, to make the output file easier to sort and filter.
    
    for i in locationsJson['locations']:
        if i['id'] == location_id: # once you find the location ....
            for j in librariesJson['loclibs']: # use the location to search your stored copy of the libraries Json
                if i['libraryId'] == j['id']: # to find the associated library
                    friendlyResults['library_name'] = j['name'] # and pull the name
            friendlyResults['location'] = i['code'] # finally, add the location code so that it shows up in that order in the output file.
    if not 'library_name' in friendlyResults:
        friendlyResults['libraryName'], friendlyResults['location'] = "Library not found", "Location not found"
    if not 'location' in friendlyResults:
        friendlyResults['location'] = "Location not found"

    # now, you'll use the UUID values to query the APIs, get the results back, and then form
    # the full row in friendlyResults with the friendly names
    
    # first, let's create the URLs for asking for each policy.
    
    urlLoanPolicy = '{}{}{}{}{}{}{}{}{}{}'.format(testServer, '/circulation/rules/loan-policy?' , 'loan_type_id=', loan_type_id, '&item_type_id=', item_type_id, '&patron_type_id=', patron_type_id, '&location_id=', location_id)
    urlRequestPolicy = '{}{}{}{}{}{}{}{}{}{}'.format(testServer, '/circulation/rules/request-policy?' , 'loan_type_id=', loan_type_id, '&item_type_id=', item_type_id, '&patron_type_id=', patron_type_id, '&location_id=', location_id)
    urlNoticePolicy = '{}{}{}{}{}{}{}{}{}{}'.format(testServer, '/circulation/rules/notice-policy?' , 'loan_type_id=', loan_type_id, '&item_type_id=', item_type_id, '&patron_type_id=', patron_type_id, '&location_id=', location_id)
    urlOverduePolicy = '{}{}{}{}{}{}{}{}{}{}'.format(testServer, '/circulation/rules/overdue-fine-policy?' , 'loan_type_id=', loan_type_id, '&item_type_id=', item_type_id, '&patron_type_id=', patron_type_id, '&location_id=', location_id)
    urlLostItemPolicy = '{}{}{}{}{}{}{}{}{}{}'.format(testServer, '/circulation/rules/lost-item-policy?' , 'loan_type_id=', loan_type_id, '&item_type_id=', item_type_id, '&patron_type_id=', patron_type_id, '&location_id=', location_id)

    # now, send a GET request to each URL - the return value will be the UUID for the circulation policy
    # that would be applied.
    # 
    # You could make one giant loop for this, but it seemed like I got a bit of a performance improvement by
    # doing individual loops through the smaller chunks of data / discrete sections.

    postLoanPolicies = requests.get(urlLoanPolicy, headers=postHeaders)
    postLoanPoliciesJson = postLoanPolicies.json()
    for i in loanPoliciesJson['loanPolicies']:
        if i['id'] == postLoanPoliciesJson['loanPolicyId']:
            friendlyResults['loanPolicy'] = i['name']

    postRequestPolicies = requests.get(urlRequestPolicy, headers=postHeaders)
    postRequestPoliciesJson = postRequestPolicies.json()
    for i in requestPoliciesJson['requestPolicies']:
        if i['id'] == postRequestPoliciesJson['requestPolicyId']:
            friendlyResults['requestPolicy'] = i['name']
    
    postNoticePolicies = requests.get(urlNoticePolicy, headers=postHeaders)
    postNoticePoliciesJson = postNoticePolicies.json()
    for i in noticePoliciesJson['patronNoticePolicies']:
        if i['id'] == postNoticePoliciesJson['noticePolicyId']:
            friendlyResults['noticePolicy'] = i['name']
            
    postOverduePolicies = requests.get(urlOverduePolicy, headers=postHeaders)
    postOverduePoliciesJson = postOverduePolicies.json()
    for i in overduePoliciesJson['overdueFinePolicies']:
        if i['id'] == postOverduePoliciesJson['overdueFinePolicyId']:
            friendlyResults['overduePolicy'] = i['name']
            
    postLostItemPolicies = requests.get(urlLostItemPolicy, headers=postHeaders)
    postLostItemPoliciesJson = postLostItemPolicies.json()
    for i in lostItemPoliciesJson['lostItemFeePolicies']:
        if i['id'] == postLostItemPoliciesJson['lostItemPolicyId']:
            friendlyResults['lostItemPolicy'] = i['name']

    # Finally, take the results and add them to the row in the file where we're capturing the results.
    # your output file will be saved as friendlyOutput-starttime.csv in your working directory.
    with open("friendlyOutput-%s.csv" % startTime.strftime("%d-%m-%Y-%H%M%S"), 'a', newline='') as output_file:
         test_file = csv.writer(output_file)
         test_file.writerow(friendlyResults.values())

# when the tester is finally done, give some basic time information so you 
# know how long it took        
endTime = datetime.now()
print("Script started at %s and ended at %s" % (startTime, endTime))

# close the initial file of scenarios
initialFile.close()
