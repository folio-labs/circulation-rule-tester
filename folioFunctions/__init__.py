"""
Basic functions for working with Python and FOLIO

written by Erin Nettifee with assistance from Tod Olson and Aaron Neslin
in sharing code and learning Python

"""

import requests
import json
import sys

"""
Support checking whether a POST request errored out - 
if it did, one of the phrases below appears in the request
response, and we can use that to trigger trying a PUT request instead.
"""

error_phrases = ["errors", "ERROR", "duplicate key"]

"""
Next set of definitions - fetching settings files and returning the JSON.

This could be made more generalized, but for now, the API calls
are individually hard coded since we may want the limits to change depending on the values.
"""

def fetchpatrongroups(server, fetchheaders):
    patronGroupsUrl = '{}{}'.format(server, '/groups?limit=1000')
    patronGroupsRequest = requests.get(patronGroupsUrl, headers=fetchheaders)
    patronGroupsJson = patronGroupsRequest.json()
    return patronGroupsJson


def fetchloantypes(server, fetchHeaders):
    loanTypesUrl = '{}{}'.format(server, '/loan-types?limit=1000')
    loanTypesRequest = requests.get(loanTypesUrl, headers=fetchHeaders)
    loanTypesJson = loanTypesRequest.json()
    return loanTypesJson

def fetchmaterialtypes(server, fetchHeaders):
    materialTypesUrl = '{}{}'.format(server, '/material-types?limit=1000')
    materialTypesRequest = requests.get(materialTypesUrl, headers=fetchHeaders)
    materialTypesJson = materialTypesRequest.json()
    return materialTypesJson

def fetchlibraries(server, fetchHeaders):
    librariesUrl = '{}{}'.format(server, '/location-units/libraries?limit=100')
    librariesRequest = requests.get(librariesUrl, headers=fetchHeaders)
    librariesJson = librariesRequest.json()
    return librariesJson

def fetchlocations(server, fetchHeaders):
    locationsUrl = '{}{}'.format(server, '/locations?limit=1500')
    locationsRequest = requests.get(locationsUrl, headers=fetchHeaders)
    locationsJson = locationsRequest.json()
    return locationsJson

def fetchloanpolicies(server, fetchHeaders):
    loanPoliciesUrl = '{}{}'.format(server, '/loan-policy-storage/loan-policies?limit=500')
    loanPoliciesRequest = requests.get(loanPoliciesUrl, headers=fetchHeaders)
    loanPoliciesJson = loanPoliciesRequest.json()
    return loanPoliciesJson

def fetchnoticepolicies(server, fetchHeaders):
    noticePoliciesUrl = '{}{}'.format(server, '/patron-notice-policy-storage/patron-notice-policies?limit=100')
    noticePoliciesRequest = requests.get(noticePoliciesUrl, headers=fetchHeaders)
    noticePoliciesJson = noticePoliciesRequest.json()
    return noticePoliciesJson

def fetchrequestpolicies(server, fetchHeaders):
    requestPoliciesUrl = '{}{}'.format(server, '/request-policy-storage/request-policies?limit=50')
    requestPoliciesRequest = requests.get(requestPoliciesUrl, headers=fetchHeaders)
    requestPoliciesJson = requestPoliciesRequest.json()
    return requestPoliciesJson

def fetchoverduepolicies(server, fetchHeaders):
    overduePoliciesUrl = '{}{}'.format(server, '/overdue-fines-policies?limit=100')
    overduePoliciesRequest = requests.get(overduePoliciesUrl, headers=fetchHeaders)
    overduePoliciesJson = overduePoliciesRequest.json()
    return overduePoliciesJson

def fetchlostpolicies(server, fetchHeaders):
    lostItemPoliciesUrl = '{}{}'.format(server, '/lost-item-fees-policies?limit=100')
    lostItemPoliciesRequest = requests.get(lostItemPoliciesUrl, headers=fetchHeaders)
    lostItemPoliciesJson = lostItemPoliciesRequest.json()
    return lostItemPoliciesJson

"""
These functions take a setting UUID and add the friendly name to a file.

Could be more generalizable; work in progress.
"""

def fetchfriendlyusergroupname(id, patronGroupsJson, friendlyResults):
    for i in patronGroupsJson['usergroups']:
        if i['id'] == id:
            friendlyResults['patron_group'] = i['group']
    if not 'patron_group' in friendlyResults:
        friendlyResults['patron_group'] = "Patron group not found"


def fetchfriendlyloantypename(id, loanTypesJson, friendlyResults):
    for i in loanTypesJson['loantypes']:
        if i['id'] == id:
            friendlyResults['loan_type'] = i['name']
    if not 'loan_type' in friendlyResults:
        friendlyResults['loan_type'] = "Loan type not found"


def fetchfriendlymaterialtypename(id, materialTypesJson, friendlyResults):
    for i in materialTypesJson['mtypes']:
        if i['id'] == id:
            friendlyResults['material_type'] = i['name']
    if not 'material_type' in friendlyResults:
        friendlyResults['material_type'] = "Material type not found"


# # pull location friendly name - using location code since a lot of Duke location names have commas in them
# # which makes working with CSV a little too messy
# #
# # also pulling library friendly name so that it can be used in sorting/reviewing results in the
# # output file

def fetchlocationcode(id, locationsJson, librariesJson, friendlyResults):
    for i in locationsJson['locations']:
        if i['id'] == id:  # once you find the location ....
            for j in librariesJson['loclibs']:  # use the location to search your stored copy of the libraries Json
                if i['libraryId'] == j['id']:  # to find the associated library
                    friendlyResults['library_name'] = j['name']  # and pull the name
            friendlyResults['location'] = i[
                'code']  # finally, add the location code so that it shows up in that order in the output file.
    if not 'library_name' in friendlyResults:
        friendlyResults['libraryName'], friendlyResults['location'] = "Library not found", "Location not found"
    if not 'location' in friendlyResults:
        friendlyResults['location'] = "Location not found"


# map a circulation policy ID to friendly name

def policytoname(url, fetchHeaders, key, friendlyResults):
    # key in the function call is a variable; here, you have to read its value into a local variable to get
    # python's dictionary functions to call values as expected
    keyname = key
    postPolicy = requests.get(url, headers=fetchHeaders)
    postPolicyJson = postPolicy.json()
    # you should always get a policy - either the matched policy, or the fallback. So we don't add functions here to
    # accommodate not finding a result like we do in other functions
    for i in postPolicyJson:
        print(postPolicyJson[i])

