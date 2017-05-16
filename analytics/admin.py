from django.contrib import admin
from analytics import models

# Register your models here.

admin.site.register(models.Experiment)
admin.site.register(models.Image)
admin.site.register(models.Probe)
admin.site.register(models.ExperimentProbeMap)
