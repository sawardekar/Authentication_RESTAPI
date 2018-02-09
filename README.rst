Django Custom Authorization and Memcache Implementation

The Django custom Authorization is based on django groups. This authorization applied to API controller.
Suppose specific API access to specific group of the user then you can refer to this packages.
Django cache data store in default RAM memory using MemcachedCache. Bydefault he store entire webpage
but in that only store user specific information those required in API Authentication.

Below step for installation and configuration:
1>First download authorizeapi package form git repository.
Git URl: https://github.com/Merilent/Django-Authorization.git
Install package on the terminal using command:
pip install django-authorizeapi-1.0.tar.gz [also mention downloaded folder path]

2>Now changes in default setting py:
INSTALLED_APPS = [
‘authorizeapi’    add package name
]
MIDDLEWARE = [
# 'django.middleware.csrf.CsrfViewMiddleware',    Comment out this package
]
    #  Here Memcached Cache configurations
    CACHE_MIDDLEWARE_SECONDS = 31449600 # (approximately 1 year, in seconds)
   CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
    SESSION_CACHE_ALIAS = "default"

3> Install required packages:
    pip install python-memcached

4>when you run your project before makemigrations authorizeapi and then migrate project.
Below makemigrations command:
python manage.py makemigrations authorizeapi

5>Now applied Authorization decorator method on any API controller method:
Below the example of read API applied on authorization decorator:
from authorizeapi.permission import Authorize    Importing Authorize packages
@api_view(['GET'])
@Authorize(['Admin'])   'Admin' as Group Name, Now you can assign multiple group names.
def read(request):
        .....
        return HttpResponse()

6>Before test your code, First Create group and assign to users.

7> In group you can add super group means super group can access child group permission.
