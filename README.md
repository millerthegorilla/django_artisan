# django_artisan
django_artisan is an app that provides a simple multi-tenanted website for ceramicists, artists, potters or any other artist's collective.  Each artist can upload three (current maximum) images of their work, and three of their images will be displayed, along with other artists work, in a random order on the landing page.  Each member can opt to display a personal page, which will show a brief description of themselves, and a slide show of their work.  The site has an 'about' page the text of which can be customised, and this can show events and lists the members, if they opt in.  Each member's personal page, can be reached without logging in, and so can be used as a simple brochure site to display their work and personal details, shop link etc.

## install
pip install git+https://github.com/millerthegorilla/django_artist.git#egg=django_artist
add django_artisan to your installed apps.
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'django_artisan',
]
```
## settings
You will need to set the site domain in the admin app, and also the settings.BASE_HTML for the statement `{% extends BASE_HTML %}` in the templates where BASE_HTML comes from the context_processor.
```python
BASE_HTML = 'django_artisan/base.html'
```

Post and Comments extend the message model which itself extends soft deletion model, so when either a post or a comment is deleted, it has a field set to true that reflects that it is deleted, and a schedule is created using django_q that then deletes the Post or Comment at a timedelta later.
```python
DELETION_TIMEOUT = {
        'POST':timezone.timedelta(days=21),
        'COMMENT':timezone.timedelta(days=14)
}
```
When a comment is created, an email is sent to subscribed users to inform them of the new comment.  This email is delayed from being sent, in case the user deletes the comment immediately, and so when the email schedule fires, the existence of the comment is checked.
```python
# the amount of time to wait before emails are sent to subscribed users
COMMENT_WAIT = timezone.timedelta(seconds=600)

# msg sent to subscribed users
# the msg must include one pair of brackets, which will contain
# the href of the post
SUBSCRIBED_MSG = "<h3 style='color: blue;'>Ceramic Isles</h3><br>A new comment has been added to a post that you are subscribed to!<br>Follow this link to view the post and comments: {}"
```
the following image upload settings are used:
```python
CONTENT_TYPES = ['image', 'video']
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 52428800
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 10485760
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o700
FILE_UPLOAD_PERMISSIONS = 0o644
```
django_q has the following settings:
```python
Q_CLUSTER = {
    'name': 'DJRedis',
    'workers': 4,
    'timeout': 20,
    'retry': 60,
    'django_redis': 'default'
}
```
with redis used as a cache:
```python
CACHES = {
     "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```
bleach is used to sanitize text in the message class underlying the Post and Comments.
```python
ALLOWED_TAGS = [
    'a', 'div', 'p', 'span', 'img', 'iframe', 'em', 'i', 'li', 'ol', 'ul', 'strong', 'br',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'table', 'tbody', 'thead', 'tr', 'td',
    'abbr', 'acronym', 'b', 'blockquote', 'code', 'strike', 'u', 'sup', 'sub',
]

STYLES = [
    'background-color', 'font-size', 'line-height', 'color', 'font-family'
]

ATTRIBUTES = {
    '*': ['style', 'align', 'title', ],
    'a': ['href', ],
    'iframe': ['src', 'height', 'width', 'allowfullscreen'],
}
```
TinyMCE is used to provide the editor for Posts...
```python
TINYMCE_DEFAULT_CONFIG = {
    "menubar": False,
    "min-height": "500px",
    "browser_spellcheck": True,
    "contextmenu": False,
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor | a11ycheck ltr rtl | showcomments addcomment table",
    "custom_undo_redo_levels": 10,
    "selector": 'textarea',
}

```
ElasticSearch is used to search the text of Posts and Comments.
```python
ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
}
```
Crispy-forms bootstrap5 has some settings...
```python
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```
You will also need recaptcha settings, which are part of django_profile.
```python
## RECAPTCHA SETTINGS
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
```
The keys shown here are the test keys that allow you to use the recaptcha in your development setup.  The silenced system check simply silences the warning that is displayed that says that the recaptcha keys are the test keys.

sorl-thumbnail is used for the avatar image, which defaults randomly to one of the default_avatars in the /media/default_avatars folder.  The default avatars should be numbered in the filename, as follows:
```python
default_avatar_n.jpg     # where n is a number from one to x.
```

Safe_imagefield is an app by moi, to validate images in a number of ways, including a virus scan.
```python
# safe imagefield
CLAMAV_SOCKET = str(os.getenv("CLAMAV_ADDRESS"))
```
django_artisan makes the underlying django_forum and django_profile models abstract in the following way:
```python
ABSTRACTPROFILE = True
ABSTRACTFORUMPROFILE = True
ABSTRACTMESSAGE = True
ABSTRACTPOST = True
POST_MODEL = 'django_artisan.Post'
```
django_artisan uses pipeline to compress css and javascript.  the settings are as follows:
```python
#django-pipeline
STATICFILES_STORAGE = 'pipeline.storage.PipelineManifestStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
   'PIPELINE_ENABLED': True,
    'JS_COMPRESSOR': 'pipeline.compressors.jsmin.JSMinCompressor',
    'CSS_COMPRESSOR': 'pipeline.compressors.csshtmljsminify.CssHtmlJsMinifyCompressor',
    'STYLESHEETS': {
        'main_styles': {
            'source_filenames': (
              'django_artisan/css/styles.css',
            ),
            'output_filename': 'css/styles_min.css',
        },
        'registration_styles': {
            'source_filenames': (
                'django_users/css/balloons.css',
            ),
            'output_filename': 'css/blns_min.css',
        },
        'carousel_styles': {
            'source_filenames': (
                'django_bs_carousel/css/styles.css',
            ),
            'output_filename': 'css/crsl_min.css',
        },
    },
    'JAVASCRIPT': {
        'django_bs_carousel': {
            'source_filenames': (
                'django_bs_carousel/js/carousel.js',
            ),
             'output_filename': 'django_bs_carousel/js/c_min.js',
        },
        'django_bs_image_loader': {
             'source_filenames': (
                'django_bs_carousel/js/imageLoader.js',
             ),
          'output_filename': 'django_bs_carousel/js/il_min.js',
        },
        'django_forum': {
            'source_filenames': (
                'django_forum/js/*.js',
             ),
             'output_filename': 'js/df_min.js',
        },
        'django_artisan': {
            'source_filenames': (
                'django_artisan/js/profileUpdate.js',
            ),
            'output_filename': 'js/da_min.js',
        }
    }
}

```
the following settings are used to redirect users on login/logout
```python
LOGIN_REDIRECT_URL = reverse_lazy('django_artisan:post_list_view')
LOGOUT_REDIRECT_URL = reverse_lazy('django_artisan:landing_page')
LOGIN_URL = reverse_lazy('login')
```
django_artisan uses sorl-thumbnail
```python
# sorl-thumbnail
THUMBNAIL_SIZE = (120,120)
# THUMBNAIL_DEBUG = True
MAX_USER_IMAGES = 3
```
django_bs_carousel is included, an app by me that loads images asynchronously, and displays them
in random order on the landing page of the site and on the personal page of a user.
```python
IMAGE_SIZE_LARGE = "1024x768"
IMAGE_SIZE_SMALL = "360x640"

NUM_IMAGES_PER_REQUEST = 5

CAROUSEL_RANDOMIZE_IMAGES = True
CAROUSEL_USE_CACHE = False
CAROUSEL_OFFSET = True
CAROUSEL_IMG_PAUSE = 6500
DJANGO_BS_CAROUSEL_IMAGE_MODEL = "django_artisan.UserProductImage"
```
a message sent to subscribed users each time a new comment is added to a post.
```python
# msg sent to subscribed users
# the msg must include one pair of brackets, which will contain
# the href of the post
SUBSCRIBED_MSG = "<h3 style='color: blue;'>Ceramic Isles</h3><br>A new comment has been added to a post that you are subscribed to!<br>Follow this link to view the post and comments: {}"

```
Some of the text of the website can be set in the settings...
```python
### ABOUT PAGE
ABOUT_US_SPIEL = "<span class='spiel-headline'>Ceramic Isles</span> <span class='spiel-normal'>as a website is presented \
                  on behalf of ceramicists, sculptors, potters \
                  and anyone else who likes to work with clay, \
                  in the Channel Islands.</span>"

### NAVBAR
NAVBAR_SPIEL = "Welcome to Ceramic Isles, a site where ceramic artists \
                local to the Channel Islands are able to meet, chat, and show off their work. \
                If you are a ceramic artist local to one of the Channel Islands, consider \
                registering as a user to be able to access the forum, \
                and to be able present images of your work here, on this page.<br> \
                Click the Ceramic Isles Logo to return to the landing page \
                which acts as a gallery for member's work.<br> \
                On a diet???  This site is cookie free!<br> \
                Problems??? contact - ceramic_isles [at] gmail.com"

```
the site_name, site_logo and site_domain are used by the code.  Obtaining the site domain from the sites framework was really slow so I used settings.SITE_DOMAIN instead.
```python
### The following are used by django_artisan and django_forum
SITE_NAME = str(os.getenv("SITE_NAME"))
SITE_LOGO = 'django_artisan/images/vase.svg'
SITE_DOMAIN = '127.0.0.1:8000'
#for the sites framework so that sitemaps will work
SITE_ID = 1
```
Each post has a category and a location choices field, with drop down that is searchable.  Because I can't make models dynamic, the class CATEGORY, and class LOCATION below must be defined, but you can hide them from view by changing either SHOW_CATEGORY or SHOW_LOCATION to False.
```python
# category and location
SHOW_CATEGORY = True
SHOW_LOCATION = True
from django.db import models
from django.utils.translation import gettext_lazy as _
class CATEGORY(models.TextChoices):
    EVENT = 'EV', _('Event')
    QUESTION = 'QN', _('Question')
    GENERAL = 'GL', _('General')
    PICTURES = 'PS', _('Pictures')
    FORSALE = 'FS', _('For Sale')

class LOCATION(models.TextChoices):
    ANY_ISLE = 'AI', _('Any')
    ALDERNEY = 'AY', _('Alderney')
    GUERNSEY = 'GY', _('Guernsey')
    JERSEY = 'JE', _('Jersey')
    SARK = 'SK', _('Sark')
```
see the file settings.py in this directory for an example settings.py file.

## dependencies
The long list of dependencies are not automatically installed by this package.  Instead, I use [artisan_scripts](https://github.com/millerthegorilla/artisan_scripts) to provision the site using podman.  This has a requirements.txt file which you can find [here](https://raw.githubusercontent.com/millerthegorilla/artisan_scripts/main/dockerfiles/pip_requirements_dev) in the case of running the dev site or [here](https://raw.githubusercontent.com/millerthegorilla/artisan_scripts/main/dockerfiles/pip_requirements_prod) in the case of running the site in production mode.

Of course, I reccomend that you use artisan_scripts, but you can install django_artisan in a pipenv, and use pip install to install the requirements.txt if you prefer.

git+https://github.com/millerthegorilla/django_forum.git#egg=django_forum # this pulls in django_profile, django_messages, django_users and safe_imagefield,  all apps made by myself
asgiref==3.3.3
bleach==3.3.0
certifi==2020.12.5
clamd==1.0.2
Django==3.2.9
django-crispy-forms==1.11.2
django-elasticsearch-dsl==7.1.4
django-email-verification==0.1.0
django-password-validators==1.4.0
django-recaptcha==2.0.6
django-tinymce==3.3.0
django-debug-toolbar==3.2.1
elasticsearch==7.12.0
elasticsearch-dsl==7.3.0
ffmpeg==1.4
fuzzywuzzy==0.18.0
gunicorn==20.1.0
mysqlclient==2.0.3
packaging==20.9
Pillow==8.2.0
pyparsing==2.4.7
pytest==7.0.1
python-dateutil==2.8.1
python-dotenv==0.17.0
python-Levenshtein==0.12.2
python-magic==0.4.25
django-redis==4.12.1
pytz==2021.1
six==1.15.0
sorl-thumbnail==12.7.0
sqlparse==0.4.1
urllib3==1.26.4
webencodings==0.5.1
random_username==1.0.2
django-extensions==3.1.3
pygraphviz==1.7
crispy_bootstrap5
django-q==1.3.8
django-dbbackup==3.3.0
dropbox==11.12.0
mypy==0.910
django-stubs==1.9.0
ipython==7.29.0
# django-pipeline==2.0.7
git+https://github.com/millerthegorilla/django-pipeline.git@main
jsmin==3.0.0
faker==11.1.0
css_html_js_minify==2.5.5