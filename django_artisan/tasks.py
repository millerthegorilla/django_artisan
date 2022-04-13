import logging

from django.contrib import sitemaps

logger = logging.getLogger('django_artisan')

"""
    pings_google to recrawl site when user opts to list on about page
    or to display personal page
"""
def ping_google_func() -> None:
    try:
        sitemaps.ping_google()
        logger.info("Pinged Google!")
    except Exception as e:
        logger.error("unable to ping_google : {0}".format(e))