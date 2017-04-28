#!/bin/bash
gunicorn --workers 3 --bind unix:/ihc-image-analysis/lap.sock lap.wsgi:application &
service nginx restart