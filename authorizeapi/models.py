from django.db import models
from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save
import memcache
from django.conf import settings
# Create your models here.


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'company'

    def __str__(self):
        return self.company_name


# class SuperUser(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.OneToOneField(User, related_name='SuperUser', on_delete=models.CASCADE)
#     super_user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'super_user'
#
#     def __str__(self):
#         return self.user.username
#
#
# # here when user has assign or remove group then user cache will updated
# def set_user_cache(sender, instance, created,*args, **kwargs):
#     cache_location = CACHES['default']['LOCATION']
#     mc = memcache.Client([str(cache_location)])
#     user = instance.id
#     # To calculate current user group list
#     user_group_ids = [x.id for x in Group.objects.filter(user=user)]
#     super_user_group_ids = [x.group_id for x in
#                             GroupPermissions.objects.filter(super_group__in=user_group_ids)]
#     if super_user_group_ids:
#         user_group_ids.extend(super_user_group_ids)
#     user_group_name = [x.name for x in Group.objects.filter(id__in=user_group_ids)]
#     # User and group list store in memory cache for 300000 second time period after the cache is clear
#     if user_group_name:
#         response = mc.set(str(user), str(user_group_name), 31449600)
#     else:
#         response = mc.delete(str(user))
#     return response
#
#
# # signals call to auth user table this function call at the end of the save() method.
# post_save.connect(set_user_cache, sender=User)


class GroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.OneToOneField(Group, related_name='GroupPermissions', on_delete=models.CASCADE)
    super_group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'group_permissions'


# here when group has assign and remove super group then all memory cache will delete.
def set_group_cache(sender, instance, created,*args, **kwargs):
    cache_location = settings.CACHES['default']['LOCATION']
    mc = memcache.Client([str(cache_location)])
    group_ids = instance.id
    # To check group has assign to super group then delete to all memory cache
    super_group_ids = [x.super_group_id for x in GroupPermissions.objects.filter(group=group_ids)]
    response = True
    if super_group_ids:
        response = mc.flush_all()
    return response


# signals call to auth group table this function call at the end of the save() method.
post_save.connect(set_group_cache, sender=Group)


class Designation(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'designation'
        # verbose_name_plural = 'designation'

    def __str__(self):
        return self.name


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'role'
        # verbose_name_plural = 'role'

    def __str__(self):
        return self.name


class UserRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ManyToManyField(Role)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    designation = models.ForeignKey(Designation, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'auth_user_roles'
        # verbose_name_plural = 'auth_user_roles'

        def __str__(self):
            return self.user.username


# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#        profile, created = UserRoles.objects.get_or_create(user=instance)
#
#
# post_save.connect(create_user_profile, sender=User)