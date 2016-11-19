from django.db import models
from django.contrib.auth.models import User
from updown.fields import RatingField
from tagging.registry import register
from tagging.fields import TagField
from django_comments import signals, models as comment_models
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from datetime import date

class Project(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    problem = models.TextField(null=True, blank=True)
    rating = RatingField(can_change_vote=True)
    tags = TagField()
    image = models.ImageField(upload_to="images")
    public_views = models.IntegerField(default=0)
    private_views = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    funding = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    goal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    paypal =models.EmailField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        return "/"+str(self.slug)

    def __unicode__(self):
        return self.name




class Team(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.project;


class Group(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name;


class Benefit(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name;


class Barrier(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name;


class Collaborator(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name;


class Organization(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="logos")
    website = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Grant(models.Model):
    organization = models.ForeignKey(Organization)
    soliciation_number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    comments = models.TextField()
    link = models.URLField()
    years = models.IntegerField(default=0)
    award_count = models.IntegerField(default=0)
    amount_max = models.DecimalField(max_digits=15, decimal_places=2)
    deadline = models.DateTimeField()
    tags = TagField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def is_past(self):
        if date.today() > self.deadline:
            return True
        return False


class Resource(models.Model):
    project = models.ForeignKey(Project)
    icon = models.CharField(max_length=200)
    link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True) 


def new_comment_notifier(sender, comment, request, *args, **kwargs):
    content_object = comment.content_object
    site = Site.objects.get_current()
    content_object = comment.content_object
    url = 'http://%s?c=%d' % (site.domain + content_object.get_absolute_url(), comment.id)
    subject = "New comment posted on '%s'" % str(content_object)
    message = "%s:\n%s" % (subject, url)
    #mail_admins(subject, message)
    send_mail(
        subject,
        message,
        'Spurri <no-reply@spurri.com>', 
        [content_object.user.email],
        fail_silently=False,
    ) 

signals.comment_was_posted.connect(new_comment_notifier, sender=comment_models.Comment)






