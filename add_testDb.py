# -*- coding: utf-8 -*-
'''
Created on 2018. máj. 13.

@author: Andris
'''

import chargebee
import time
import datetime
import calendar
import json

chargebee.ChargeBee.verify_ca_certs = False
chargebee.configure("test_ac68LkfLCfkacuYl5wINzwgZR9uzTecuzd","nokia-swmp-test")

def addByHand():
    start = "01/07/2018 10:12"
    s = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y %H:%M").timetuple())
    end = "04/07/2018 06:40"
    e = time.mktime(datetime.datetime.strptime(end, "%d/%m/%Y %H:%M").timetuple())

    # parameter of chargebee.Invoice.add_charge()  to be set for different invoices
    result = chargebee.Invoice.add_charge("draft_inv_1mk51bnQxg0uPxRRZ", {
        "amount" : 4000, 
        "description" : "eNodeB_demo_1_jul",
        "line_item[date_from]" : int(s),
        "line_item[date_to]" : int(e)
        })
    invoice = result.invoice

# should use customer too
def findInvoice(cust, subs):
    invs = chargebee.Invoice.list({'limit': 100})
    for inv in invs:
        #print(inv)
        if inv.invoice.subscription_id == subs and 'draft' in inv.invoice.id:
            return inv.invoice
    return False

def addLineItem(customer, subscription, start, end, description, amount):
    start = start.replace('T',' ')
    end = end.replace('T',' ')
    s = time.mktime(datetime.datetime.strptime(start, "%Y-%m-%d %H:%M").timetuple())
    e = time.mktime(datetime.datetime.strptime(end, "%Y-%m-%d %H:%M").timetuple())
    inv = findInvoice(customer, subscription)
    #print(amount, float(amount), (int(e)-int(s))/1000*float(amount))
    #print(inv)
    if inv:
        #print(inv.id, description, int(s), int(e))
        am = int((int(e)-int(s))/36*float(amount))
        result = chargebee.Invoice.add_charge(inv.id, {
            "amount" : am,
            "description" : description,
            "line_item[date_from]" : int(s),
            "line_item[date_to]" : int(e)
        })
        #for inv in invId:
        #    print(inv)
'''
addByHand()
entry = chargebee.Invoice.list({})
for k in entry:
    print(k)

print(s,e)
'''
#TODO: findInvoice to be corrected so that it searches for the subscription of the given custumer
#TODO: In AddLineItem if findInvoice returns False, print something else for the customer
#TODO: AddForm's input validation needs to be done
