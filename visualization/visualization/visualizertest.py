from django.http import HttpResponse, JsonResponse
import sys
sys.path.insert(0, 'C:\\Users\\VALKI\\Documents\\Chargebee')
import getNames

def main(request):
    usage = getNames.initUsage()
    return JsonResponse(usage)