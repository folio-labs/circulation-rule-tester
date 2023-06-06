# FOLIO Circulation Rule tester

This is a very basic tool to allow you to test your circulation rules in FOLIO without having to actually create loans. You 
provide a CSV file as an input, and FOLIO provides the five circulation policies that would apply

## Background - FOLIO Circulation Rules System

FOLIO supports a WYSIWIG circulation rules editor that provides libraries with exceptional flexibility in writing rules to meet
their needs. Rules are defined according to one or more parameters - patron group, material type, loan type, or location tree. When
FOLIO determines that a set of parameters matches on a circulation transaction, it then uses the policies attached to the rule
to create the loan. More information can be found at https://docs.folio.org/docs/access/additional-topics/loans/loans/ and at
https://github.com/folio-org/mod-circulation/blob/master/doc/circulationrules.md

There are five categories of policies that are part of a circulation loan:
* Loan policy
* Request policy
* Notice policy
* Overdue fine policy
* Lost item fee policy

Each has its own call to figure out which policy applies. So, when you are attempting a loan, you are actually doing five different
transactions. What this script does is allows you to provide FOLIO with the four parameter values - patron group, material type, loan type,
and location - and then receive back the name of the five circulation policies that would apply if that loan transaction had occurred. This way
you can test what an actual transaction would do and review the results in bulk without actually having to create a loan.

### Example

Suppose a faculty member comes to your service point and wants to borrow a book from the location "Main Library Stacks". You scan their patron
information into the Check out app, and then you scan the item barcode to loan the book to the faculty member.

When you are loaning the item, FOLIO has to figure out which loan policy, request policy, notice policy, overdue policy, and lost item fee
policy apply so that it can create the loan. 

Behind the scenes, FOLIO is doing something like this (vastly oversimplified, of course):
* Check out app: "Hey Loan Policy API, I have a patron who has group **faculty**, an item with material type **book** and loan type **regular loan**, and the location is **Main stacks**. What loan policy applies?" Circulation module: "Use **Faculty year long loan**."
* Check out app: "Hey Request Policy API, I have a patron who has group **faculty**, an item with material type **book** and loan type **regular loan**, and the location is **Main stacks**. What loan policy applies?" Circulation module: "Use **Allow all requests**."
* Check out app: "Hey Notice Policy API, I have a patron who has group **faculty**, an item with material type **book** and loan type **regular loan**, and the location is **Main stacks**. What notice policy applies?" Circulation module: "Use **Faculty Notices**."
* Check out app: "Hey Overdue Fine Policy API, I have a patron who has group **faculty**, an item with material type **book** and loan type **regular loan**, and the location is **Main stacks**. What overdue fine policy applies?" Fee-fines module: "Use **Faculty overdue**."
* Check out app: "Hey Lost Item Fee Policy API, I have a patron who has group **faculty**, an item with material type **book** and loan type **regular loan**, and the location is **Main stacks**. What lost item fee policy applies?" Fee-fines module: "Use **General lost items**."

The script essentially mimics asking these questions to FOLIO and spits back the names of the policies that would apply **if** you were
loaning a "regular loan" book from the Main library stacks to your faculty member.

## Requirements

You need a FOLIO user account for the environment you are testing on with the following permissions
** circulation.rules.loan-policy.get
** circulation.rules.overdue-fine-policy.get
** circulation.rules.lost-item-policy.get
** circulation.rules.request-policy.get
** circulation.rules.notice-policy.get

Then you need
* loan-tester.py
* config-template.ini (filled out to include appropriate authentication information for your test environment)
* the folioFunctions library included in this repository

## Releases to use 
This script has been tested on Lotus and Morning Glory, and as far as we know should work on more updated/supported
versions of FOLIO

## How long does this script take to run? 
FOLIO does not have bulk circulation rule is tested one-by-one. That means that the length of time this
takes to run depends on how many combinations you are testing. As an example, at a large institution
that had over 100,000 combinations of patron group, loan type, material type, and location, the script
took approximately 15-18 hours. You're advised to run this on a separate computer like a VM where it can be
started and left to run until completion.

## What's the format to use for the input file?
Your input file should be in CSV format. Each row in the file is a combination of UUIDs that you would like to test. E.g., if your library
has five patron groups, five loan types, five material types and 20 locations, you would have 2500 lines to test if you wanted
to test your entire library. (You could, of course, test a smaller subset if desired.)

The UUIDs must be in the order shown below or else it won't work:

patron_type_id,loan_type_id,item_type_id,location_id
patrontypeUUID,loantypeUUID,itemtypeUUID,locationUUID
...
...
...

**NOTE** "item_type" in this script is referring to "material type" in the UI - the API calls it item type, I think that is tech debt 
from very early project decisions.

## How to run the script
The script takes two command line arguments:
1. The name of the server from the config.ini file
2. The name of the input file, including path if relevant.

E.g., if the name of my server in the config file is 'snapshot' and my filename is 'faculty_loan_tester.csv' then
I would run this at the command line as
./loanTester.py snapshot faculty_loan_tester.csv

## Contributors
This script was written by Erin Nettifee, with assistance from Tod Olson and Aaron Neslin. All three are members of the FOLIO community.
