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
'''
start = "24/04/2018"
s = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
end = "29/04/2018"
e = time.mktime(datetime.datetime.strptime(end, "%d/%m/%Y").timetuple())

result = chargebee.Invoice.add_charge("draft_inv_Hr5514rQuIhYNa11wE", {
    "amount" : 7500, 
    "description" : "austin april fourth",
    "line_item[date_from]" : int(s),
    "line_item[date_to]" : int(e)
    })
invoice = result.invoice

'''
entry = chargebee.Invoice.list({})
for k in entry:
    print(k)
