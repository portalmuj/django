import os
import sys
from django.contrib.staticfiles.handlers import StaticFilesHandler


path = '/home/mkkuc/mysite'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'Django.settings'

## Uncomment the lines below depending on your Django version
###### then, for Django >=1.5:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
application = StaticFilesHandler(get_wsgi_application())