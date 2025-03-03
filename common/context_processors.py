from django.conf import settings


def base_domain(request):
    return {'base_domain': settings.BASE_DOMAIN}
