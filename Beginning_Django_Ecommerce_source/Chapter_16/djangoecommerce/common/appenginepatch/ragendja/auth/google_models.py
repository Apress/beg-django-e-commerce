from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from google.appengine.api import users
from google.appengine.ext import db
from ragendja.auth.models import EmailUserTraits

class GoogleUserTraits(EmailUserTraits):
    @classmethod
    def get_djangouser_for_user(cls, user):
        django_user = cls.all().filter('user =', user).get()
        if django_user:
            if getattr(settings, 'AUTH_ADMIN_USER_AS_SUPERUSER', True):
                is_admin = users.is_current_user_admin()
                if django_user.is_staff != is_admin or \
                        django_user.is_superuser != is_admin:
                    django_user.is_superuser = django_user.is_staff = is_admin
                    django_user.put()
        else:
            django_user = cls.create_djangouser_for_user(user)
            django_user.is_active = True
            if getattr(settings, 'AUTH_ADMIN_USER_AS_SUPERUSER', True) and \
                    users.is_current_user_admin():
                django_user.is_staff = True
                django_user.is_superuser = True
            django_user.put()
        return django_user

    class Meta:
        abstract = True

class User(GoogleUserTraits):
    """Extended User class that provides support for Google Accounts."""
    user = db.UserProperty(required=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def username(self):
        return self.user.nickname()

    @property
    def email(self):
        return self.user.email()

    @classmethod
    def create_djangouser_for_user(cls, user):
        return cls(user=user)
