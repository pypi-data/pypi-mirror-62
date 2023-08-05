#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_security.generations main module

"""

from zope.lifecycleevent import ObjectCreatedEvent
from zope.principalannotation.interfaces import IPrincipalAnnotationUtility
from zope.principalannotation.utility import PrincipalAnnotationUtility

from pyams_security.interfaces import ADMIN_USER_LOGIN, ADMIN_USER_NAME, INTERNAL_USER_LOGIN, \
    INTERNAL_USER_NAME, ISecurityManager, SYSTEM_PREFIX
from pyams_security.plugin.admin import AdminAuthenticationPlugin
from pyams_security.utility import SecurityManager
from pyams_site.interfaces import ISiteGenerations
from pyams_site.generations import check_required_utilities
from pyams_utils.registry import get_current_registry, utility_config


__docformat__ = 'restructuredtext'


RENAMED_CLASSES = {
    'pyams_security.interfaces ISocialUsersFolderPlugin':
        'pyams_security.interfaces IOAuthUsersFolderPlugin',
    'pyams_security.interfaces ISocialUser':
        'pyams_security.interfaces IOAuthUser',
    'pyams_security.interfaces ISocialLoginProviderInfo':
        'pyams_security.interfaces IOAuthLoginProviderInfo',
    'pyams_security.interfaces ISocialLoginConfiguration':
        'pyams_security.interfaces IOAuthLoginConfiguration',
    'pyams_security.interfaces ISocialLoginProviderConnection':
        'pyams_security.interfaces IOAuthLoginProviderConnection',
    'pyams_security.plugin.social SocialUser':
        'pyams_security.plugin.oauth OAuthUser',
    'pyams_security.plugin.social SocialUsersFolder':
        'pyams_security.plugin.oauth OAuthUsersFolder',
    'pyams_security.plugin.social SocialLoginProviderInfo':
        'pyams_security.plugin.social OAuthLoginProviderInfo',
    'pyams_security.plugin.social SocialLoginConfiguration':
        'pyams_security.plugin.oauth OAuthLoginConfiguration',
    'pyams_security.plugin.social SocialLoginProviderConnection':
        'pyams_security.plugin.oauth OAuthLoginProviderConnection'
}


REQUIRED_UTILITIES = (
    (ISecurityManager, '', SecurityManager, 'Security manager'),
    (IPrincipalAnnotationUtility, '', PrincipalAnnotationUtility, 'User profiles')
)


def get_admin_user():
    """Get system manager profile"""
    admin_auth = AdminAuthenticationPlugin()
    admin_auth.prefix = SYSTEM_PREFIX
    admin_auth.title = 'System manager authentication'
    admin_auth.login = ADMIN_USER_LOGIN
    admin_auth.password = 'admin'
    return admin_auth


def get_service_user():
    """Get internal services profile"""
    service_auth = AdminAuthenticationPlugin()
    service_auth.prefix = SYSTEM_PREFIX
    service_auth.title = 'internal service'
    service_auth.login = INTERNAL_USER_LOGIN
    service_auth.password = None
    return service_auth


@utility_config(name='PyAMS security', provides=ISiteGenerations)
class SecurityGenerationsChecker:
    """I18n generations checker"""

    order = 50
    generation = 1

    def evolve(self, site, current=None):  # pylint: disable=no-self-use,unused-argument
        """Check for required utilities"""
        check_required_utilities(site, REQUIRED_UTILITIES)
        manager = site.getSiteManager().queryUtility(ISecurityManager)
        if manager is not None:
            if ADMIN_USER_NAME not in manager:
                admin_auth = get_admin_user()
                get_current_registry().notify(ObjectCreatedEvent(admin_auth))
                manager[ADMIN_USER_NAME] = admin_auth
            if INTERNAL_USER_NAME not in manager:
                service_auth = get_service_user()
                get_current_registry().notify(ObjectCreatedEvent(service_auth))
                manager[INTERNAL_USER_NAME] = service_auth
