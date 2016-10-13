from django.core.management.base import NoArgsCommand
from ecomstore.cart import cart

class Command(NoArgsCommand):
    help = "Delete shopping cart items more than 90 days old"
    def handle_noargs(self, **options):
        cart.remove_old_cart_items()
