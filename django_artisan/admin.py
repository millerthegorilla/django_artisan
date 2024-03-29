import logging

from django import apps, conf, http
from django.contrib import admin, messages
from django.core import exceptions, management
from django.utils import translation, log
from django.db import models

from django_password_validators.password_history.models import PasswordHistory

from django_forum.models import ForumProfile
from .models import UserProductImage, Event, ArtisanForumProfile


logger = logging.getLogger('django_artisan')

# from django.contrib.admin.helpers import ActionForm
# from django import forms


# class XForm(ActionForm):
#     _pack_choice = forms.FloatField(max_value=100, min_value=0, required=False)

# @admin.register(UserProductImage)
# class ConsignmentAdmin(admin.ModelAdmin):

#     action_form = XForm
#     actions = ['change_status']

#     def change_status(modeladmin, request, queryset):
#         print(request.POST['_pack_choice'])
#         for obj in queryset:
#             print(obj)
#     change_status.short_description = "Change status according to the field"

class DjangoArtisan(apps.AppConfig):
    name = 'django_artisan'

    def ready(self) -> None:
        models.signals.post_migrate.connect(callback, sender=self)

def callback(sender: DjangoArtisan, **kwargs) -> None:
    from django.contrib.sites.models import Site
    try:
        current_site = Site.objects.get(id=conf.settings.SITE_ID)
        if current_site.domain != conf.settings.SITE_DOMAIN:
            raise exceptions.ImproperlyConfigured("SITE_ID does not match SITE_DOMAIN")
    except Site.DoesNotExist:
        logger.info("Creating Site Model with domain={0}, name={1}, id={2}".format(
            conf.settings.SITE_DOMAIN, conf.settings.SITE_NAME, conf.settings.SITE_ID))
        Site.objects.create(domain=conf.settings.SITE_DOMAIN,
                            name=conf.settings.SITE_NAME, id=conf.settings.SITE_ID)


@admin.register(UserProductImage)
class Image(admin.ModelAdmin):
    list_display = (
        'active', 'file',
        'shop_link',
        'shop_link_title',
        'title', 'text',
    )
    list_filter = (
        'active', 'file',
        'title'
    )
    search_fields = (
        'text', 'title',
        'shop_link'
    )
    actions = ['approve_image']

    def approve_image(self, request: http.HttpRequest, queryset: models.QuerySet) -> None:
        updated = queryset.update(active=True)
        self.message_user(
            request,
            translation.ngettext(
                '%d image was approved.',
                '%d images were approved.',
                updated,
            ) % updated,
            messages.SUCCESS
        )


@admin.register(Event)
class Event(admin.ModelAdmin):
    list_display = (
        'active', 'title',
        'text', 'date',
        'repeating'
    )
    actions = ['approve_event', 'disapprove_event']

    def approve_event(self, request: http.HttpRequest, queryset: models.QuerySet) -> None:
        updated = queryset.update(active=True)
        self.message_user(
            request,
            translation.ngettext(
                '%d event was approved.',
                '%d events were approved.',
                updated,
            ) % updated,
            messages.SUCCESS
        )

    def disapprove_event(self, request: http.HttpRequest, queryset: models.QuerySet) -> None:
        updated = queryset.update(active=False)
        self.message_user(
            request,
            translation.ngettext(
                '%d event was disapproved.',
                '%d events were disapproved.',
                updated,
            ) % updated,
            messages.SUCCESS
        )


# #admin.site.unregister(UserPasswordHistoryConfig)
admin.site.unregister(PasswordHistory)

try:
    abs_forum_profile = conf.settings.ABSTRACTFORUMPROFILE
except AttributeError:
    abs_forum_profile = False
if not abs_forum_profile:
    admin.site.unregister(ForumProfile)

# Register your models here.


@admin.register(ArtisanForumProfile)
class ArtisanForumProfile(admin.ModelAdmin):
    list_display = [
        'display_name', 'bio',
        'image_file', 'shop_web_address',
        'outlets', 'listed_member',
        'display_personal_page', 'address_line_1',
        'address_line_2', 'city', 'country',
        'postcode', 'avatar',
        'rules_agreed'
    ]
    list_filter = [
        'display_name', 'city', 'country',
        'rules_agreed', 'shop_web_address',
        'listed_member', 'display_personal_page'
    ]
    search_fields = [
        'display_name', 'address_line_1',
        'city', 'country', 'bio'
    ]

    def get_queryset(self, request: http.HttpRequest) -> models.QuerySet:
        return super().get_queryset(request).exclude(profile_user__is_superuser=True)
