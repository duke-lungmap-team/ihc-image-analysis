import os
from jinja2 import Template

from lap import BASE_DIR as PROJECT_DIR
from lungmap_sparql_client.lungmap_sparql_client import LMClient

lminstance = LMClient()

AGE_CHOICES = lminstance.get_unique_keys(key_name='age')
GENDER = lminstance.get_unique_keys(key_name='gender')
GENDER_CHOICES = []
for x in GENDER:
    if x.lower() not in GENDER_CHOICES:
        GENDER_CHOICES.append(x.lower())

ORGANISM_CHOICES = lminstance.get_unique_keys(key_name='organism')
MAGNIFICATION_CHOICES = lminstance.get_unique_keys(key_name='magnification')

def convert_list_to_tuple(list):
    output = []
    for x in list:
        output.append((x,x))
    return tuple(output)

AGE_CHOICES = convert_list_to_tuple(AGE_CHOICES)
GENDER_CHOICES = convert_list_to_tuple(GENDER_CHOICES)
ORGANISM_CHOICES = convert_list_to_tuple(ORGANISM_CHOICES)
MAGNIFICATION_CHOICES = convert_list_to_tuple(MAGNIFICATION_CHOICES)

models_choices = """
AGE_CHOICES = {{AGE_CHOICES}}
GENDER_CHOICES = {{GENDER_CHOICES}}
ORGANISM_CHOICES = {{ORGANISM_CHOICES}}
MAGNIFICATION_CHOICES = {{MAGNIFICATION_CHOICES}}
"""

t = Template(models_choices)
t_rendered = t.render(AGE_CHOICES=AGE_CHOICES,
                      GENDER_CHOICES=GENDER_CHOICES,
                      ORGANISM_CHOICES=ORGANISM_CHOICES,
                      MAGNIFICATION_CHOICES=MAGNIFICATION_CHOICES)

with open(os.path.join(PROJECT_DIR, 'analytics', 'models_choices.py'), 'w') as f:
    f.write(t_rendered)


