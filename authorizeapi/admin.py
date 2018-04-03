from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from .models import *

# class SuperUser(admin.StackedInline):
#     model = SuperUser
#     fk_name = 'user'
#     verbose_name_plural = 'User Manager'
#     can_delete = False

# Define a new User admin
# here user inherit superuser class
# class UserAdmin(BaseUserAdmin):
#     inlines = [SuperUser]
# Re-register UserAdmin

# Register your models here.
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


class GroupPermissionsInline(admin.StackedInline):
    model = GroupPermissions
    fk_name = 'group'
    verbose_name_plural = 'Group Permissions'
    can_delete = False


# Define a new Group admin
# here group inherit group permission class
class GroupAdmin(BaseGroupAdmin):
    inlines = [GroupPermissionsInline]
# Re-register GroupAdmin


# Register your models here.
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)


class UserRolesInline(admin.StackedInline):
    model = UserRoles
    verbose_name_plural = 'User Roles'
    can_delete = False

    fieldsets = (
        (None, {
            'fields': ('role', 'company','designation')}
    ),
)


# Define a new Role admin
# here role inherit user class
class UserRolesAdmin(BaseUserAdmin):
    inlines = [UserRolesInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_company','get_designation')

    # display user designation on list view
    def get_designation(self, instance):
        if instance.userroles.designation:
            return instance.userroles.designation.name
        else:
            return ''

    get_designation.short_description = 'Designation'

    # display user company details on list view
    def get_company(self, instance):
        if instance.userroles.company:
            return instance.userroles.company.company_name
        else:
            return ''

    get_company.short_description = 'Company'
# Re-register UserRolesAdmin


# Register your models here.
admin.site.register(Company)
admin.site.register(Designation)
admin.site.register(Role)
admin.site.unregister(User)
admin.site.register(User, UserRolesAdmin)