from django.http import HttpResponse, JsonResponse
import sys
sys.path.insert(0, 'C:\\Users\\amona\\Documents\\Chargebee')
import getNames

def main(request):
    usage = getNames.initUsage()
    return JsonResponse(usage)