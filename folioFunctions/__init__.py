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


