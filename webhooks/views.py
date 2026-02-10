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
    entry = HttpRequest.createEntry(request)
    response = HttpResponse(...)
    print(response)
    return HttpResponse(f"HTTP Request caught")

def viewRequests(request):
    allrecords = HttpRequest.objects.all().order_by("-timestamp")

    method = request.GET.get("Method")
    status = request.GET.get("Status Code")

    print(method)
    print(status)

    if method is not None:
        allrecords = allrecords.filter(http_method=method)
    paginator = Paginator(allrecords, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    filters = {
        'Method': ['GET', 'POST', 'DELETE', 'UPDATE'],
        'Status Code': [200, 404, 400],
        # 'Date Range': ["Last 1 Hour", "24 Hours"]
    }
    return render(request, "index.html", {"page_obj": page_obj, "records": page_obj.object_list, "filters": filters, "active_method": method})

def getRequest(request, target_id):
    target_record = get_object_or_404(HttpRequest, id = target_id)
    return render(request, "view.html", {"records": [target_record]})

def delete_all_requests(request):
    all_records = HttpRequest.objects.all()

    if all_records.count() == 0:
        return HttpResponse("No records found")

    return HttpResponse("Records Deleted")