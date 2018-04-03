from django.test import TestCase
from .permission import *
from .views import *
from .models import *
# Create your tests here.
import logging
logger = logging.getLogger(__name__)


class AuthorizeTestCase(TestCase):

    def setUp(self):
        logger.info('Authorize testing setup Started.')
        # create company records
        com1 = Company.objects.create(company_name="Merilent Inc")
        com2 = Company.objects.create(company_name="facebook Inc")

        # create group records
        group1 = Group.objects.create(name="Accounting")
        group2 = Group.objects.create(name="Operations")

        # create role records
        role1 = Role.objects.create(name="Reviewer", company=com1)
        role2 = Role.objects.create(name="Approver", company=com2)

        # group records assign company
        group_perm1 = GroupPermissions.objects.create(group=group1, company=com1)
        group_perm2 = GroupPermissions.objects.create(group=group2, company=com2)

        # create user records
        user1 = User.objects.create_superuser(username="sanket_reviewers", first_name="sanket", last_name="reviewers",
                            is_staff=True, is_active=True,email="ssawardekar@merilent.com",password="stavpay!23")
        user2 = User.objects.create_user(username="sanket_approvers", first_name="sanket", last_name="approvers",
                            is_staff=True, is_active=True, email="ssawardekar@merilent.com",password="stavpay!23")

        # user records assign groups
        user1.groups.add(group1)
        user2.groups.add(group2)

        # user records assign company
        user_role1 = UserRoles.objects.create(user=user1, company=com1)
        user_role2 = UserRoles.objects.create(user=user2, company=com2)

        # user records assign roles
        user_role1.role.add(role1)
        user_role2.role.add(role2)
        logger.info('Authorize testing setup Ended.')

    def test_authorize_api(self):
        # check Auhorize decorator method pass groups and role parameter
        response = Authorize({'group':['Accounting','Risk'],'role':['Approver']})
        logger.info('Authorize decorator response %s' % response)
        # check user group role map method to fetch user,group and role records
        data = user_group_role_map({'group': ['Accounting'], 'role': ['Approver'], 'user': [1]})
        logger.info('User Group Role Map Generic method response %s' % data)