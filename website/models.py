from django.db import models
from django.contrib.auth.models import User
from updown.fields import RatingField
from tagging.registry import register
from tagging.fields import TagField
from django_comments import signals, models as comment_models
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from datetime import date
from django.contrib.humanize.templatetags.humanize import intcomma


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, default="-")
    symbol = models.CharField(max_length=200)
    description = models.TextField()
    market_cap_usd = models.DecimalField(max_digits=21, decimal_places=0, default=0)
    chart_24h = models.TextField()
    price_usd = models.DecimalField(max_digits=21, decimal_places=12, default=0)
    price_btc = models.DecimalField(max_digits=21, decimal_places=9, default=0)
    available_supply = models.DecimalField(max_digits=21, decimal_places=0, default=0)
    total_supply = models.DecimalField(max_digits=21, decimal_places=2, default=0)
    max_supply = models.DecimalField(max_digits=21, decimal_places=2, default=0)
    volume_usd_24h = models.DecimalField(max_digits=21, decimal_places=8, default=0)
    percent_change_1h = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    percent_change_24h = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    percent_change_7d = models.DecimalField(max_digits=6, decimal_places=2, default=0) 
    last_updated = models.DateTimeField()
    donation_count = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    donation_total = models.DecimalField(max_digits=21, decimal_places=0, default=0)
    donation_wallet = models.TextField()
    percent_locked = models.DecimalField(max_digits=4, decimal_places=2, default=0) 
    masternode_count = models.IntegerField(default=0)
    masternode_cost_coins = models.DecimalField(max_digits=21, decimal_places=0, default=0)
    masternode_cost_dollars = models.DecimalField(max_digits=21, decimal_places=2, default=0)
    masternode_roi_days = models.IntegerField(default=0)
    masternode_coins_daily = models.DecimalField(max_digits=21, decimal_places=2, default=0)
    masternode_roi_yearly_percent = models.DecimalField(max_digits=21, decimal_places=2, default=0) 
    masternode_dollars_daily = models.DecimalField(max_digits=21, decimal_places=2, default=0)
    masternode_dollars_weekly = models.DecimalField(max_digits=21, decimal_places=2, default=0)
    masternode_dollars_monthly = models.DecimalField(max_digits=21, decimal_places=2, default=0)
    masternode_dollars_yearly = models.DecimalField(max_digits=21, decimal_places=2, default=0)
    algorithm = models.CharField(max_length=200)
    block_count = models.IntegerField(default=0)
    block_time_seconds = models.IntegerField(default=0)
    proof_type = models.CharField(max_length=200)
    pool1 = models.URLField(blank=True, null=True)
    pool2 = models.URLField(blank=True, null=True)
    pool3 = models.URLField(blank=True, null=True)
    emoji = models.URLField(blank=True, null=True)
    exchange1 = models.URLField(blank=True, null=True)
    exchange2 = models.URLField(blank=True, null=True)
    exchange3 = models.URLField(blank=True, null=True)
    social1 = models.URLField(blank=True, null=True)
    social2 = models.URLField(blank=True, null=True)
    social3 = models.URLField(blank=True, null=True)
    block_explorer = models.URLField(blank=True, null=True)
    block_explorer_balance_api = models.URLField(blank=True, null=True)
    block_explorer_balance_url = models.URLField(blank=True, null=True)
    block_explorer_balance_in_satoshis = models.BooleanField(default=False)
    source_code = models.URLField(blank=True, null=True)
    issue_count = models.IntegerField(default=0)
    #dob = models.DateTimeField()
    website = models.URLField(blank=True, null=True)
    logo_image = models.ImageField(upload_to="logos", blank=True, null=True)
    tags = TagField()
    logo_word = models.ImageField(upload_to="words", blank=True, null=True)
    website_screenshot = models.ImageField(upload_to="website_screenshots", blank=True, null=True)
    paper_wallet = models.URLField(blank=True, null=True)
    white_paper = models.URLField(blank=True, null=True)
    multi_wallet = models.URLField(blank=True, null=True)
    mobile_wallet = models.URLField(blank=True, null=True)
    related_to = models.CharField(max_length=200, blank=True, null=True)
    windows_wallet = models.URLField(blank=True, null=True)
    mac_wallet = models.URLField(blank=True, null=True)
    linux_wallet = models.URLField(blank=True, null=True)
    forum = models.URLField(blank=True, null=True)
    chat = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-market_cap_usd',]

    def get_absolute_url(self):
        return "/"+str(self.slug)

    def __str__(self):
        return self.name
    
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Cryptocurrency._meta.fields]

    def render_price_usd(self):
        if self.price_usd > 1:
            return "$" + intcomma("{0:.2f}".format(self.price_usd))
        else:
            return "$" + intcomma(self.price_usd.normalize())


    def render_tags(self):
        string = ""
        if "masternode" in self.tags:
            string = string + '<a href="/coins/?tags__contains=masternode" style="color:black;"><icon class="far fa-hdd" title="Masternode"></icon></a>'
        if "PoS" in self.tags:
            string = string + '<a href="/coins/?tags__contains=PoS" style="color:black;"><icon class="fa fa-map-pin" title="Proof of Stake"></icon></a>'
        if "PoW" in self.tags:
            string = string + '<a href="/coins/?tags__contains=PoW" style="color:black;"><icon class="far fa-gem" title="Proof of Work"></icon></a>'
        return string


class Goal(models.Model):
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=21, decimal_places=9, default=0)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    current_amount = models.DecimalField(max_digits=21, decimal_places=9, default=0)
    target_cryptocurrency = models.ForeignKey(Cryptocurrency, related_name="target_cryptocurrency", blank=True, null=True, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default=None, blank=True, null=True)
    result = models.CharField(max_length=255, blank=True, null=True)
    contribution_count = models.IntegerField(default=0)
    updated = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['status','-number']


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.name


class Team(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project;


class Group(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name;


class Benefit(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name;


class Barrier(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name;


class Collaborator(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name;


class Organization(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="logos")
    website = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Grant(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
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
    corpus = models.TextField(default=" ")

    def __str__(self):
        return self.name

    def is_past(self):
        if date.today() > self.deadline.date():
            return True
        return False


class Resource(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    icon = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True) 


class Match(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE)
    similarity = models.FloatField()
    score = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = (("project", "grant"),)

    


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






