from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from webhooks.models import HttpRequest
from django.core.paginator import Paginator
from django.http import JsonResponse

def health(request):
    return render(request, "health.html")


def homepage(request):
    return render(request, "homepage.html")

def update_Request(request):
    records = HttpRequest.objects.all().order_by("timestamp")

    page = request.GET.get("page", 1)
    paginator = Paginator(records, 5)
    page_obj = paginator.get_page(page)


    data = []

    for req in page_obj:
        data.append({
            "id": req.id,
            "method": req.http_method,
            "path": req.path,
            "status": req.response_status,
            "time": req.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return JsonResponse(data, safe=False)