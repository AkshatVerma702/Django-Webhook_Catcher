from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

@csrf_exempt
# Create your views here.
def catch(request):
    
    return HttpResponse("HTTP Request Caught ")

def viewRequests(request):
    allrecords = HttpRequest.objects.all().order_by("-timestamp")
    method = request.GET.get("method")

    if method:
        allrecords = allrecords.filter(http_method=method)
    paginator = Paginator(allrecords, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    filters = {
        'method': ['GET', 'POST', 'DELETE', 'UPDATE']
    }
    return render(request, "index.html", {"page_obj": page_obj, "records": page_obj.object_list, "filters": filters, "active_method": method})

def getRequest(request, target_id):
    target_record = get_object_or_404(HttpRequest, id = target_id)
    return render(request, "view.html", {"records": [target_record]})

