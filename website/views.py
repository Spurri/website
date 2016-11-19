from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, CreateView, View, ListView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render_to_response, RequestContext
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib import messages
from website.models import Project, Team, Grant
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from updown.views import AddRatingFromModel
import json
from django_comments.models import Comment
from datetime import date


def comment_posted( request ):
    if request.GET['c']:
        comment_id = request.GET['c'] 
        comment = Comment.objects.get( pk=comment_id )
        project = Project.objects.get(id=comment.object_pk) 

        if project:
            messages.success(request, 'Comment Posted!')
            return HttpResponseRedirect( project.get_absolute_url() )

    return HttpResponseRedirect( "/" )

def index(request, template="index.html"):
    projects = Project.objects.all().order_by('-order')
    context = {
        'project_count': projects.count(),
        'projects': projects[0:15],
        'user_count': User.objects.all().count(),
        'grant_count': Grant.objects.all().count(),
    }
    return render_to_response(template, context, context_instance=RequestContext(request))

class ProjectListView(ListView):
    model = Project
    queryset = Project.objects.order_by('-order')      
    template_name = 'list.html'  
    context_object_name = "projects"    
    paginate_by = 21 

class GrantListView(ListView):
    model = Grant
    dayofyear = int(date.today().strftime("%j"))

    datediff = '(DAYOFYEAR(date) - %d + 365) MOD 365' % (
          dayofyear
        )
    queryset = Grant.objects.extra(select={'datediff': datediff}).order_by('datediff')
    template_name = 'grants.html'  
    context_object_name = "grants"    
    paginate_by = 100 

def profile(request):
    try:
        return redirect('/profile/' + request.user.username)
    except Exception:
        return redirect('/')

class AddRating(View):
  
    def post(self, request, *args, **kwargs):
        params = {
            'app_label': 'website',
            'model': 'project',
            'field_name': 'rating'
        }
        params.update(kwargs)
        response = AddRatingFromModel()(request, **params)
        print response 
        if response.status_code == 200:

            return HttpResponse(Project.objects.get(id=kwargs['object_id']).rating.likes)
        return HttpResponse(json.dumps({'error': 9, 'message': response.content}))
  
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            messages.error(self.request, 'That user was not found.')
            return redirect("/")
        return super(UserProfileDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        return user

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        return context



class ProjectDetailView(DetailView):
    model = Project
    slug_field = "slug"
    template_name = "project.html"

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
           return HttpResponseNotFound('<h1>Page not found</h1>')
        if request.user.is_authenticated():
            self.object.private_views = self.object.private_views + 1
        else:
            self.object.public_views = self.object.public_views + 1
        self.object.save()
        return super(ProjectDetailView, self).get(request, *args, **kwargs)



class ProjectCreate(CreateView):
    model = Project
    fields = ['name','description','image','slug']
    template_name = "add_project.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        messages.success(self.request, 'Project added!')
        return HttpResponseRedirect("/"+obj.slug) 

    # def get_context_data(self, **kwargs):
    #     context = super(ProjectCreate, self).get_context_data(**kwargs)
    #     return context