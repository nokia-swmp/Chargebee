# -*- coding: utf-8 -*-
'''
Created on 2018. máj. 22.

@author: Andris
'''

import chargebee
import sys
import json
import datetime
import time
import datetime

chargebee.ChargeBee.verify_ca_certs = False
chargebee.configure("test_ac68LkfLCfkacuYl5wINzwgZR9uzTecuzd","nokia-swmp-test")


def write(listForUser):
    print(listForUser)
    print(listForUser[0])
    print(listForUser[1])
    for subs in listForUser[2]:
        print(subs, ": \n{")
        for item in listForUser[2][subs]:
            print("    ", item, ": \n     {")
            print("        ", listForUser[2][subs][item][0])
            print("        ", listForUser[2][subs][item][1])
            print("        ", listForUser[2][subs][item][2])
            print("        ", listForUser[2][subs][item][3])
            print("     },\n")
        print("}")

def toDate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

def initUsage():
    customers = chargebee.Customer.list({})
    
    usage = {}
    
    for cust in customers:
        c = cust.customer
        if not c.deleted:
            usage[c.id] = [c.first_name + " " + c.last_name, c.email, {"January": {}, "February": {}, "March": {}, "April": {}, "May": {}, "June": {}, "July": {}, "August": {}}]
    
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

    entries = chargebee.Invoice.list({})
    
    for entry in entries:
        c_id = entry.invoice.customer_id
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
        for item in entry.invoice.line_items:
            if item.date_from <= sep and 'Plan' not in item.description:
                if item.date_from >= aug:
                    usage[c_id][2]["August"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                elif item.date_from >= jul:
                    if item.date_to < aug:
                        usage[c_id][2]["July"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                    else:
                        usage[c_id][2]["July"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(apr), item.amount/100*(apr-item.date_from)/(item.date_to-item.date_from), item.description]
                        usage[c_id][2]["August"][entry.invoice.subscription_id][item.id] = [toDate(apr), toDate(item.date_to), item.amount/100*(item.date_to-apr)/(item.date_to-item.date_from), item.description]
                elif item.date_from >= jun:
                    if item.date_to < jul:
                        usage[c_id][2]["June"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                    else:
                        usage[c_id][2]["June"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(apr), item.amount/100*(apr-item.date_from)/(item.date_to-item.date_from), item.description]
                        usage[c_id][2]["July"][entry.invoice.subscription_id][item.id] = [toDate(apr), toDate(item.date_to), item.amount/100*(item.date_to-apr)/(item.date_to-item.date_from), item.description]
                elif item.date_from >= may:
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
    return usage

def useage(cust_id, date_from, date_to):
    usedAmount = 0
    usage = initUsage()
    if cust_id in usage:
        cust_use = usage[cust_id][2]
        for subs in cust_use:
            for li in cust_use[subs]:
                df = cust_use[subs][li][0]
                dt = cust_use[subs][li][1]
                am = cust_use[subs][li][2]
                if df <= date_to and dt >= date_from:
                    if df >= date_from:
                        if dt <= date_to:
                            usedAmount += am
                        else:
                            usedAmount += am*(date_to - df)/(dt - df)
                    else:
                        if dt <= date_to:
                            usedAmount += am*(dt - date_from)/(dt - df)
                        else:
                            usedAmount += am*(date_to - date_from)/(dt - df)
    return usedAmount/100

def listCustNames():
    custList = []
    custs = chargebee.Customer.list({})
    for cust in custs:
        custList.append(cust.customer.first_name + ' ' + cust.customer.last_name)
        #custList.append({cust.customer.id: cust.customer.first_name + ' ' + cust.customer.last_name})
    return custList

def listSubsNames(cust):
    subsList = []
    subs = chargebee.Subscription.list({})
    for sub in subs:
        if sub.customer.first_name + ' ' + sub.customer.last_name == cust:
            subsList.append(sub.subscription.id)
    return subsList

def listSubsNames():
    subsList = []
    subs = chargebee.Subscription.list({})
    for sub in subs:
        subsList.append(sub.subscription.id)
    return subsList

def listSubsByCust():
    subsDict = {}
    subs = chargebee.Subscription.list({})
    for sub in subs:
        if sub.customer.first_name + ' ' + sub.customer.last_name in subsDict:
            subsDict[sub.customer.first_name + ' ' + sub.customer.last_name].append(sub.subscription.id)
        else:
            subsDict[sub.customer.first_name + ' ' + sub.customer.last_name] = [sub.subscription.id]
    return subsDict

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