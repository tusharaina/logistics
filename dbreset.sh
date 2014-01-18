#!/bin/bash
heroku pg:reset HEROKU_POSTGRESQL_CHARCOAL_URL --confirm nameless-scrubland-9890
echo "HEROKU DATABASE Reset done!"
heroku run python manage.py syncdb
heroku run python manage.py migrate client
heroku run python manage.py migrate transit
heroku run python manage.py migrate internal
heroku run python manage.py migrate awb

pg_restore --verbose --clean --no-acl --no-owner -h ec2-184-73-194-196.compute-1.amazonaws.com -U dnsbgkwdhldsoq -d dalnnb7i2dm00a latest.dump
