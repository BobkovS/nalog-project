#!/bin/sh
exec gunicorn -b :8282 app:application_object --timeout 7200
