from django.shortcuts import render
from django.http import HttpResponse
import getNames
import addLineItem
# Create your views here.

def addForm(request):
    print("Hello world")
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
    print(request.method)
    print(request.body)
    return HttpResponse("ok")