from django.contrib import admin
from analytics.models import Experiment, LungmapImage, ProbeExperiments

# Register your models here.

admin.site.register(Experiment)
admin.site.register(LungmapImage)
admin.site.register(ProbeExperiments)
