from django.utils.deprecation import MiddlewareMixin
from .models import HttpRequest, WebhookToken

class myMiddleware(MiddlewareMixin):
    def process_request(self, request):
        req_path = request.path
        
        
        if req_path.startswith('/webhook'):
            try:
                parts = req_path.strip("/").split("/")
                if len(parts) == 2:
                    token = parts[1]
                token_obj = WebhookToken.objects.get(
                    token= token,
                    is_active= True
                )

                request.token_obj = token_obj

                entry = HttpRequest.createEntry(request, token_obj)
                request.created_entry = entry
            except WebhookToken.DoesNotExist:
                pass

        
    def process_response(self, request, response):
        
        if hasattr(request, 'created_entry') and hasattr(request, "token_obj"):
            request.created_entry.response_status = response.status_code
            request.created_entry.save()

        return response