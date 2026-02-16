from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from datetime import timedelta


@csrf_exempt
# Create your views here.
def catch(request):
    print("In catch view")
    return HttpResponse(f"HTTP Request caught")

def viewRequests(request):
    query_params = request.GET.copy()
    allrecords = HttpRequest.objects.all().order_by("-timestamp")

    method = request.GET.get("Method")
    status = request.GET.get("Status Code")
    path  = request.GET.get("Path")
    date_filter = request.GET.get("Date Range")
    sortType = request.GET.get("sort")
    
    if 'page' in query_params:
        query_params.pop('page') 
    
    if method:
        allrecords = allrecords.filter(http_method=method)

    if status:
        allrecords = allrecords.filter(response_status = status)

    if path:
        path = "/" + path
        allrecords = allrecords.filter(path__startswith = path)

    allrecords = date_query_set(date_filter, allrecords)

    if sortType == "timestamp_asc":
        allrecords = allrecords.order_by("timestamp")

    paginator = Paginator(allrecords, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    filters = {
        'Method': ['GET', 'POST', 'DELETE', 'PUT'],
        'Status Code': [200, 404, 400],
        'Path': ['catch', 'admin'],
        'Date Range': ["Last 1 Hour", "Last 24 Hours", "Last 7 Days", "Last 30 Days"]
    }
    return render(request, "index.html", {"page_obj": page_obj, "records": page_obj.object_list, "filters": filters, "active_method": method, "query_params": query_params.urlencode()})

def date_query_set(filter, allrecords):
    curr = timezone.now()

    filters = {
        "Last 1 Hour": timedelta(hours=1),
        "Last 24 Hours": timedelta(hours=24),
        "Last 7 Days": timedelta(days=7),
        "Last 30 Days": timedelta(days=30)
    }

    delta = filters.get(filter)

    if not delta:
        return allrecords

    cutoff = curr - delta
    return allrecords.filter(timestamp__gte = cutoff)

def getRequest(request, target_id):
    target_record = get_object_or_404(HttpRequest, id = target_id)
    return render(request, "view.html", {"records": [target_record]})


@require_http_methods(["POST"])
def delete_all_requests(request):
    all_records = HttpRequest.objects.all()

    if all_records.count() == 0:
        return HttpResponse("No records found")

    all_records.delete()
    return redirect('getAllRequests')

