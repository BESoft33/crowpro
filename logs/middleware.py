import time
from django.utils.timezone import now
from django.contrib.gis.geoip2 import GeoIP2
from user_agents import parse as parse_ua
from logs.models import RequestLog


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geoip = GeoIP2()

    def __call__(self, request):
        # Start timer
        start_time = time.time()

        # Info before response
        method = request.method
        path = request.get_full_path()
        headers = get_request_headers(request)
        remote_addr = get_client_ip(request)
        referrer = request.META.get('HTTP_REFERER', '')
        user_agent_str = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse_ua(user_agent_str)

        device = (
            "Mobile" if user_agent.is_mobile
            else "Tablet" if user_agent.is_tablet
            else "PC"
        )
        browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
        os = f"{user_agent.os.family} {user_agent.os.version_string}"

        # Geolocation
        country = ''
        timezone = ''
        try:
            geo_data = self.geoip.city(remote_addr)
            country = geo_data.get('country_name', '')
            timezone = geo_data.get('time_zone', '')
        except Exception:
            pass

        body = ''
        if method in ['POST', 'PUT', 'PATCH']:
            try:
                body = request.body.decode('utf-8')
            except Exception:
                body = '<unreadable body>'

        # Get user if authenticated
        user = request.user if request.user.is_authenticated else None

        # Get the response first
        response = self.get_response(request)
        duration = (time.time() - start_time) * 1000  # in ms

        # Save the log
        RequestLog.objects.create(
            user=user,
            method=method,
            path=path,
            headers=headers,
            body=body,
            remote_addr=remote_addr,
            referrer=referrer,
            user_agent=user_agent_str,
            device=device,
            browser=browser,
            os=os,
            country=country,
            timezone=timezone,
            status_code=response.status_code,
            duration_ms=round(duration, 2),
        )

        return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')


def get_request_headers(request):
    return {
        k[5:].replace('_', '-').title(): v
        for k, v in request.META.items()
        if k.startswith('HTTP_')
    }
