from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from .models import SuperUser, GroupPermissions


class SuperUser(admin.StackedInline):
    model = SuperUser
    fk_name = 'user'
    verbose_name_plural = 'User Manager'
    can_delete = False


class GroupPermissions(admin.StackedInline):
    model = GroupPermissions
    fk_name = 'group'
    verbose_name_plural = 'Group Permissions'
    can_delete = False


# Define a new User admin
# here user inherit superuser class
class UserAdmin(BaseUserAdmin):
    inlines = [SuperUser]
# Re-register UserAdmin


# Define a new Group admin
# here group inherit group permission class
class GroupAdmin(BaseGroupAdmin):
    inlines = [GroupPermissions]
# Re-register GroupAdmin


# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

