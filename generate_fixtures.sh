#!/bin/bash
python manage.py dumpdata analytics.anatomy > analytics/fixtures/anatomy.js
python manage.py dumpdata analytics.anatomyprobemap > analytics/fixtures/anatomyprobemap.js
python manage.py dumpdata analytics.experiment > analytics/fixtures/experiment.js
python manage.py dumpdata analytics.experimentprobemap > analytics/fixtures/experimentprobemap.js
python manage.py dumpdata analytics.image > analytics/fixtures/image.js
python manage.py dumpdata analytics.imageset > analytics/fixtures/imageset.js
python manage.py dumpdata analytics.imagesetprobemap > analytics/fixtures/imagesetprobemap.js
python manage.py dumpdata analytics.points > analytics/fixtures/points.js
python manage.py dumpdata analytics.probe > analytics/fixtures/probe.js
python manage.py dumpdata analytics.subregion > analytics/fixtures/subregion.js