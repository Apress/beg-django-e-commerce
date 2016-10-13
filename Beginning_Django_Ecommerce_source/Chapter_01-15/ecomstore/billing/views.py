from django.shortcuts import render_to_response
from django.core import serializers
from django.utils import simplejson
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from ecomstore.billing.forms import CardForm
#from ecomstore.billing import passkey

@login_required
def add_card(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        # convert the POST variables into JSON format
        post_data.__delitem__('csrfmiddlewaretoken')
        json_data = simplejson.dumps(post_data)
        # encrypt the JSON
        encrypted_json = passkey.encrypt(json_data)
        # retrieve the encrypted JSON
        #decrypted_json = passkey.decrypt(encrypted_json)
        # convert the decrypted JSON into a dictionary
        #decrypted_data = simplejson.loads(decrypted_json)
        
        # store the newly encrypted data as a Card instance
        form = CardForm(post_data)
        card = form.save(commit=False)
        card.user = request.user
        card.num = post_data.get('card_number')[-4:]
        #card.data = encrypted_json
        card.save()
    else:
        form = CardForm()
    return render_to_response("billing/add_card.html", locals(), context_instance=RequestContext(request))
