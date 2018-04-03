from threading import local
from rest_framework.response import Response
try:
    from django.contrib.auth import get_user_model
except ImportError:  # Django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
from django.contrib.auth import get_user
from .models import *
from django.core.exceptions import PermissionDenied
_user = local()
import logging
logger = logging.getLogger(__name__)
import memcache
from django.conf import settings


class Authorize(object):
    '''
    Multiple parameter pass in argument
    '''
    def __init__(self, argument=[]):
        if isinstance(argument, dict):
            self.group_name = argument.get('group')
            if not self.group_name:
                self.group_name =['Default']
            self.role_name = argument.get('role')
            if not self.role_name:
                self.role_name = False
        else:
            self.group_name = argument
            self.role_name = False

    def __call__(self, fn):
        ''' To check group level permissions
        if user belong to group present in predefined group of argument than he authorize user
        '''
        def check_permission(request):
            group_name = self.group_name
            role_name = self.role_name
            # here cache connections
            cache_location = settings.CACHES['default']['LOCATION']
            mc = memcache.Client([str(cache_location)])
            logger.info('Authorize Started.')
            if str(request.user) == 'AnonymousUser':
                request._cached_user = get_user(request)
                user_name = request._cached_user
            else:
                user_name = request.user
            user = User.objects.get(username=user_name).id or 0
            if group_name and role_name and user:
                # first user group check in memory cache if not present than check in database
                # here code for check user group in memory cache
                cache_group_role_name = mc.get(str(user)) or []
                if isinstance(cache_group_role_name, str):
                    cache_group_role_name = eval(cache_group_role_name)
                if (set(group_name) & set(cache_group_role_name)) and (set(role_name) & set(cache_group_role_name)):
                    logger.info('user are authorize')
                    return fn(request)
                else:
                    group_user_list = []
                    group_company_list = []
                    role_user_list = []
                    role_company_list = []
                    if group_name:
                        # find out user list of passing in argument of the group list and also check parent group
                        group_ids = [x.id for x in Group.objects.filter(name__in=group_name)]
                        if not group_ids:
                            # raise PermissionDenied
                            return Response({'Group is not present.'},status=403)
                        super_group_ids = []
                        for x in GroupPermissions.objects.filter(group__in=group_ids):
                            super_group_ids.append(x.super_group_id)
                            group_company_list.append(x.company_id)
                        if super_group_ids:
                            group_ids.extend(super_group_ids)
                        # To calculate total no of user in group list
                        group_user_list = [x.id for x in User.objects.filter(groups__in=group_ids)]
                    if role_name:
                        # find out user list of passing in argument of the role list
                        role_ids = []
                        for x in Role.objects.filter(name__in=role_name):
                            role_ids.append(x.id)
                            role_company_list.append(x.company_id)
                        if not role_ids:
                            return Response({'Roles is not present.'},status=403)
                        role_user_list = [x.user.id for x in UserRoles.objects.filter(role__in=role_ids)]

                    try:
                        user_company_id = UserRoles.objects.get(user=user).company.company_id
                    except:
                        return Response({'User company is not present.'}, status=403)
                    logger.info('Authorize Ended.')
                    # To check user are present in user list
                    if (user in group_user_list) and(user in role_user_list) and (user_company_id in group_company_list)\
                            and (user_company_id in role_company_list):
                        # To calculate current user group list
                        user_group_ids = [x.id for x in Group.objects.filter(user=user)]
                        super_user_group_ids = [x.group_id for x in
                                                GroupPermissions.objects.filter(super_group__in=user_group_ids)]
                        if super_user_group_ids:
                            user_group_ids.extend(super_user_group_ids)
                        user_group_name = [x.name for x in Group.objects.filter(id__in=user_group_ids)]
                        roles_ids = [x for x in UserRoles.objects.filter(user=user)]
                        user_role_name = [n.name for n in roles_ids[0].role.all()]
                        user_group_role_list = user_group_name + user_role_name
                        # User and group list store in memory cache for 300000 second timeperiod after the cache is clear
                        cache_response = mc.set(str(user), str(user_group_role_list), 300000)
                        logger.info('User group data store in cache')
                        return fn(request)
                    else:
                        raise PermissionDenied
            elif group_name and user:

                # first user group check in memory cache if not present than check in database
                # here code for check user group in memory cache
                cache_group_name = mc.get(str(user)) or []
                if isinstance(cache_group_name, str):
                    cache_group_name = eval(cache_group_name)
                if set(group_name) & set(cache_group_name):
                    logger.info('user are authorize')
                    return fn(request)
                else:
                    # find out user list of passing in argument of the group list and also check parent group
                    group_ids = [x.id for x in Group.objects.filter(name__in=group_name)]
                    super_group_ids = [x.super_group_id for x in GroupPermissions.objects.filter(group__in=group_ids)]
                    if super_group_ids:
                        group_ids.extend(super_group_ids)
                    # To calculate total no of user in group list
                    user_list = [x.id for x in User.objects.filter(groups__in=group_ids)]

                    logger.info('Authorize Ended.')
                    # To check user are present in user list
                    if user in user_list:
                        # To calculate current user group list
                        user_group_ids = [x.id for x in Group.objects.filter(user=user)]
                        super_user_group_ids = [x.group_id for x in
                                           GroupPermissions.objects.filter(super_group__in=user_group_ids)]
                        if super_user_group_ids:
                            user_group_ids.extend(super_user_group_ids)
                        user_group_name = [x.name for x in Group.objects.filter(id__in=user_group_ids)]
                        # User and group list store in memory cache for 300000 second timeperiod after the cache is clear
                        response = mc.set(str(user), str(user_group_name), 300000)
                        logger.info('User group data store in cache')
                        return fn(request)
                    else:
                        raise PermissionDenied
            else:
                return fn(request)
        return check_permission


