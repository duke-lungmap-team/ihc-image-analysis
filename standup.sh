#!/usr/bin/env bash
python3 /ihc-image-analysis/manage.py makemigrations analytics
python3 /ihc-image-analysis/manage.py migrate
python3 /ihc-image-analysis/manage.py runserver 0.0.0.0:8000