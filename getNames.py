# -*- coding: utf-8 -*-
'''
Created on 2018. máj. 22.

@author: Andris
'''

#a

import chargebee
import sys
import json
import datetime
import time

chargebee.ChargeBee.verify_ca_certs = False
chargebee.configure("test_ac68LkfLCfkacuYl5wINzwgZR9uzTecuzd","nokia-swmp-test")


def write(listForUser):     #input: One customer in this format: [Name,Email,Subscriptions]
    print(listForUser)          #print all
    print(listForUser[0])           # Name
    print(listForUser[1])           # Email
    for subs in listForUser[2]:     # For each Subsc: [data structure has been changed since -> doesnt work right now]
        print(subs, ": \n{")
        for item in listForUser[2][subs]:   # for each LineItem:
            print("    ", item, ": \n     {")                   
            print("        ", listForUser[2][subs][item][0])    #Date_From
            print("        ", listForUser[2][subs][item][1])    #Date_To
            print("        ", listForUser[2][subs][item][2])    #Amount
            print("        ", listForUser[2][subs][item][3])    #Description
            print("     },\n")
        print("}")

# makes date format from timestamp
def toDate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

# returns the data from ChargeBee
def initUsage():
    customers = chargebee.Customer.list({})
    
    usage = {}
    
    # crating the frame of usage[customer_id] dictionary for each customer:  (Name + Email + months dictionary)
    for cust in customers:
        c = cust.customer
        if not c.deleted:
            usage[c.id] = [c.first_name + " " + c.last_name, c.email, {"January": {}, "February": {}, "March": {}, "April": {}, "May": {}, "June": {}, "July": {}, "August": {}}]
    
    # setting the starting times of months
    start = "01/01/2018"
    jan = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    start = "01/02/2018"
    feb = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    start = "01/03/2018"
    mar = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    start = "01/04/2018"
    apr = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    start = "01/05/2018"
    may = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    start = "01/06/2018"
    jun = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    start = "01/07/2018"
    jul = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    start = "01/08/2018"
    aug = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    start = "01/09/2018"
    sep = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())

    # list of Invoices
    entries = chargebee.Invoice.list({})
    # for each Invoice:
    for entry in entries:
        c_id = entry.invoice.customer_id        # set customer_id
        # Assigns the subsc_id of the Invoice to each months for a customer.
        #TODO: Subscription ID olny at proper months
        if entry.invoice.subscription_id not in usage[c_id][2]["January"]:
            usage[c_id][2]["January"][entry.invoice.subscription_id] = {}
        if entry.invoice.subscription_id not in usage[c_id][2]["February"]:
            usage[c_id][2]["February"][entry.invoice.subscription_id] = {}
        if entry.invoice.subscription_id not in usage[c_id][2]["March"]:
            usage[c_id][2]["March"][entry.invoice.subscription_id] = {}
        if entry.invoice.subscription_id not in usage[c_id][2]["April"]:
            usage[c_id][2]["April"][entry.invoice.subscription_id] = {}
        if entry.invoice.subscription_id not in usage[c_id][2]["May"]:
            usage[c_id][2]["May"][entry.invoice.subscription_id] = {}
        if entry.invoice.subscription_id not in usage[c_id][2]["June"]:
            usage[c_id][2]["June"][entry.invoice.subscription_id] = {}
        if entry.invoice.subscription_id not in usage[c_id][2]["July"]:
            usage[c_id][2]["July"][entry.invoice.subscription_id] = {}
        if entry.invoice.subscription_id not in usage[c_id][2]["August"]:
            usage[c_id][2]["August"][entry.invoice.subscription_id] = {}
        
        # for each LineItem in an Invoice:
        for item in entry.invoice.line_items:
            if item.date_from <= sep and 'Plan' not in item.description:   #If it starts until the end of August
                if item.date_from >= aug:       #If it starts in August
                    # Into the proper (Customer -> "August" -> Subscription) dictionary:
                    #   LineItem ID: [date_from, date_to, amount, description]
                    usage[c_id][2]["August"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                elif item.date_from >= jul:     #If it starts in July      
                    if item.date_to < aug:          #If it ends in July:  puts in the Item to July
                        usage[c_id][2]["July"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                    else:               # If it doesn't end in July: Splitting by months (DE!!!)
                                        # (!!! April is hardcoded at some wrong places!  &&& Splits 3+ months long Items into 2 parts only !!!)
                                        # TODO: Replace April const with generic solution
                                        # TODO: Solve multiple (3+) months long LineItem separation
                        usage[c_id][2]["July"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(apr), item.amount/100*(apr-item.date_from)/(item.date_to-item.date_from), item.description]
                        usage[c_id][2]["August"][entry.invoice.subscription_id][item.id] = [toDate(apr), toDate(item.date_to), item.amount/100*(item.date_to-apr)/(item.date_to-item.date_from), item.description]
                elif item.date_from >= jun:     #If it starts in Juny
                    if item.date_to < jul:
                        usage[c_id][2]["June"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                    else:
                        usage[c_id][2]["June"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(apr), item.amount/100*(apr-item.date_from)/(item.date_to-item.date_from), item.description]
                        usage[c_id][2]["July"][entry.invoice.subscription_id][item.id] = [toDate(apr), toDate(item.date_to), item.amount/100*(item.date_to-apr)/(item.date_to-item.date_from), item.description]
                elif item.date_from >= may:     #If it starts in May
                    if item.date_to < jun:
                        usage[c_id][2]["May"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                    else:
                        usage[c_id][2]["May"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(apr), item.amount/100*(apr-item.date_from)/(item.date_to-item.date_from), item.description]
                        usage[c_id][2]["June"][entry.invoice.subscription_id][item.id] = [toDate(apr), toDate(item.date_to), item.amount/100*(item.date_to-apr)/(item.date_to-item.date_from), item.description]
                elif item.date_from >= apr:
                    if item.date_to < may:
                        usage[c_id][2]["April"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                    else:
                        usage[c_id][2]["April"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(apr), item.amount/100*(apr-item.date_from)/(item.date_to-item.date_from), item.description]
                        usage[c_id][2]["May"][entry.invoice.subscription_id][item.id] = [toDate(apr), toDate(item.date_to), item.amount/100*(item.date_to-apr)/(item.date_to-item.date_from), item.description]
                elif item.date_from >= mar:
                    if item.date_to < apr:
                        usage[c_id][2]["March"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                    else:
                        usage[c_id][2]["March"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(apr), item.amount/100*(apr-item.date_from)/(item.date_to-item.date_from), item.description]
                        usage[c_id][2]["April"][entry.invoice.subscription_id][item.id] = [toDate(apr), toDate(item.date_to), item.amount/100*(item.date_to-apr)/(item.date_to-item.date_from), item.description]
                elif item.date_from >= feb:
                    if item.date_to < mar:
                        usage[c_id][2]["February"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                    else:
                        usage[c_id][2]["February"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(mar), item.amount/100*(mar-item.date_from)/(item.date_to-item.date_from), item.description]
                        usage[c_id][2]["March"][entry.invoice.subscription_id][item.id] = [toDate(mar), toDate(item.date_to), item.amount/100*(item.date_to-mar)/(item.date_to-item.date_from), item.description]
                elif item.date_from >= jan:
                    if item.date_to < feb:
                        usage[c_id][2]["January"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                    else:
                        usage[c_id][2]["January"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(feb), item.amount/100*(feb-item.date_from)/(item.date_to-item.date_from), item.description]
                        usage[c_id][2]["February"][entry.invoice.subscription_id][item.id] = [toDate(feb), toDate(item.date_to), item.amount/100*(item.date_to-feb)/(item.date_to-item.date_from), item.description]
                # works between 2018.01.01 - 2018.08.30 only
    return usage

def useage(cust_id, date_from, date_to):    # total amount for a single customer in the given time interval 
    usedAmount = 0
    usage = initUsage()     # loads data from ChargeBee
    if cust_id in usage:    # If the customer with the given ID exists:
        cust_use = usage[cust_id][2]    # month-directory of the customer
        for subs in cust_use:           # Minden Subs-ra: (!!! data structure has changed since. Should be updated if used !!!)
            for li in cust_use[subs]:       # for each LineItem:
                df = cust_use[subs][li][0]      # LineItem.Date_from
                dt = cust_use[subs][li][1]      # LineItem.Date_To
                am = cust_use[subs][li][2]      # LineItem.Amount
                if df <= date_to and dt >= date_from:   #If there is an intersection between LineItem's time and the given time interval (Giv_Time_Int):
                    if df >= date_from:                 
                        if dt <= date_to:       #If Giv_Time_Int fully includes the LineItems time:
                            usedAmount += am        # adds the full time of the LineItem
                        else:                   #If the LineItems time's end is otside:
                            usedAmount += am*(date_to - df)/(dt - df)   #adds proportionally less
                    else:
                        if dt <= date_to:       #If the LineItems time's start is otside:
                            usedAmount += am*(dt - date_from)/(dt - df)     #adds proportionally less
                        else:                   #If the LineItems time's start and end are both otside:
                            usedAmount += am*(date_to - date_from)/(dt - df)    #adds proportionally less
    return usedAmount/100

# returns: List of names of customers
def listCustNames():
    custList = []
    custs = chargebee.Customer.list({})
    for cust in custs:
        custList.append(cust.customer.first_name + ' ' + cust.customer.last_name)
        #custList.append({cust.customer.id: cust.customer.first_name + ' ' + cust.customer.last_name})
    return custList

# input: Customer name ; return: Customer's list of subsr_id-s
def listSubsNames(cust):
    subsList = []
    subs = chargebee.Subscription.list({})
    for sub in subs:
        if sub.customer.first_name + ' ' + sub.customer.last_name == cust:
            subsList.append(sub.subscription.id)
    return subsList

# (!!! no overload in python !!!) return: a list with all subscription_id-s
def listSubsNames():
    subsList = []
    subs = chargebee.Subscription.list({})
    for sub in subs:
        subsList.append(sub.subscription.id)
    return subsList

# return: {customer name: [customer's subsriptions' ID list]}  dictionary
def listSubsByCust():       
    subsDict = {}
    subs = chargebee.Subscription.list({})
    for sub in subs:
        if sub.customer.first_name + ' ' + sub.customer.last_name in subsDict:
            subsDict[sub.customer.first_name + ' ' + sub.customer.last_name].append(sub.subscription.id)
        else:
            subsDict[sub.customer.first_name + ' ' + sub.customer.last_name] = [sub.subscription.id]
    return subsDict

#----------------For testing only ----------------------
#print(listSubsByCust())
#u = initUsage()
#with open('usageJson.txt', 'w') as outfile:
#    json.dump(u, outfile)
#u_json = json.dumps(u)
#write(u[sys.argv[1]])
#print(useage(sys.argv[1], toDate(sys.argv[2]), toDate(sys.argv[3])))

#--------------------------------------------------
#TODO
#cut at monthend
#write toDate function
#TODO: Throw out unnecessary functions : write, useage, listSubsNames, AddFormCust, AddFormSubs
#TODO: Subscription ID olny at proper months
#TODO: Replace April const with generic solution
#TODO: Solve multiple (3+) months long LineItem separation
'''TODO: django refactorisation: 
                Bottom visualization folder needs to be moved up
                usage of generic views
                add app namespaces'''


#----------------------------------------------------------------
''' TODO: Use of ChargeBee:
- Better use of "Plans"
'''