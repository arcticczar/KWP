# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import (lookup_index, 
                     
                    Status, 
                    InfrastructureView,InfrastructureUpdate,InfrastructureList,InfrastructureCreate,InfrastructureDelete,
                    SpeciesDefView,SpeciesDefList,SpeciesDefCreate,SpeciesDefUpdate,SpeciesDefDelete,
                    PlantSpeciesView,PlantSpeciesList,PlantSpeciesCreate,PlantSpeciesUpdate,PlantSpeciesDelete,
                    DirectionView,DirectionList,DirectionCreate,DirectionUpdate,DirectionDelete,
                    personnel_data,PersonnelList,PersonnelCreate,PersonnelUpdate,PersonnelDelete,
                    CanineView,CanineList,CanineCreate,CanineUpdate,CanineDelete,
                    SiteView,SiteList,SiteCreate,SiteUpdate,SiteDelete,
                    TrapTypeView,TrapTypeList,TrapTypeCreate,TrapTypeUpdate,TrapTypeDelete,
                    RandomPointsView,RandomPointsList,RandomPointsCreate,RandomPointsUpdate,RandomPointsDelete,
                    SearchAreaView,SearchAreaList,SearchAreaCreate,SearchAreaUpdate,SearchAreaDelete,
                    AllModels
                    )

urlpatterns = [
        url(r'^$', AllModels.as_view(), name='lookup'),
        url(r'speciesdef$', SpeciesDefList.as_view(), name='speciesdef_list'),
        url(r'speciesdef/create/$', SpeciesDefCreate.as_view(), name='speciesdef_create'),
        url(r'speciesdef/update/(?P<species_code>[\w\-]+)$', SpeciesDefUpdate.as_view(), name='speciesdef_update'),
        url(r'speciesdef/(?P<species_code>[\w\-]+)/delete/$', SpeciesDefDelete.as_view(), name='speciesdef_delete'),
        url(r'speciesdef/(?P<species_code>[\w\-]+)$', SpeciesDefView.as_view(), name='speciesdef_detail'),
        url(r'plantspecies$', PlantSpeciesList.as_view(), name='plantspecies_list'),
        url(r'plantspecies/create/$', PlantSpeciesCreate.as_view(), name='plantspecies_create'),
        url(r'plantspecies/update/(?P<species_code>[\w\-]+)$',PlantSpeciesUpdate.as_view(), name='plantspecies_update'),
        url(r'plantspecies/(?P<species_code>[\w\-]+)/delete/$', PlantSpeciesDelete.as_view(), name='plantspecies_delete'),
        url(r'plantspecies/(?P<species_code>[\w\-]+)$', PlantSpeciesView.as_view(), name='plantspecies_detail'),
        url(r'direction$', DirectionList.as_view(), name='direction_list'),
        url(r'direction/create/$', DirectionCreate.as_view(), name='direction_create'),
        url(r'direction/update/(?P<direction_short>[\w\-]+)$',DirectionUpdate.as_view(),name='direction_update'),
        url(r'direction/(?P<direction_short>[\w\-]+)/delete/$', DirectionDelete.as_view(), name='direction_delete'),
        url(r'direction/(?P<direction_short>[\w\-]+)$', DirectionView.as_view(), name='direction_detail'),
        url(r'personnel$', PersonnelList.as_view(), name='personnel_list'),
        url(r'personnel/create/$', PersonnelCreate.as_view(), name='personnel_create'),
        url(r'personnel/update/(?P<initials>[\w\-]+)/$', PersonnelUpdate.as_view(), name='personnel_update'),
        url(r'personnel/(?P<initials>[\w\-]+)/delete/$', PersonnelDelete.as_view(), name='personnel_delete'),
        url(r'personnel/(?P<initials>[\w\-]+)$', personnel_data, name='personnel_detail'),
        url(r'canine$', CanineList.as_view(), name='canine_list'),
        url(r'canine/create/$', CanineCreate.as_view(), name='canine_create'),
        url(r'canine/update/(?P<name>[\w\-]+)/$', CanineUpdate.as_view(), name='canine_update'),
        url(r'canine/(?P<name>[\w\- ]+)/delete/$', CanineDelete.as_view(), name='canine_delete'),
        url(r'canine/(?P<name>[\w\- ]+)/$', CanineView.as_view(), name='canine_detail'),
        url(r'site$', SiteList.as_view(), name='site_list'),
        url(r'site/create/$', SiteCreate.as_view(), name='site_create'),
        url(r'site/(?P<locations>[\w\- ]+)/delete/$', SiteDelete.as_view(), name='site_delete'),
        url(r'site/(?P<locations>[\w\- ]+)/$', SiteView.as_view(), name='site_detail'),
        url(r'site/update/(?P<locations>[\w\- ]+)/$', SiteUpdate.as_view(), name='site_update'),
        url(r'infrastructure$', InfrastructureList.as_view(), name='infrastructure_list'),
        url(r'infrastructure/update/(?P<phase1>[\w\-]+)/(?P<name1>[\w\-]+)$', InfrastructureUpdate.as_view(), name='infrastructure_update'),
        url(r'infrastructure/create/$', InfrastructureCreate.as_view(), name='infrastructure_create'),
        url(r'infrastructure/(?P<phase1>[\w\-]+)/(?P<name1>[\w\-]+)/delete$', InfrastructureDelete.as_view(), name='infrastructure_delete'),
        url(r'infrastructure/(?P<phase1>[\w\-]+)/(?P<name1>[\w\-]+)$', InfrastructureView.as_view(), name='infrastructure'),
        url(r'traptype$', TrapTypeList.as_view(), name='traptype_list'),
        url(r'traptype/update/(?P<trap_type_text>[\w\- ]+)$', TrapTypeUpdate.as_view(), name='traptype_update'),
        url(r'traptype/create/$', TrapTypeCreate.as_view(), name='traptype_create'),
        url(r'traptype/(?P<trap_type_text>[\w\- ]+)/delete/$', TrapTypeDelete.as_view(), name='traptype_delete'),
        url(r'traptype/(?P<trap_type_text>[\w\- ]+)$', TrapTypeView.as_view(), name='traptype_detail'),
        url(r'randompoints$', RandomPointsList.as_view(), name='randompoints_list'),
        url(r'randompoints/create/$', RandomPointsCreate.as_view(), name='randompoints_create'),
        url(r'randompoints/(?P<point_id>[\w\-]+)/delete/$', RandomPointsDelete.as_view(), name='randompoints_delete'),
        url(r'randompoints/(?P<point_id>[\w\-]+)$', RandomPointsView.as_view(), name='randompoints_detail'),
        url(r'randompoints/update/(?P<point_id>[\w\-]+)$', RandomPointsUpdate.as_view(), name='randompoints_update'),
        url(r'searcharea$', SearchAreaList.as_view(), name='searcharea_list'),
        url(r'searcharea/create/$', SearchAreaCreate.as_view(), name='searcharea_create'),
        url(r'searcharea/update/(?P<phase1>[\w\-]+)/(?P<name1>[\w\-]+)$', SearchAreaUpdate.as_view(), name='searcharea_update'),
        url(r'searcharea/(?P<phase1>[\w\-]+)/(?P<name1>[\w\-]+)/delete$', SearchAreaDelete.as_view(), name='searcharea_delete'),
        url(r'searcharea/(?P<phase1>[\w\-]+)/(?P<name1>[\w\-]+)$', SearchAreaView.as_view(), name='searcharea_detail')
	]