# core/middleware.py

from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)

class BlockUnauthorizedToolsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_agents = [
            "postmanruntime", "curl", "httpclient", "python-requests",
            "java", "go-http-client", "insomnia", "okhttp"
        ]
        self.trusted_origins = [
            "http://127.0.0.1:8080/",
            "https://yourmobileapp.com"
        ]

    def __call__(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
        origin = request.META.get("HTTP_ORIGIN", "")
        referer = request.META.get("HTTP_REFERER", "")

        if not user_agent:
            logger.warning(f"Missing UA - IP: {self.get_client_ip(request)}")
            return HttpResponseForbidden("Blocked: Missing User-Agent.")

        if any(agent in user_agent for agent in self.blocked_agents):
            logger.warning(f"Blocked UA: {user_agent} - IP: {self.get_client_ip(request)}")
            return HttpResponseForbidden("Blocked: Suspicious User-Agent.")

        if origin and origin not in self.trusted_origins:
            logger.warning(f"Blocked Origin: {origin}")
            return HttpResponseForbidden("Blocked: Untrusted Origin.")

        if referer and not any(trusted in referer for trusted in self.trusted_origins):
            logger.warning(f"Blocked Referer: {referer}")
            return HttpResponseForbidden("Blocked: Untrusted Referer.")

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")
