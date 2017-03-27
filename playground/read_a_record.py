import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "lap.settings")
import django
django.setup()
from PIL import Image

from analytics.models import LungmapImage
lm = LungmapImage.objects.get(pk=1)


img = Image.open(lm.image_orig)
img.show()