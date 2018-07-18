from django.shortcuts import render
from django.http import HttpResponse
import getNames
import add_testDb
import addLineItem
# Create your views here.

def addForm(request):
    custs = getNames.listCustNames()
    #chosenCust = request.POST.get('custs', 'Austin Jones')
    subs = getNames.listSubsByCust()
    return render(
            request,
            'addForm.html',
            context={'custs':custs, 'subs':subs},
        )
    #return addFormCust(request)

def addFormCust(request):
    custs={'cust1':['subs_first','subs_second'], 'cust2':['subs_third'], 'cust3':[]}
    return render(
            request,
            'addFormCust.html',
            context={'custs': custs},
        )
    #return HttpResponse("You're looking at addLineItem.")

def addFormSubs(request):
    print(request)
    return render(
            request,
            'addFormSubs.html',
            context={'cust': request},
        )

def saveLineItem(request):
    add_testDb.addLineItem(request.POST['custs'], request.POST['subs'], request.POST['start'], request.POST['end'], request.POST['desc'], request.POST['amount'])
    return HttpResponse("Your line item is added to chargebee")