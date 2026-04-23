from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import HttpRequest, WebhookToken
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import uuid
from datetime import timedelta

def viewRequests(request):
    records = filter_records(request)

    query_params = request.GET.copy()

    if 'page' in query_params:
        query_params.pop('page')

    paginator = Paginator(records, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    filters = {
        'Method': ['GET', 'POST', 'DELETE', 'PUT'],
        'Status Code': [200, 404, 400],
        'Path': ['catch', 'admin'],
        'Date Range': ["Last 1 Hour", "Last 24 Hours", "Last 7 Days", "Last 30 Days"],
    }

    return render(request, "index.html", {
        "page_obj": page_obj,
        "filters": filters, 
        "records": page_obj.object_list,
        "query_params": query_params.urlencode(),
        "active_method": request.GET.get("Method")
    })

def filter_records(request):
    filtered_records = HttpRequest.objects.all().order_by("-timestamp")
    
    method = request.GET.get("Method")
    status = request.GET.get("Status Code")
    path = request.GET.get("Path")
    date_filter = request.GET.get("Date Range")
    sort = request.GET.get("sort")

    if method :
        filtered_records = filtered_records.filter(http_method = method)
    
    if status:
        filtered_records = filtered_records.filter(response_status = status)
    
    if path:
        path = "/" + path
        filtered_records = filtered_records.filter(path__startswith = path)


    filtered_records = date_query_set(date_filter, filtered_records)

    return filtered_records


def updateView(request):
    records = filter_records(request)

    paginator = Paginator(records, 5)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    data = [
        {
            "id": req.id,
            "method": req.http_method,
            "status": req.response_status,
            "path": req.path,
            "time": req.timestamp
        }for req in page_obj
    ]

    return JsonResponse({
        "data": data
    })

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

@csrf_exempt
def generateToken(request):

    token_obj = WebhookToken.objects.create(
        token = uuid.uuid4(),
        expiry = timezone.now() + timedelta(hours=1),
        is_active =True
    )

    return JsonResponse({
        "token": token_obj.token,
        "url": f"/webhook/{token_obj.token}"
    })


def catchRequest(request, token):
    if not hasattr(request, "token_obj"):
        return HttpResponse("Invalid Webhook", status=404)
    return HttpResponse("Webhook Hit")


