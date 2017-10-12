#!/bin/bash
python manage.py dumpdata analytics.anatomy > analytics/fixtures/anatomy.json
python manage.py dumpdata analytics.anatomyprobemap > analytics/fixtures/anatomy_probe_map.json
python manage.py dumpdata analytics.experiment > analytics/fixtures/experiment.json
python manage.py dumpdata analytics.experimentprobemap > analytics/fixtures/experiment_probe_map.json
python manage.py dumpdata analytics.image > analytics/fixtures/image.json
python manage.py dumpdata analytics.imageset > analytics/fixtures/image_set.json
python manage.py dumpdata analytics.imagesetprobemap > analytics/fixtures/image_set_probe_map.json
python manage.py dumpdata analytics.points > analytics/fixtures/points.json
python manage.py dumpdata analytics.probe > analytics/fixtures/probe.json
python manage.py dumpdata analytics.subregion > analytics/fixtures/subregion.json