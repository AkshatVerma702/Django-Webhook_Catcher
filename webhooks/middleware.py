from django.utils.deprecation import MiddlewareMixin
from .models import HttpRequest

class myMiddleware(MiddlewareMixin):
    def process_request(self, request):
        req_path = request.path
        if req_path == "/catch/request/":
            entry = HttpRequest.createEntry(request)
            request.created_entry = entry

        
    def process_response(self, request, response):
        print(response)
        if hasattr(request, 'created_entry'):
            request.created_entry.response_status = response.status_code
            request.created_entry.save()
        return response