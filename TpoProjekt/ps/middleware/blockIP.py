
from django.conf import settings
from django import http
from django.utils import timezone
import datetime


class BlockedIpMiddleware(object):

    def process_request(self, request):
        if len(settings.BLOCKED_TIME) > 0:
            reg_time = settings.BLOCKED_TIME[0]
            now = datetime.datetime.now()
            s1 = reg_time.second + reg_time.minute * 60 + reg_time.hour * 3600
            s2 = now.second + now.minute * 60 + now.hour * 3600
            if s2 -s1 > 20:
                settings.BLOCKED_IPS = []
                settings.BLOCKED_TIME = []
        if request.META['REMOTE_ADDR'] in settings.BLOCKED_IPS:
            return http.HttpResponse('<h1>Dostop začasno prepovedan</h1>' + str(timezone.now()))
        return None
