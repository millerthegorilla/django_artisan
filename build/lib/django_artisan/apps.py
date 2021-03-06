import importlib.util
import sys, logging, redis, elasticsearch

from django import apps
from django.db import models
from django.conf import settings
from django.core import exceptions

logger = logging.getLogger('django_artisan')


class DjangoArtisan(apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_artisan'

    def ready(self) -> None:
        models.signals.post_migrate.connect(callback, sender=self)
        try:
            settings.DEBUG
        except NameError:
            logger.info("settings.DEBUG is not defined, assuming production mode.")
        else:
            if settings.DEBUG and 'runserver' in sys.argv:
                mypy_package = importlib.util.find_spec("mypy")
                if settings.MYPY and mypy_package:
                    from .checks import mypy


def callback(sender: DjangoArtisan, **kwargs) -> None:
    from django.contrib.sites.models import Site
    try:
        current_site = Site.objects.get(id=settings.SITE_ID)
        if current_site.domain == "example.com":
            current_site.domain = settings.SITE_DOMAIN
            current_site.name = settings.SITE_NAME
            #current_site.id = settings.SITE_ID
            current_site.save()
        elif current_site.domain != settings.SITE_DOMAIN:
            raise exceptions.ImproperlyConfigured("SITE_ID does not match SITE_DOMAIN")
    except Site.DoesNotExist:
        Site.objects.create(domain=settings.SITE_DOMAIN,
                            name=settings.SITE_NAME, id=settings.SITE_ID)
