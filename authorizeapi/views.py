from .models import *
import logging
logger = logging.getLogger(__name__)


# Generic method to check user has assign any manager(super users)
# This method for manager can see under user records i.e access records
# def user_manger_recurse(user_list=[]):
#     logger.info('user_manger_recurse start')
#     user_manager_list=[]
#     for i in user_list:
#         super_user_list = SuperUser.objects.filter(super_user_id=i).values('user_id')
#         new_user_list = list(map(lambda x: x['user_id'],super_user_list))
#         if super_user_list:
#             user_manager_list.append(i)
#             user_manager_list.extend(user_manger_recurse(new_user_list))
#         else:
#             user_manager_list.append(i)
#     logger.info('user_manger_recurse end')
#     return user_manager_list


# Generic method to fetch user wise role and group, role wise user and group wise user list
def user_group_role_map(map_list={}):
    user_list = map_list.get('user',False)
    group_list = map_list.get('group',False)
    role_list = map_list.get('role',False)
    if user_list:
        # To calculate current user group list
        user_company_name = [x.company.company_id for x in UserRoles.objects.filter(user__in=user_list)]
        user_group_ids = [x.id for x in Group.objects.filter(user__in=user_list)]
        super_user_group_ids = [x.group_id for x in
                                GroupPermissions.objects.filter(super_group__in=user_group_ids)]
        if super_user_group_ids:
            user_group_ids.extend(super_user_group_ids)
        user_group_name = [x.name for x in Group.objects.filter(id__in=user_group_ids)]
        # To calculate current user Role list
        roles_ids = [x for x in UserRoles.objects.filter(user__in=user_list)]
        if roles_ids:
            user_role_name = [n.name for n in roles_ids[0].role.all()]
        else:
            user_role_name = []
        map_list.update({'user_group': user_group_name,'user_role':user_role_name,'user_company':user_company_name})
    if group_list:
        # find out user list of passing in argument of the group list and also check parent group
        group_ids = [x.id for x in Group.objects.filter(name__in=group_list)]
        super_group_ids,group_company_list = [],[]
        for x in GroupPermissions.objects.filter(group__in=group_ids):
            super_group_ids.append(x.super_group_id)
            group_company_list.append(x.company_id)
        if super_group_ids:
            group_ids.extend(super_group_ids)
        # To calculate total no of user in group list
        user_list = [x.id for x in User.objects.filter(groups__in=group_ids)]
        map_list.update({'group_user': user_list,'group_company':group_company_list})
    if role_list:
        # find out user list of passing in argument of the role list
        role_ids,role_company_list = [],[]
        for x in Role.objects.filter(name__in=role_list):
            role_ids.append(x.id)
            role_company_list.append(x.company_id)
        user_list = [x.user.id for x in UserRoles.objects.filter(role__in=role_ids)]
        map_list.update({'role_user': user_list,'role_company':role_company_list})
    return map_list