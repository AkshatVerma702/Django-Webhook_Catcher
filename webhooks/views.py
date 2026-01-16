from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

request_store = []

@csrf_exempt
# Create your views here.
def testing(request):
    print("Method: ", request.method)
    print("Path:", request.path)
    print("GET params:", request.GET.dict())   
    print("Headers:", dict(request.headers))   
    print("Body (raw):", request.body.decode('utf-8', errors='ignore'))  
    data = {
        "time": timezone.localtime(timezone.now()),
        "method" : request.method,
        "path": request.path,
        "get params": request.GET.dict(),
        "headers": dict(request.headers)
    }
    request_store.append(data)
    print(len(request_store))

    return render(request, "index.html", {"data": request_store})