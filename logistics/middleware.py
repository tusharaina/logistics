from django.utils.cache import patch_vary_headers
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseRedirect

from userlogin.models import Subdomain

class SubdomainMiddleware:
    def process_request(self, request):
        # Strip off the port, mostly useful for development environments
        fqdn = request.get_host().split(':')[0]

        # Break up the domain into parts and get the subdomain slug
        domain_parts = fqdn.split('.')
        if len(domain_parts) > 2:
            subdomain = domain_parts[0]
            if subdomain.lower() == 'www':
                subdomain = None
        else:
            subdomain = None

        try:
            request.account = Subdomain.objects.get(
                Q(url=fqdn) |
                Q(name=subdomain)
            )
        except Subdomain.DoesNotExist:
            pass
        else:
            request.urlconf = settings.SUBDOMAIN_URLCONF

    def process_response(self, request, response):
        patch_vary_headers(response, ('Host',))
        return response