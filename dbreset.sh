#!/bin/bash
heroku pg:reset HEROKU_POSTGRESQL_CHARCOAL_URL --confirm nameless-scrubland-9890
echo "HEROKU DATABASE Reset done!"
heroku run python manage.py syncdb
heroku run python manage.py migrate --all
pg_restore --verbose --clean --no-acl --no-owner -h ec2-54-204-21-178.compute-1.amazonaws.com -U idlrtcknznmgcz -d d67g2km220h4dc latest.dump
