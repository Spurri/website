from django.conf.urls import include, url
from website.views import UserProfileDetailView, ProjectCreate, ProjectDetailView, AddRating, ProjectListView 
from django.contrib import admin
from django.contrib.auth.decorators import login_required
admin.autodiscover()

from django.conf import settings
from updown.views import AddRatingFromModel
from django.conf.urls.static import static

import website.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', website.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/$', website.views.profile, name='profile'),
    url(r'^like_button/$', AddRating.as_view(), name='like_button'),
    url(r'^create/$', login_required(ProjectCreate.as_view()), name="create"),
    url(r'^profile/(?P<slug>[^/]+)/$', UserProfileDetailView.as_view(), name="profile"),
    url(r'^list/$', ProjectListView.as_view()),
    url(r'^(?P<slug>[^/]+)/$', ProjectDetailView.as_view(), name="project"),
    url(r"^project/(?P<object_id>\d+)/rate/(?P<score>[\d\-]+)$", AddRating.as_view(), name="project_rating"),
    url(r'^comments/', include('django_comments.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)