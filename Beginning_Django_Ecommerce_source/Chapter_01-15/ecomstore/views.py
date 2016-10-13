from django.shortcuts import render_to_response
from django.template import RequestContext

def file_not_found_404(request):
    page_title = 'Page Not Found'
    return render_to_response("404.html", locals(), context_instance=RequestContext(request))

def server_error_500(request):
    return render_to_response('500.html')

def app_offline(request):
    page_title = 'Application is offline'
    return render_to_response('app_offline.html', locals(), context_instance=RequestContext(request))
