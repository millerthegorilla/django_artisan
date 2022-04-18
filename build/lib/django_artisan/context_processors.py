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

def image_exts(request):
    ae = conf.settings.ALLOWED_EXTENSIONS
    return {'ALLOWED_EXTENSIONS': ' '.join(
        map(lambda x: x+',' if x not in (ae[-1],ae[-2]) else x if x is ae[-2] else 'or '+x, ae)
    )}

def max_upload_size(request):
    return {'MAX_UPLOAD_SIZE': conf.settings.MAX_UPLOAD_SIZE}

