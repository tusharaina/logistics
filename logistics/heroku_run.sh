#!/bin/bash
. bin/activate
bin/pip-2.7 -E . install --upgrade gunicorn
cd logistics
../bin/gunicorn_django -b 0.0.0.0:$PORT -w 3
