
from django import forms

from web.forms.bootstrap import BootStrapForm
from web import models
from web.forms.widgets import ColorRadioSelect

class ProjectModelForm(BootStrapForm, forms.ModelForm):
    bootstrap_class_exclude = ['color']
    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc': forms.Textarea(),
            'color': ColorRadioSelect(attrs={'class': 'color-radio'})
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        exists = models.Project.objects.filter(name=self.cleaned_data['name'], creator=self.request.tracer.user).exists()
        if exists:
            raise forms.ValidationError('Project name already exists')
        
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()
        if count >= self.request.tracer.price_policy.project_num:
            raise forms.ValidationError('You can only create %s projects under this price policy' % self.request.tracer.price_policy.project_num)
        
        return self.cleaned_data['name']