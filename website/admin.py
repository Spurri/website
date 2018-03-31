from django.contrib import admin

from website.models import Project, Team, Group, Benefit, Barrier, Collaborator, Grant, Organization, Resource, Match, Cryptocurrency, Goal
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from tagging.models import Tag

class GroupAdmin(admin.ModelAdmin):
    list_display = ('project','name')

class GoalAdmin(admin.ModelAdmin):
    list_display = ('id','cryptocurrency','number','title','description','target_cryptocurrency','current_amount','target_amount','wallet_address','status','result','contribution_count','updated','created','modified')




class BenefitAdmin(admin.ModelAdmin):
    list_display = ('project','name')

class BarrierAdmin(admin.ModelAdmin):
    list_display = ('project','name')

class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ('project','name')


class GroupInline(admin.TabularInline):
    model = Group

class BenefitInline(admin.TabularInline):
    model = Benefit

class BarrierInline(admin.TabularInline):
    model = Barrier

class CollaboratorInline(admin.TabularInline):
    model = Collaborator


class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ('name','slug','description','forum','masternode_cost_coins','tags','created','modified')
    search_fields = ('name', 'description','tags')
    list_editable = ( 'forum', 'tags', 'masternode_cost_coins')
    list_per_page = 500

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','slug','description','created','tags','rating_likes','public_views','private_views','funding','goal','paypal','created','modified')
    inlines = [
        GroupInline,
        BenefitInline,
        BarrierInline,
        CollaboratorInline,
    ]
    search_fields = ('name', 'description','tags')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('project','user','role','created','modified')

class GrantAdmin(admin.ModelAdmin):
    list_display = ('organization','soliciation_number','name','tags','comments','link','years','award_count','amount_max','deadline','modified')
    search_fields = ('soliciation_number', 'name')

class MatchAdmin(admin.ModelAdmin):
    list_display = ('project','grant','similarity','score','created','modified')


admin.site.unregister(User)
UserAdmin.list_display = ('id','username','email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')


admin.site.register(User, UserAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(Organization)
admin.site.register(Resource)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Cryptocurrency, CryptocurrencyAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Benefit, BenefitAdmin)
admin.site.register(Barrier, BarrierAdmin)
admin.site.register(Collaborator, CollaboratorAdmin)
admin.site.register(Match, MatchAdmin)