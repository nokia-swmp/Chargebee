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


def write(listForUser):     #input: Egy customer (?) [Name,Email,Subscriptions]
    print(listForUser)          #print minden?  [KERDES 6]
    print(listForUser[0])           # Name
    print(listForUser[1])           # Email
    for subs in listForUser[2]:     # Minden Subsc/re: [KERDES 7: mint KERDES 4]
        print(subs, ": \n{")
        for item in listForUser[2][subs]:   # Minden LineItem-re:
            print("    ", item, ": \n     {")                   
            print("        ", listForUser[2][subs][item][0])    #Date_From
            print("        ", listForUser[2][subs][item][1])    #Date_To
            print("        ", listForUser[2][subs][item][2])    #Amount
            print("        ", listForUser[2][subs][item][3])    #Description  (Sorrend mas lehet)
            print("     },\n")
        print("}")

#timespamp-bol datum formatumra valtas
def toDate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

# usage valtozoba beletolti a ChargeBee adatait
def initUsage():
    customers = chargebee.Customer.list({})
    
    usage = {}
    
    # usage[customer_id] dictionary vazanak elkeszitese: minden customerhez:
    # nev + email + honapok dictionary
    for cust in customers:
        c = cust.customer
        if not c.deleted:
            usage[c.id] = [c.first_name + " " + c.last_name, c.email, {"January": {}, "February": {}, "March": {}, "April": {}, "May": {}, "June": {}, "July": {}, "August": {}}]
    
    # honapok kezdoidejenek beallitasa
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

    # Invoice-ok listaja
    entries = chargebee.Invoice.list({})
    # minden Invoice-hoz:
    for entry in entries:
        c_id = entry.invoice.customer_id        # beallitja a customer_id-t
        # Az Invoice subsc_id-jat berakja a customer osszes honapjahoz (Miert?)
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
        
        # Az Invoice-on beluli osszes LineItem-re:
        for item in entry.invoice.line_items:
            if item.date_from <= sep and 'Plan' not in item.description:   #Ha Aug vegeig elkezdodik
                if item.date_from >= aug:       #Ha Augusztusban kezdodik
                    # Megfelelo (Customer -> "August" -> Subscription) dictionary-be:
                    #   LineItem cimzessel: [date_from, date_to, amount, description]
                    usage[c_id][2]["August"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                elif item.date_from >= jul:     #Ha Juliusban kezdodik      
                    if item.date_to < aug:          #Ha Juliusban veget is er:  berakja Juli-hoz ay Itemet
                        usage[c_id][2]["July"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                    else:               # [KERDES 2] Ha nem ert veget Juliusban: Minden honaphoz a megfelelo reszt (DE!!!)
                                        # (??? mindenhol Aprilis van!  &&& Barmilzen hosszu LineItem-et 2 honapra bont csak ???)
                                        # (??? Ez most csak a Marc - Apr atfedest kezeli jol?  Ha maskor vagz tobb honapos? ???)
                                        # [KERDES 3]
                                        # TODO: Replace April const with generic solution
                                        # TODO: Solve multiple (3+) months long LineItem separation
                        usage[c_id][2]["July"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(apr), item.amount/100*(apr-item.date_from)/(item.date_to-item.date_from), item.description]
                        usage[c_id][2]["August"][entry.invoice.subscription_id][item.id] = [toDate(apr), toDate(item.date_to), item.amount/100*(item.date_to-apr)/(item.date_to-item.date_from), item.description]
                elif item.date_from >= jun:     #Ha Juniusban kezdodik
                    if item.date_to < jul:
                        usage[c_id][2]["June"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(item.date_to), item.amount/100, item.description]
                    else:
                        usage[c_id][2]["June"][entry.invoice.subscription_id][item.id] = [toDate(item.date_from), toDate(apr), item.amount/100*(apr-item.date_from)/(item.date_to-item.date_from), item.description]
                        usage[c_id][2]["July"][entry.invoice.subscription_id][item.id] = [toDate(apr), toDate(item.date_to), item.amount/100*(item.date_to-apr)/(item.date_to-item.date_from), item.description]
                elif item.date_from >= may:     #Ha Majusban kezdodik
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
                # nyilvan csak 2018-01-01 - 2018.09.01  kozott jo most
    return usage

def useage(cust_id, date_from, date_to):    #Adott Customer mekkora ertekben hasznal az adott idoszakban 
    usedAmount = 0
    usage = initUsage()     # Feltolti adatokkal
    if cust_id in usage:    # Ha van cust_id-hez tartozo Customer a Usage-ben
        cust_use = usage[cust_id][2]    # Customerhez tartozo Honap-dictionary
        for subs in cust_use:           # ([KERDES 4] Ezek itt nem csak a honapok?)   Minden Subs-ra:
            for li in cust_use[subs]:       # minden LineItem-re:
                df = cust_use[subs][li][0]      # LineItem.Date_from
                dt = cust_use[subs][li][1]      # LineItem.Date_To
                am = cust_use[subs][li][2]      # LineItem.Amount
                if df <= date_to and dt >= date_from:   #Ha van atfedes a LineItem ideje es a lekerdezett idointervallum (Lek_Id_Int) kozott:
                    if df >= date_from:                 
                        if dt <= date_to:       #Ha a LineItem teljesen benne van a Lek_Id_Int-ban:
                            usedAmount += am        #Az LineItem teljes arat hozzaadjuk
                        else:                   #Ha a LineItem-nek kilog a vege:
                            usedAmount += am*(date_to - df)/(dt - df)   #aranyosan kevesebbet adunk hozza
                    else:
                        if dt <= date_to:       #Ha a LineItem-nek az eleje log ki:
                            usedAmount += am*(dt - date_from)/(dt - df)     #aranyosan...
                        else:                   #Ha a LineItem-nek az eleje es vege is kilog:
                            usedAmount += am*(date_to - date_from)/(dt - df)    #aranyosan...
    return usedAmount/100

# return: Customerek neveinek listaja (valtozasban van)
def listCustNames():
    custList = []
    custs = chargebee.Customer.list({})
    for cust in custs:
        custList.append(cust.customer.first_name + ' ' + cust.customer.last_name)
        #custList.append({cust.customer.id: cust.customer.first_name + ' ' + cust.customer.last_name})
    return custList

# input: Customer name ; return: Customerhez tartozo subsr_id-k listaja
def listSubsNames(cust):
    subsList = []
    subs = chargebee.Subscription.list({})
    for sub in subs:
        if sub.customer.first_name + ' ' + sub.customer.last_name == cust:
            subsList.append(sub.subscription.id)
    return subsList

# ([KERDES 5] pythonban overload?) return: minden Subscription ID-jet tartalmazo lista
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