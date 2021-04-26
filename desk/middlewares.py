from django.contrib.auth import logout
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_superuser:
            request.session['last_action'] = timezone.now()
            if (timezone.now() - request.session['last_action']).seconds >= 5*2:
                logout(request)
        return request
