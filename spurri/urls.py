from django.conf.urls import include, url
from website.views import *
from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from website.serializers import router

admin.autodiscover()

from django.conf import settings
from updown.views import AddRatingFromModel
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from django.utils.decorators import available_attrs



import website.views
from functools import wraps



def cache_on_auth(timeout):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            return cache_page(timeout, key_prefix="_auth_%s_" % request.user.is_authenticated)(view_func)(request, *args, **kwargs)
        return _wrapped_view
    return decorator


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', website.views.index, name='index'),
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/$', website.views.profile, name='profile'),
    url(r'^like_button/$', AddRating.as_view(), name='like_button'),
    url(r'^create/$', login_required(ProjectCreate.as_view()), name="create"),
    url(r'^profile/(?P<slug>[^/]+)/$', UserProfileDetailView.as_view(), name="profile"),
    url(r'^list/$', ProjectListView.as_view()),
    url(r'^grants/$', GrantListView.as_view()),
    url(r'^cryptocurrency/$', RedirectView.as_view(url='/coins/', permanent=False), name='index'),
    url(r'^cryptocurrency/(?P<slug>[\w-]+)/$', cache_on_auth(60*60)(CryptocurrencyDetailView.as_view())),
    url(r'^coins/$', cache_on_auth(60*60)(CryptocurrencyListView.as_view())),

    url(r'^grant/(?P<pk>\d+)/$', GrantDetailView.as_view()),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    url(r"^project/(?P<object_id>\d+)/rate/(?P<score>[\d\-]+)$", login_required(AddRating.as_view()), name="project_rating"),
    url(r"^add_resource/$", login_required(AddResource.as_view()), name="add_resource"),
    url(r'^comments/posted/$', website.views.comment_posted, name='comment_posted'),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^fly_eye/$', FlyEyeView.as_view()),
    #url(r'^(?P<slug>[\w-]+)/$', CryptocurrencyDetailView.as_view()),
    url(r'^(?P<slug>[\w-]+)/$', ProjectDetailView.as_view(), name="project"),
    
    url(r'^emoji/', include('emoji.urls')),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ")),
    
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)