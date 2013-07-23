/* web: python manage.py runserver */
nginx: nginx -p `pwd` -c conf/nginx.conf
uwsgi: uwsgi conf/wsgi.ini
db: postgres -D postgresql_db
redis: redis-server
rq: rqworker
