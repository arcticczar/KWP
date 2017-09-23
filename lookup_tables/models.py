# -*- coding: utf-8 -*-

"""
Created on Tue Mar 07 08:33:14 2017
@author: mstelmach
"""

'''
Lookup tables are created to be modified rarely if ever.
Models here will be referenced by data in other apps.
'''

from django.db import models
from django.contrib.gis.db import models
from django.shortcuts import reverse

SizeClass = (('Small','Small'),('Medium','Medium'),('Large','Large'),('Rat','Rat'))
Status = (('MBTA', 'MBTA'),('Endangered','Endangerd'),('Non-listed','Non-listed'),('Game','Game'))
Age = (('Adult','Adult'),('Juvenile','Juvenile'),('Other','Other'),('Unknown','Unknown'))

    
#species information for all wildlife
class SpeciesDef(models.Model):
    common_name=models.CharField(max_length=200)
    scientific_name=models.CharField(max_length=200)
    species_code=models.CharField(max_length=10, unique=True, help_text="<a href='http://www.birdpop.org/docs/misc/Alpha_codes_tax.pdf' target='_blank'>4 letter code</a> ")
    species_status=models.CharField(max_length=50,choices=Status) #get status from status model
    size_class=models.CharField(max_length=20,choices=SizeClass) #get size from sizeclass model

    def __str__(self):
        return self.common_name
    
    def get_absolute_url(self):
        return reverse('speciesdef_detail', kwargs={'species_code':self.species_code})
    
    def get_update_url(self):
        return reverse('speciesdef_update', kwargs={'species_code':self.species_code})

    def get_list_url(self):
        return reverse('speciesdef_list')
    
    def get_delete_url(self):
        return reverse( 'speciesdef_delete', kwargs={'species_code':self.species_code})
    
    
Distribution = (('Endemic','Endemic'),('Indigenous','Indigenous'),('Naturalized','Naturalized') )
PlantStatus = (('Non-listed','Non-listed'),('Threatened','Threatened'),('Endangered','Endangered'))

#Species information for plants to use in outplanting and weed control
class PlantSpecies(models.Model):
    common_name = models.CharField(max_length=200)
    hawaiian_name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200, unique=True)
    species_code = models.CharField(max_length=6, unique=True, help_text='first three letters of genus and species')
    status = models.CharField(max_length=200, choices=PlantStatus)
    family = models.CharField(max_length=200)
    distribution = models.CharField(max_length=200, choices=Distribution)
    notes = models.CharField(max_length=200, null=True,blank=True)

    def __str__(self):
        return self.scientific_name
    
    def get_absolute_url(self):
        return reverse('plantspecies_detail', kwargs={'species_code':self.species_code})
    
    def get_update_url(self):
        return reverse('plantspecies_update', kwargs={'species_code':self.species_code})

    def get_list_url(self):
        return reverse('plantSpecies_list')
    
    def get_delete_url(self):
        return reverse('plantspecies_delete', kwargs={'species_code': self.species_code})
    
#Cardinal directions for use with compass bearings
class Direction(models.Model):
    direction_text = models.CharField(max_length=50, unique=True, help_text="long cardinal direction i.e. 'North'")
    direction_short = models.CharField(max_length=2, help_text="short cardinal direction i.e. 'N'")
    direction_deg = models.IntegerField(help_text="compass bearing, East=90")

    def __str__(self):
        return self.direction_text
    
    def get_absolute_url(self):
        return reverse('direction_detail', kwargs={'direction_short':self.direction_short})

    def get_update_url(self):
        return reverse('direction_update', kwargs={'direction_short':self.direction_short})
    
    def get_list_url(self):
        return reverse('direction_list')
    
    def get_delete_url(self):
        return reverse('direction_delete', kwargs={'direction_short': self.direction_short})
    
#All personnel related to site activity
class Personnel(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    initials = models.CharField(max_length=20, unique=True, help_text="Must be unique")
    staff_type = models.CharField(max_length=50, help_text="Job description")
    hire_date = models.DateField( null=True, blank=True)
    phone = models.CharField(max_length=20, help_text="all numbers i.e. ##########")
    email = models.EmailField()
    active = models.BooleanField()

    def __str__(self):
        return self.first_name +' ' + self.last_name
    
    def get_absolute_url(self):
        return reverse('personnel_detail', kwargs={'initials':self.initials})

    def get_update_url(self):
        return reverse('personnel_update', kwargs={'initials':self.initials})
    
    def get_list_url(self):
        return reverse('personnel_list')
    
    def get_delete_url(self):
        return reverse('personnel_delete', kwargs={'initials':self.initials})
    
#Canine searchers
class Canine(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return (reverse('canine_detail', kwargs={'name':self.name}))
    
    def get_update_url(self):
        return reverse('canine_update', kwargs={'name':self.name})
    
    def get_list_url(self):
        return reverse('canine_list')
    
    def get_delete_url(self):
        return reverse('canine_delete', kwargs={'name':self.name})

#General locations where activity occurs
class Site(models.Model):
    loc = models.MultiPolygonField(null=True,blank=True) #Defines general area
    locations = models.CharField(max_length=200, unique=True, help_text="Site name i.e. 'Kaheawa Wind'")
    short = models.CharField(max_length=20, unique=True, help_text="Short name i.e. KWPI")

    def __str__(self):
        return self.locations
    
    def get_absolute_url(self):
        return reverse('site_detail', kwargs={'locations':self.locations})
    
    def get_update_url(self):
        return reverse('site_update', kwargs={'locations':self.locations})

    def get_list_url(self):
        return reverse('site_list')
    
    def get_delete_url(self):
        return reverse('site_delete', kwargs={'locations':self.locations})

#On Site infrastructure buildings and sites of importance
class Infrastructure(models.Model):
    loc = models.PointField(null=True,blank=True) #point location for buildings
    name = models.CharField(max_length=200)
    physical_phase = models.ForeignKey(Site, related_name='geographic_location')
    phase = models.ForeignKey(Site, related_name='owner')
    notes = models.TextField( null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    elevation = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)

    def __str__(self):
        return self.phase.short +'-'+ self.name
    
    def get_absolute_url(self):
        return reverse('infrastructure', kwargs={'phase1':self.phase.id, 'name1':self.name})
    
    def get_update_url(self):
        return reverse('infrastructure_update', kwargs={'phase1':self.phase.id, 'name1':self.name})
    
    def get_list_url(self):
        return reverse('infrastructure_list')
    
    def get_delete_url(self):
        return reverse('infrastructure_delete', kwargs={'phase1':self.phase.id, 'name1':self.name})

class TrapType(models.Model):
    trap_type_text = models.CharField(max_length=200, unique=True)
    cost = models.CharField(max_length=200)
    check_frequency = models.IntegerField()
    

    def __str__(self):
        return self.trap_type_text
    
    def get_absolute_url(self):
        return reverse('traptype_detail', kwargs={'trap_type_text':self.trap_type_text})
    
    def get_update_url(self):
        return reverse('traptype_update', kwargs={'trap_type_text':self.trap_type_text})

    def get_list_url(self):
        return reverse('traptype_list')
    
    def get_delete_url(self):
        return reverse('traptype_delete', kwargs={'trap_type_text':self.trap_type_text})

Weather = (('Heavy','Heavy'),('Light','Light'),('Drizzle','Drizzle'),('None','None'))

NightSurveyBehavior = (('Transit','Transit'),('Circling','Circling'))

NightSurveyElevation = (('Above','Above'),('Same','Same'),('Below','Below'))

BandColor = (('Yellow','Yellow'),
             ('Black','Black'),
             ('Red','Red'),
             ('Blue','Blue'),
             ('Green','Green'),
             ('Orange','Orange'),
             ('Other','Other'))

class RandomPoints(models.Model):
    point_id = models.AutoField(primary_key=True, unique=True)
    loc = models.PointField(null=True,blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    phase = models.ForeignKey(Site)
    near = models.ForeignKey(Infrastructure)
    notes = models.TextField(null=True,blank=True)

    def __str__(self):
        string = str(self.point_id)
        return string
    
    def get_absolute_url(self):
        return reverse('randompoints_detail', kwargs={'point_id':self.point_id})
    
    def get_update_url(self):
        return reverse('randompoints_update', kwargs={'point_id':self.point_id})

    def get_list_url(self):
        return reverse('randompoints_list')
    
    def get_delete_url(self):
        return reverse('randompoints_delete', kwargs={'point_id':self.point_id})
    
    
class SearchArea(models.Model):
    loc = models.MultiPolygonField()
    site = models.ForeignKey(Site)
    turbine = models.ForeignKey(Infrastructure)
    from_0_to_10 = models.DecimalField(max_digits=20, decimal_places=10, null=True,blank=True)
    from_10_to_20 = models.DecimalField(max_digits=20, decimal_places=10, null=True,blank=True)
    from_20_to_30 = models.DecimalField(max_digits=20, decimal_places=10, null=True,blank=True)
    from_30_to_40 = models.DecimalField(max_digits=20, decimal_places=10, null=True,blank=True)
    from_40_to_50 = models.DecimalField(max_digits=20, decimal_places=10, null=True,blank=True)
    from_50_to_60 = models.DecimalField(max_digits=20, decimal_places=10, null=True,blank=True)
    from_60_to_70 = models.DecimalField(max_digits=20, decimal_places=10, null=True,blank=True)
    from_70_to_80 = models.DecimalField(max_digits=20, decimal_places=10, null=True,blank=True)
    total_searchable = models.DecimalField(max_digits=20, decimal_places=10, null=True,blank=True)
    notes = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.site.short+'-'+self.turbine.name
    
    def get_absolute_url(self):
        return reverse('searcharea_detail', kwargs={'phase1':self.site.id, 'name1':self.turbine.id})
    
    def get_update_url(self):
        return reverse('searcharea_update', kwargs={'phase1':self.site.id, 'name1':self.turbine.id})
    
    def get_list_url(self):
        return reverse('searcharea_list')
    
    def get_delete_url(self):
        return reverse('searcharea_delete', kwargs={'phase1':self.site.id, 'name1':self.turbine.id})