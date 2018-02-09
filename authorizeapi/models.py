from django.db import models
from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save
import memcache
from cxp.settings import CACHES
# Create your models here.


class SuperUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, related_name='SuperUser', on_delete=models.CASCADE)
    super_user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_super_user'

    def __str__(self):
        return self.user.username


# here when user has assign or remove group then user cache will updated
def set_user_cache(sender, instance, created,*args, **kwargs):
    cache_location = CACHES['default']['LOCATION']
    mc = memcache.Client([str(cache_location)])
    user = instance.id
    # To calculate current user group list
    user_group_ids = [x.id for x in Group.objects.filter(user=user)]
    super_user_group_ids = [x.group_id for x in
                            GroupPermissions.objects.filter(super_group__in=user_group_ids)]
    if super_user_group_ids:
        user_group_ids.extend(super_user_group_ids)
    user_group_name = [x.name for x in Group.objects.filter(id__in=user_group_ids)]
    # User and group list store in memory cache for 300000 second time period after the cache is clear
    if user_group_name:
        response = mc.set(str(user), str(user_group_name), 31449600)
    else:
        response = mc.delete(str(user))
    return response


# signals call to auth user table this function call at the end of the save() method.
post_save.connect(set_user_cache, sender=User)


class GroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.OneToOneField(Group, related_name='GroupPermissions', on_delete=models.CASCADE)
    super_group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_group_permissions'


# here when group has assign and remove super group then all memory cache will delete.
def set_group_cache(sender, instance, created,*args, **kwargs):
    cache_location = CACHES['default']['LOCATION']
    mc = memcache.Client([str(cache_location)])
    group_ids = instance.id
    # To check group has assign to super group then delete to all memory cache
    super_group_ids = [x.super_group_id for x in GroupPermissions.objects.filter(group=group_ids)][0]
    response = True
    if super_group_ids:
        response = mc.flush_all()
    return response


# signals call to auth group table this function call at the end of the save() method.
post_save.connect(set_group_cache, sender=Group)