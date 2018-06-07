# -*- coding: utf-8 -*-
'''
Created on 2018. máj. 22.

@author: Andris
'''

import chargebee
import sys
import json
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

def initUsage():
    customers = chargebee.Customer.list({})
    
    usage = {}
    
    for cust in customers:
        c = cust.customer
        if not c.deleted:
            usage[c.id] = [c.first_name + " " + c.last_name, c.email, {"January": {}, "February": {}, "March": {}, "April": {}}]
    
    start = "01/01/2018"
    jan = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    start = "01/02/2018"
    feb = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    start = "01/03/2018"
    mar = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    start = "01/04/2018"
    apr = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())


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
        for item in entry.invoice.line_items:
            if item.date_from >= apr:
                usage[c_id][2]["April"][entry.invoice.subscription_id][item.id] = [item.date_from, item.date_to, item.amount, item.description]
            elif item.date_from >= mar:
                usage[c_id][2]["March"][entry.invoice.subscription_id][item.id] = [item.date_from, item.date_to, item.amount, item.description]
            elif item.date_from >= feb:
                usage[c_id][2]["February"][entry.invoice.subscription_id][item.id] = [item.date_from, item.date_to, item.amount, item.description]
            elif item.date_from >= jan:
                usage[c_id][2]["January"][entry.invoice.subscription_id][item.id] = [item.date_from, item.date_to, item.amount, item.description]
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

def toDate(dmy):
    return time.mktime(datetime.datetime.strptime(dmy, "%d/%m/%Y").timetuple())


u = initUsage()
with open('usageJson2.txt', 'w') as outfile:
    json.dump(u, outfile)
#u_json = json.dumps(u)
#write(u[sys.argv[1]])
#print(useage(sys.argv[1], toDate(sys.argv[2]), toDate(sys.argv[3])))