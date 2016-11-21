from django.conf.urls import include, url
from website.views import UserProfileDetailView, ProjectCreate, GrantListView, GrantDetailView, ProjectDetailView, AddRating, ProjectListView 
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView

admin.autodiscover()

from django.conf import settings
from updown.views import AddRatingFromModel
from django.conf.urls.static import static

import website.views

urlpatterns = [
    url(r'^$', website.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/$', website.views.profile, name='profile'),
    url(r'^like_button/$', AddRating.as_view(), name='like_button'),
    url(r'^create/$', login_required(ProjectCreate.as_view()), name="create"),
    url(r'^profile/(?P<slug>[^/]+)/$', UserProfileDetailView.as_view(), name="profile"),
    url(r'^list/$', ProjectListView.as_view()),
    url(r'^grants/$', GrantListView.as_view()),
    url(r'^grant/(?P<pk>\d+)/$', GrantDetailView.as_view()),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    url(r"^project/(?P<id>\d+)/rate/(?P<score>[\d\-]+)$", login_required(AddRating.as_view()), name="project_rating"),
    url(r'^comments/posted/$', website.views.comment_posted, name='comment_posted'),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^(?P<slug>[^/]+)/$', ProjectDetailView.as_view(), name="project"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)