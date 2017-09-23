from __future__ import unicode_literals

from django.apps import apps
from django.template import Context, loader
from django.conf import settings
from django.http.response import HttpResponse, Http404
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, render_to_response


def homepage(request):
	#Get all apps into a set
	applist = set()
	for item in settings.INSTALLED_APPS:
		appname = item.split('.')[0]
		if appname!='django':
			applist.add(appname)
	
	modellist = dict()
	for app in applist:
		modellist[app]=apps.get_app_config(app).models
	

	template = loader.get_template('landingPage.html')
	context = Context({'applist':applist, 'modellist':modellist})
	output = template.render(context)
	return HttpResponse(output)

class data(View):
    template_name = 'general.html'
    
    
    def get_absolute_url(self, appstr, model):
        return reverse('data', args={'appstr':self.appstr,'model':self.model})
        
    def get(self, request, appstr, model):
        modelactual=apps.get_model(appstr, model)
        modelitems = modelactual.objects.all()
        return render(
                request, 
                self.template_name, 
                {'model':modelactual._meta.object_name, 'modelitems': modelitems})