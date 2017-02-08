#!/bin/bash
: "${ENVIRONMENT:? You must set ENVIRONMENT (STAGING, PRODUCTION)}"
: "${SECRET_KEY:? You must set SECRET_KEY}"
: "${DATABASE_HOST:? You must set DATABASE_HOST}"
: "${DATABASE_PORT:? You must set DATABASE_PORT}"
: "${DATABASE_NAME:? You must set DATABASE_NAME}"
: "${DATABASE_USER:? You must set DATABASE_USER}"
: "${DATABASE_PASSWORD:? You must set DATABASE_PASSWORD}"
: "${FRONTEND_URL:? You must set FRONTEND_URL (http://*.*)}"
: "${ADMIN_NAME:? You must set ADMIN_NAME}"
: "${ADMIN_EMAIL_ADDRESS:? You must set ADMIN_EMAIL_ADDRESS}"
: "${EMAIL_HOST:? You must set EMAIL_HOST (smtp.*.*)}"
: "${EMAIL_PORT:? You must set EMAIL_PORT (587)}"
: "${EMAIL_USER:? You must set EMAIL_USER}"
: "${EMAIL_PASSWORD:? You must set EMAIL_PASSWORD}"
: "${EMAIL_FEEDBACK:? You must set EMAIL_FEEDBACK}"
: "${AWS_ACCESS_KEY_ID:? You must set AWS_ACCESS_KEY_ID}"
: "${AWS_SECRET_ACCESS_KEY:? You must set AWS_SECRET_ACCESS_KEY}"
: "${AWS_STORAGE_BUCKET_NAME:? You must set AWS_STORAGE_BUCKET_NAME}"
: "${REDIS_HOST:? You must set REDIS_HOST}"
: "${REDIS_PORT:? You must set REDIS_PORT}"
: "${TMDB_API_KEY:? You must set TMDB_API_KEY}"
: "${IMPORT_MEDIA_DATA:? You must set IMPORT_MEDIA_DATA (NO, YES)}"
: "${IMPORT_STATIC_FILE:? You must set IMPORT_STATIC_FILE (NO, YES)}"

# Update Database Schema
echo '----MIGRATING DATABASE----'
python ./manage.py migrate --noinput

# Import TV Show/Movie data 	
if [ "$IMPORT_MEDIA_DATA" == "YES" ]
then
	echo '----FLUSH DATABASE----'
	python ./manage.py flush --noinput

	echo '----IMPORTING TV Show/Movie DATA----'
	python ./manage.py collectmediafromtmdb
fi	

# Collecting Static Files
if [ "$IMPORT_STATIC_FILE" == "YES" ]
then
	echo '----COLLECTING STATIC FILES----'
	python ./manage.py collectstatic --noinput
fi	

# Start Gunicorn
gunicorn Wekker_API.wsgi:application -w 5 -b 0.0.0.0:8080 --log-file /logs/gunicorn-error.log --log-level error