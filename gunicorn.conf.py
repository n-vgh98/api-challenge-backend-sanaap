wsgi_app = 'config.wsgi:application'
loglevel = 'debug'
workers = 2
bind = '0.0.0.0:8000'

accesslog = '/var/log/gunicorn/api_challenge.log'
errorlog = '/var/log/gunicorn/api_challenge.log'

capture_output = True