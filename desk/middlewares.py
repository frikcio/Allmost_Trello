from django.contrib.auth import logout
from django.utils import timezone

from django.utils.dateparse import parse_datetime
from django.utils.deprecation import MiddlewareMixin

from Trello.settings import AUTO_LOGOUT_TIME


class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_superuser:
            try:
                if (timezone.now() - parse_datetime(request.session['last_action'])).seconds >= AUTO_LOGOUT_TIME*60:
                    logout(request)
            except KeyError:
                pass
            finally:
                request.session['last_action'] = str(timezone.now())
        return self.get_response(request)
