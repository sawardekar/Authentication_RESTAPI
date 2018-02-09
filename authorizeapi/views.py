# from django.shortcuts import render
from .models import *
import logging
logger = logging.getLogger(__name__)


# Generic method to check user has assign any manager(super users)
# This method for manager can see under user records i.e access records
def user_manger_recurse(user_list=[]):
    logger.info('user_manger_recurse start')
    user_manager_list=[]
    for i in user_list:
        super_user_list = SuperUser.objects.filter(super_user_id=i).values('user_id')
        new_user_list = list(map(lambda x: x['user_id'],super_user_list))
        if super_user_list:
            user_manager_list.append(i)
            user_manager_list.extend(user_manger_recurse(new_user_list))
        else:
            user_manager_list.append(i)
    logger.info('user_manger_recurse end')
    return user_manager_list