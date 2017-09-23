# -*- coding: utf-8 -*-
"""
Created on Sun Jun 04 10:53:42 2017

@author: MStelmach
"""

from django import forms
from django.core.exceptions import ValidationError

from .models import *

class clean_species_code_mixin:
    def clean_species_code(self):
        newcode=self.cleaned_data['species_code'].upper()
        if newcode=='CREATE':
            raise ValidationError('Code may not be "create"')
        return newcode

class SpeciesDefForm(forms.ModelForm, clean_species_code_mixin):
    class Meta:
        model = SpeciesDef
        fields = '__all__'
        
    def clean_common_name(self):
        return self.cleaned_data['common_name'].lower()
    
    
    
class PlantSpeciesForm(forms.ModelForm, clean_species_code_mixin):
    class Meta:
        model = PlantSpecies
        fields = '__all__'
        
        
class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = '__all__'
        
    def clean_dir(self):
        newdir = self.cleaned_data['direction_short'].upper()
        if newdir == 'CREATE':
            raise ValidationError('Direction cannot be "Create"')
        return newdir

class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = '__all__'
        
    def clean_initials(self):
        newinitials = self.cleaned_data['initials'].upper()
        if newinitials == 'CREATE':
            raise ValidationError('Initials cannot be "Create"')
        return newinitials
    
class CanineForm(forms.ModelForm):
    class Meta:
        model = Canine
        fields = '__all__'
        
    def clean_name(self):
        newname = self.cleaned_data['name'].title()
        if newname == 'Create':
            raise ValidationError('Name cannot be "Create"')
        return newname
    
class SiteForm(forms.ModelForm):
    class Meta:
        model= Site
        fields = '__all__'
        
    def clean_locations(self):
        newlocations = self.cleaned_data['locations'].title()
        if newlocations == 'Create':
            raise ValidationError('Name cannot be "Create"')
        return newlocations
    
class InfrastructureForm(forms.ModelForm):
    class Meta:
        model = Infrastructure
        fields = '__all__'
        
class TrapTypeForm(forms.ModelForm):
    class Meta:
        model = TrapType
        fields = '__all__'
        
    def clean_trap_type(self):
        new_trap_type=self.cleaned_data['trap_type_text'].lower()
        if new_trap_type == 'create':
            raise ValidationError('Name cannot be "create"')
        return new_trap_type

class SearchAreaForm(forms.ModelForm):
    class Meta:
        model = SearchArea
        fields = '__all__'
        
class RandomPointsForm(forms.ModelForm):
    class Meta:
        model=RandomPoints
        fields = '__all__'