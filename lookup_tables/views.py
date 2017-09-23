from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http.response import HttpResponse, Http404
from django.template import RequestContext, loader
from django.apps import apps
from django.views.generic import View
from django.core.urlresolvers import reverse

from .models import (SpeciesDef,
                     PlantSpecies,
                     Direction,
                     Personnel,
                     Canine,
                     Site,
                     Infrastructure,
                     TrapType,
                     RandomPoints,
                     SearchArea,
                     Status,
                     SizeClass,
                     Age,
                     Distribution,
                     PlantStatus,
                     Weather,
                     NightSurveyBehavior,
                     NightSurveyElevation,
                     BandColor,
                     
                     )
from .forms import (SpeciesDefForm, 
                    PlantSpeciesForm, 
                    DirectionForm,
                    PersonnelForm,
                    CanineForm,
                    SiteForm,
                    InfrastructureForm,
                    TrapTypeForm,
                    SearchAreaForm,
                    RandomPointsForm,
                    )

#******************Mixin models *************************

class get_mixin:
    
    
    def get(self, request):
        view = 'lookup'
        listview=reverse(view)
        return render(request, self.template_name, {'form': self.form_class(), 'listview':listview})

class post_mixin:
    def post(self, request):
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            newform = bound_form.save()
            return redirect(newform)
        else:
            return render(request, self.template_name, {'form':bound_form})

class list_view_mixin:
    def get(self, request):
        model = apps.get_model(app_label='lookup_tables', model_name=self.modelname)
        objects = model.objects.all()
        urllist = []
        for item in objects:
            urllist.append([item, item.get_absolute_url(), item.get_update_url(), item.get_delete_url()])
        return render(request, self.template_name, {'urllist':urllist, 'modelname':self.modelname.title()})

#Return all models in the lookup_tables app
def lookup_index(request):
	models = '<br/>'.join(apps.get_app_config('lookup_tables').models)
	return HttpResponse('<H2>Lookup landing page</h2><br/>'+models)

class AllModels(View):
    template_name = 'lookup_tables/lookup_landing.html'
    
    def get(self, request):
        modelnames = apps.get_app_config('lookup_tables').models
        return render(request, self.template_name, {'modelnames':modelnames})
        
        
            
        

#******************Avian Species *************************

#Return details for each speices def
class SpeciesDefList(View, list_view_mixin):
    template_name = 'lookup_tables/list_view.html'
    modelname = 'SpeciesDef'
                    
        

class SpeciesDefView(View):
    template_name = 'lookup_tables/data_template.html'
    
    def get(self, request, species_code):
    	data = get_object_or_404(SpeciesDef, species_code__iexact=species_code.lower()) # return data
    	fieldlist = [field.name for field in data._meta.fields] #return field list as string
    	attr = [getattr(data, item) for item in fieldlist] #return list of object attributes.
    	ziplist = zip(fieldlist, attr) #merge column names and values
        url=data.get_update_url
        deleteurl = data.get_delete_url
    	return render(request, self.template_name,  {'instance': species_code, 'ziplist': ziplist, 'update':url, 'delete':deleteurl})

class SpeciesDefCreate(View,get_mixin,post_mixin):
    form_class= SpeciesDefForm
    view = 'speciesdef_list'
    template_name = 'lookup_tables/SpeciesDef_Form.html'

class SpeciesDefUpdate(View):
    form_class = SpeciesDefForm
    model = SpeciesDef
    template_name = 'lookup_tables/speciesdef_update.html'

    def get(self, request, species_code):
        post = get_object_or_404(self.model, species_code__iexact=species_code.upper())
        detail = post.get_absolute_url
        context={'form': self.form_class(instance=post), 'post':post, 'detail':detail}
        return render(request, self.template_name, context)
    
    def post(self, request, species_code):
        post = get_object_or_404(self.model, species_code__iexact=species_code.upper())
        bound_form=self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            newpost=bound_form.save()
            return redirect(newpost)
        else:
            context = {'form':bound_form, 'post':post}
            return render(request, self.template_name, context)
        
class SpeciesDefDelete(View):
    model = SpeciesDef
    
    def get(self, request, species_code):
        post = get_object_or_404(self.model, species_code__iexact=species_code)
        listview = reverse('speciesdef_list')
        return render(request, 'lookup_tables/speciesdef_delete.html', {'post':post, 'listview':listview})
    
    def post(self, request, species_code):
        post = get_object_or_404(self.model, species_code__iexact=species_code)
        post.delete()
        return redirect('speciesdef_list')

#******************PLant Species *************************
    
class PlantSpeciesView(View):
    template_name = 'lookup_tables/data_template.html'
    
    def get(self, request, species_code):
    	data = get_object_or_404(PlantSpecies, species_code__iexact=species_code) # return data
    	fieldlist = [field.name for field in data._meta.fields] #return field list as string
    	attr = [getattr(data, item) for item in fieldlist] #return list of object attributes.
    	ziplist = zip(fieldlist, attr) #merge column names and value
    	return render(request, self.template_name,  {'instance': species_code, 'ziplist': ziplist, 'update':data.get_update_url, 'delete':data.get_delete_url})

class PlantSpeciesList(View, list_view_mixin):
    template_name = 'lookup_tables/list_view.html'
    modelname = 'PlantSpecies'

class PlantSpeciesCreate(View, get_mixin, post_mixin):
    view = 'plantspecies_list'
    form_class= PlantSpeciesForm
    template_name = 'lookup_tables/PlantSpecies_form.html'
    
class PlantSpeciesUpdate(View):
    form_class=PlantSpeciesForm
    model = PlantSpecies
    template_name = 'lookup_tables/plantspecies_update.html'
    
    def get_object(self, species_code):
        return get_object_or_404(self.model, species_code__iexact=species_code.upper())
    
    def get(self, request, species_code):
        post=self.get_object(species_code)
        listview = reverse('plantspecies_list')
        context={'form': self.form_class(instance=post), 'post':post, 'listview':listview}
        return render(request, self.template_name, context)
        
    def post(self, request, species_code):
        post=self.get_object(species_code)
        bound_form=self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            newpost=bound_form.save()
            return redirect(newpost)
        else:
            context = {'form':bound_form, 'post':post}
            return render(request, self.template_name, context)

class PlantSpeciesDelete(View):
    model = PlantSpecies
    
    def get(self, request, species_code):
        post = get_object_or_404(self.model, species_code__iexact=species_code)
        return render(request, 'lookup_tables/speciesdef_delete.html', {'post':post})
    
    def post(self, request, species_code):
        post = get_object_or_404(self.model, species_code__iexact=species_code)
        post.delete()
        return redirect('plantspecies_list')

#******************Cardinal Directions *************************    
    
class DirectionView(View):
    template_name = 'lookup_tables/data_template.html'
    
    def get(self, request, direction_short):
    	data = get_object_or_404(Direction, direction_short__iexact=direction_short) # return data
    	fieldlist = [field.name for field in data._meta.fields] #return field list as string
    	attr = [getattr(data, item) for item in fieldlist] #return list of object attributes.
    	ziplist = zip(fieldlist, attr) #merge column names and values
    	return render(request, self.template_name,  {'instance': direction_short, 'ziplist': ziplist, 'update':data.get_update_url, 'delete':data.get_delete_url})    

class DirectionList(View, list_view_mixin):
    view = 'direction_list'
    template_name = 'lookup_tables/list_view.html'
    modelname = 'Direction'

class DirectionCreate(View, get_mixin, post_mixin):
    form_class = DirectionForm
    template_name = 'lookup_tables/Direction_form.html'
    
    
class DirectionUpdate(View):
    form_class = DirectionForm
    model = Direction
    template_name = 'lookup_tables/direction_update.html'
    
    def get_object(self, direction_short):
        return get_object_or_404(self.model, direction_short__iexact=direction_short.upper())
    
    def get(self, request, direction_short):
        post=self.get_object(direction_short)
        listview = reverse('direction_list')
        context={'form': self.form_class(instance=post), 'post':post, 'listview':listview}
        return render(request, self.template_name, context)
        
    def post(self, request, direction_short):
        post=self.get_object(direction_short)
        bound_form=self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            newpost=bound_form.save()
            return redirect(newpost)
        else:
            context = {'form':bound_form, 'post':post}
            return render(request, self.template_name, context)    

class DirectionDelete(View):
    model = Direction
    
    def get(self, request, direction_short):
        post = get_object_or_404(self.model, direction_short__iexact=direction_short)
        return render(request, 'lookup_tables/direction_delete.html', {'post':post})
    
    def post(self, request, direction_short):
        post = get_object_or_404(self.model, direction_short__iexact=direction_short)
        post.delete()
        return redirect('direction_list')
    
#****************** Canines  *************************    
    
class CanineView(View):
    template_name = 'lookup_tables/data_template.html'
    
    def get(self, request, name):
    	data = get_object_or_404(Canine, name__iexact=name) # return data
    	fieldlist = [field.name for field in data._meta.fields] #return field list as string
    	attr = [getattr(data, item) for item in fieldlist] #return list of object attributes.
    	ziplist = zip(fieldlist, attr) #merge column names and values
    	return render(request, self.template_name,  {'instance': name, 'ziplist': ziplist, 'update':data.get_update_url, 'delete':data.get_delete_url})

class CanineList(View, list_view_mixin):
    template_name = 'lookup_tables/list_view.html'
    modelname = 'Canine'
    
class CanineCreate(View, get_mixin, post_mixin):
    view = 'canine_list'
    form_class = CanineForm
    template_name='lookup_tables/Canine_form.html'
    
class CanineUpdate(View):
    form_class=CanineForm
    model = Canine
    template_name = 'lookup_tables/canine_update.html'
    
    def get_object(self, name):
        return get_object_or_404(self.model, name__iexact=name.upper())
    
    def get(self, request, name):
        post=self.get_object(name)
        
        context={'form': self.form_class(instance=post), 'post':post}
        return render(request, self.template_name, context)
        
    def post(self, request, name):
        post=self.get_object(name)
        bound_form=self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            newpost=bound_form.save()
            return redirect(newpost)
        else:
            context = {'form':bound_form, 'post':post}
            return render(request, self.template_name, context)

class CanineDelete(View):
    model = Canine
    
    def get(self, request, name):
        post = get_object_or_404(self.model, name__iexact=name)
        return render(request, 'lookup_tables/canine_delete.html', {'post':post})
    
    def post(self, request, name):
        post = get_object_or_404(self.model, name__iexact=name)
        post.delete()
        return redirect('canine_list')

#******************Work Sites *************************
    
class SiteView(View):
    template_name = 'lookup_tables/data_template.html'
    
    def get(self, request, locations):
    	data = get_object_or_404(Site, locations__iexact=locations) # return data
    	fieldlist = [field.name for field in data._meta.fields] #return field list as string
    	attr = [getattr(data, item) for item in fieldlist] #return list of object attributes.
    	ziplist = zip(fieldlist, attr) #merge column names and values
    	return render(request, self.template_name,  {'instance': locations, 'ziplist': ziplist, 'update':data.get_update_url, 'delete':data.get_delete_url})

class SiteList(View, list_view_mixin):
    view = 'site_list'
    template_name = 'lookup_tables/list_view.html'
    modelname = 'Site'

class SiteCreate(View, get_mixin, post_mixin):
    form_class = SiteForm
    template_name='lookup_tables/Site_Form.html'
    
class SiteUpdate(View):
    form_class=SiteForm
    model = Site
    template_name = 'lookup_tables/site_update.html'
    
    def get_object(self, locations):
        return get_object_or_404(self.model, locations__iexact=locations)
    
    def get(self, request, locations):
        post=self.get_object(locations)
        context={'form': self.form_class(instance=post), 'post':post}
        return render(request, self.template_name, context)
        
    def post(self, request, locations):
        post=self.get_object(locations)
        bound_form=self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            newpost=bound_form.save()
            return redirect(newpost)
        else:
            context = {'form':bound_form, 'post':post}
            return render(request, self.template_name, context)

class SiteDelete(View):
    model = Site
    
    def get(self, request, locations):
        post = get_object_or_404(self.model, locations__iexact=locations)
        return render(request, 'lookup_tables/site_delete.html', {'post':post})
    
    def post(self, request, locations):
        post = get_object_or_404(self.model, locations__iexact=locations)
        post.delete()
        return redirect('site_list')

#******************Infrastructure *************************

#Class based view to return the details of infrastructure (location)
class InfrastructureView(View):
    template_name = 'lookup_tables/data_template.html'
    
    def get_absolute_url(self, phase1, name1):
        return reverse('infrastructure', kwargs={'phase1':phase1, 'name1':name1})
    
    def get(self, request, phase1, name1):
    	data = get_object_or_404(Infrastructure.objects.filter(phase=phase1).filter(name=name1)) # return data
    	fieldlist = [field.name for field in data._meta.fields] #return field list as string
    	attr = [getattr(data, item) for item in fieldlist] #return list of object attributes.
    	ziplist = zip(fieldlist, attr) #merge column names and values
    	return render(request, self.template_name,  {'instance': data.__str__, 'ziplist': ziplist, 'update':data.get_update_url, 'delete':data.get_delete_url})

class InfrastructureList(View, list_view_mixin):
    template_name = 'lookup_tables/list_view.html'
    modelname = 'Infrastructure'
     
class InfrastructureCreate(View, get_mixin, post_mixin):
    view = 'infrastructure_list'
    form_class = InfrastructureForm
    template_name = 'lookup_tables/Infrastructure_Form.html'
    
class InfrastructureUpdate(View):
    form_class=InfrastructureForm
    model = Infrastructure
    template_name = 'lookup_tables/infrastructure_update.html'
    
    def get_object(self, phase1, name1):
        return get_object_or_404(self.model.objects.filter(phase=phase1 ).filter(name=name1))
    
    def get(self, request, phase1, name1):
        post=self.get_object(phase1, name1)
        context={'form': self.form_class(instance=post), 'post':post}
        return render(request, self.template_name, context)
        
    def post(self, request, phase1, name1):
        post=self.get_object(phase1, name1)
        bound_form=self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            newpost=bound_form.save()
            return redirect(newpost)
        else:
            context = {'form':bound_form, 'post':post}
            return render(request, self.template_name, context)

class InfrastructureDelete(View):
    model=Infrastructure
    
    def get(self, request, phase1, name1):
        post = get_object_or_404(self.model.objects.filter(phase=phase1 ).filter(name=name1))
        return render(request, 'lookup_tables/infrastructure_delete.html', {'phase1':phase1, 'name1':name1, 'post':post})
    
    def post(self, request, phase1, name1):
        post = get_object_or_404(self.model.objects.filter(phase=phase1 ).filter(name=name1))
        post.delete()
        return redirect('infrastructure_list')

#****************** Traps *************************
        
class TrapTypeView(View):
    template_name = 'lookup_tables/data_template.html'
    
    def get(self, request, trap_type_text):
    	data = get_object_or_404(TrapType, trap_type_text__iexact=trap_type_text) # return data
    	fieldlist = [field.name for field in data._meta.fields] #return field list as string
    	attr = [getattr(data, item) for item in fieldlist] #return list of object attributes.
    	ziplist = zip(fieldlist, attr) #merge column names and values
    	return render(request, self.template_name,  {'instance': trap_type_text, 'ziplist': ziplist, 'update':data.get_update_url, 'delete':data.get_delete_url})

class TrapTypeList(View, list_view_mixin):
    template_name = 'lookup_tables/list_view.html'
    modelname = 'TrapType'

class TrapTypeCreate(View, get_mixin, post_mixin):
    view = 'traptype_list'
    form_class = TrapTypeForm
    template_name = 'lookup_tables/traptype_form.html'
    
class TrapTypeUpdate(View):
    form_class = TrapTypeForm
    model=TrapType
    template_name= 'lookup_tables/traptype_update.html'
    
    def get_object(self, trap_type_text):
        return get_object_or_404(self.model, trap_type_text__iexact=trap_type_text)
    
    def get(self, request, trap_type_text):
        post=self.get_object(trap_type_text)
        context={'form': self.form_class(instance=post), 'post':post}
        return render(request, self.template_name, context)
        
    def post(self, request, trap_type_text):
        post=self.get_object(trap_type_text)
        bound_form=self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            newpost=bound_form.save()
            return redirect(newpost)
        else:
            context = {'form':bound_form, 'post':post}
            return render(request, self.template_name, context) 

class TrapTypeDelete(View):
    model = TrapType
    
    def get(self, request, trap_type_text):
        post = get_object_or_404(self.model, trap_type_text__iexact=trap_type_text)
        return render(request, 'lookup_tables/traptype_delete.html', {'post':post})
    
    def post(self, request, trap_type_text):
        post = get_object_or_404(self.model, trap_type_text__iexact=trap_type_text)
        post.delete()
        return redirect('traptype_list')

#****************** Randomized Points *************************
            
class RandomPointsView(View):
    template_name = 'lookup_tables/data_template.html'
    
    def get(self, request, point_id):
    	data = get_object_or_404(RandomPoints, point_id=point_id) # return data
    	fieldlist = [str(field.name) for field in data._meta.fields] #return field list as string
    	attr = [str(getattr(data, item)) for item in fieldlist] #return list of object attributes.
    	ziplist = zip(fieldlist, attr) #merge column names and values
    	return render(request, self.template_name,  {'instance': point_id, 'ziplist': ziplist, 'update':data.get_update_url, 'delete':data.get_delete_url})

class RandomPointsList(View, list_view_mixin):
    template_name = 'lookup_tables/list_view.html'
    modelname = 'RandomPoints'

class RandomPointsCreate(View, get_mixin, post_mixin):
    view = 'randompoints_list'
    form_class = RandomPointsForm
    template_name='lookup_tables/randompoints_form.html'
    
class RandomPointsUpdate(View):
    form_class = RandomPointsForm
    model=RandomPoints
    template_name= 'lookup_tables/randompoints_update.html'
    
    def get_object(self, point_id):
        return get_object_or_404(self.model, point_id=point_id)
    
    def get(self, request, point_id):
        post=self.get_object(point_id)
        context={'form': self.form_class(instance=post), 'post':post}
        return render(request, self.template_name, context)
        
    def post(self, request, point_id):
        post=self.get_object(point_id)
        bound_form=self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            newpost=bound_form.save()
            return redirect(newpost)
        else:
            context = {'form':bound_form, 'post':post}
            return render(request, self.template_name, context) 

class RandomPointsDelete(View):
    model=RandomPoints
    
    def get(self, request, point_id):
        post = get_object_or_404(self.model, point_id=point_id)
        return render(request, 'lookup_tables/randompoints_delete.html', {'point_id':point_id, 'post':post})
    
    def post(self, request, point_id):
        post = get_object_or_404(self.model, point_id=point_id)
        post.delete()
        return redirect('randompoints_list')

#****************** Search Area *************************

class SearchAreaView(View):
    template_name = 'lookup_tables/data_template.html'
    
    def get(self, request, phase1, name1):
    	data = get_object_or_404(SearchArea.objects.filter(site=phase1).filter(turbine=name1)) # return data
    	fieldlist = [field.name for field in data._meta.fields] #return field list as string
    	attr = [getattr(data, item) for item in fieldlist] #return list of object attributes.
    	ziplist = zip(fieldlist, attr) #merge column names and values
    	return render(request, self.template_name,  {'instance': data.__str__, 'ziplist': ziplist, 'update':data.get_update_url, 'delete':data.get_delete_url})

class SearchAreaList(View, list_view_mixin):
    template_name = 'lookup_tables/list_view.html'
    modelname = 'SearchArea'

class SearchAreaCreate(View, get_mixin, post_mixin):
    view = 'searcharea_list'
    form_class=SearchAreaForm
    template_name='lookup_tables/SearchArea_Form.html'
    
class SearchAreaUpdate(View):
    form_class = SearchAreaForm
    model=SearchArea
    template_name= 'lookup_tables/searcharea_update.html'
    
    def get_object(self, phase1, name1):
        return get_object_or_404(self.model.objects.filter(site=phase1 ).filter(turbine=name1))
    
    def get(self, request, phase1, name1):
        post=self.get_object(phase1, name1)
        context={'form': self.form_class(instance=post), 'post':post}
        return render(request, self.template_name, context)
        
    def post(self, request, phase1, name1):
        post=self.get_object(phase1, name1)
        bound_form=self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            newpost=bound_form.save()
            return redirect(newpost)
        else:
            context = {'form':bound_form, 'post':post}
            return render(request, self.template_name, context)


class SearchAreaDelete(View):
    model=SearchArea
    
    def get(self, request, phase1, name1):
        post = get_object_or_404(self.model.objects.filter(site=phase1 ).filter(turbine=name1))
        return render(request, 'lookup_tables/searcharea_delete.html', {'post':post})
    
    def post(self, request, phase1, name1):
        post = get_object_or_404(self.model.objects.filter(site=phase1 ).filter(turbine=name1))
        post.delete()
        return redirect('searcharea_list')
#****************** Personnel *************************

#Return details of perssonel by initials lookup/personnel/ms/data
def personnel_data(request, initials):
	data = get_object_or_404(Personnel, initials__iexact=initials) # return data
	fieldlist = [field.name for field in data._meta.fields] #return field list as string
	attr = [getattr(data, item) for item in fieldlist] #return list of object attributes.
	ziplist = zip(fieldlist, attr) #merge column names and values
	template = loader.get_template('lookup_tables/data_template.html')
	context = RequestContext(request, {'instance': initials, 'ziplist': ziplist, 'update':data.get_update_url, 'delete':data.get_delete_url})
	output = template.render(context)
	return HttpResponse(output)

class PersonnelList(View, list_view_mixin):
    template_name = 'lookup_tables/list_view.html'
    modelname = 'Personnel'

class PersonnelCreate(View, get_mixin, post_mixin):
    view = 'personnel_list'
    form_class= PersonnelForm
    template_name = 'lookup_tables/Personnel_form.html'
    
class PersonnelUpdate(View):
    form_class = PersonnelForm
    model=Personnel
    template_name= 'lookup_tables/personnel_update.html'
    
    def get_object(self, initials):
        return get_object_or_404(self.model, initials__iexact=initials)
    
    def get(self, request, initials):
        post=self.get_object(initials)
        context={'form': self.form_class(instance=post), 'post':post}
        return render(request, self.template_name, context)
        
    def post(self, request, initials):
        post=self.get_object(initials)
        bound_form=self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            newpost=bound_form.save()
            return redirect(newpost)
        else:
            context = {'form':bound_form, 'post':post}
            return render(request, self.template_name, context) 
        
class PersonnelDelete(View):
    model = Personnel
    
    def get(self, request, initials):
        post = get_object_or_404(self.model, initials__iexact=initials)
        return render(request, 'lookup_tables/personnel_delete.html', {'post':post})
    
    def post(self, request, initials):
        post = get_object_or_404(self.model, initials__iexact=initials)
        post.delete()
        return redirect('personnel_list')
    

#General class based view for listing all records in a model.
class data(View):
    template_name = 'lookup_tables/general.html'
    
    def get_absolute_url(self, model):
        return reverse('data', args={'model':self.model})
        
    def get(self, request, model):
        modelactual=apps.get_model('lookup_tables', model)
        modelitems = modelactual.objects.all()
        return render(
                request, 
                self.template_name, 
                {'model':modelactual._meta.object_name, 'modelitems':modelitems})