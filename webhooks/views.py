from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import HttpRequest
import json

@csrf_exempt
# Create your views here.
def catch(request):
    body = request.body.decode("utf-8", errors="ignore")
    data = {
        "timestamp": timezone.now(),
        "http_method" : request.method,
        "path": request.path,
        "headers": json.dumps(dict(request.headers)),
        "request_body": body
    }

    HttpRequest.objects.create(**data)

    request_Count = HttpRequest.objects.count()

    return HttpResponse("HTTP Request Caught " + str(request_Count))

def viewRequests(request):
    allrecords = HttpRequest.objects.all()

    return render(request, "index.html", {"data": allrecords})

def getRequest(request, target_id):
    target_record = get_object_or_404(HttpRequest, id = target_id)

    return render(request, "view.html", {"records": [target_record]})