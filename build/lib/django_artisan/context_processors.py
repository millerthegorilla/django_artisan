from typing import Any, Dict

from django import conf
from django import http

def navbarSpiel(request: http.HttpRequest) -> Dict[str, Any]:
    return {'navbarSpiel': conf.settings.NAVBAR_SPIEL}


def siteLogo(request: http.HttpRequest) -> Dict[str, Any]:
    return {'siteLogo': conf.settings.SITE_LOGO}

def base_html(request):
    return {'BASE_HTML': conf.settings.BASE_HTML}

def category_visible(request):
    return {'CATEGORY_VISIBLE': conf.settings.SHOW_CATEGORY}

def location_visible(request):
    return {'LOCATION_VISIBLE': conf.settings.SHOW_LOCATION}

def max_images(request):
    return {'MAX_IMAGES': conf.settings.MAX_USER_IMAGES}

