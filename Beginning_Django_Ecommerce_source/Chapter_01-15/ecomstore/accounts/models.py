from django.db import models
from django.contrib.auth.models import User
from ecomstore.checkout.models import BaseOrderInfo

class UserProfile(BaseOrderInfo):
    """ stores customer order information used with the last order placed; can be attached to the checkout order form
    as a convenience to registered customers who have placed an order in the past.
    
    """
    user = models.ForeignKey(User, unique=True)
    
    def __unicode__(self):
        return 'User Profile for: ' + self.user.username