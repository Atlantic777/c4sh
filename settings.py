# Django settings for c4sh project.
import socket

if socket.gethostname() == "condensation.local":
	DEBUG = True
	TEMPLATE_DEBUG = DEBUG
	APP_URL = "app"
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
	MEDIA_ROOT = '/Users/zakx/dev/c4sh/media/'
	MEDIA_URL = '/media/'
	STATIC_ROOT = '/Users/zakx/dev/c4sh/static/'
	STATIC_URL = '/static/'
	DATA_ROOT = '/Users/zakx/dev/c4sh/data/'
	TEMPLATE_DIRS = (
		"/Users/zakx/dev/c4sh/templates",
	)
	DATABASES = {
		'default': {
		'NAME': 'c4sh.sqlite3',
		'ENGINE': 'django.db.backends.sqlite3',
		}
	}
	SECRET_KEY = 'SET THIS TO A RANDOM STRING'
	ADMINS = (
		('zakx', 'zakx@localhost'),
	)
	from event_sigint12 import *
elif socket.gethostname() == "$livebox":
	# stuff from above, plus:
	SESSION_COOKIE_SECURE = True
	SESSION_EXPIRE_AT_BROWSER_CLOSE = True
else:
	import sys
	print "Please configure c4sh in settings.py. Your hostname is %s." % socket.gethostname()
	sys.exit(0)

MANAGERS = ADMINS
TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
ADMIN_MEDIA_PREFIX = '/static/admin/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.transaction.TransactionMiddleware', # <- important
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
ROOT_URLCONF = 'c4sh.urls'

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'c4sh.desk',
	'c4sh.backend',
	'c4sh.preorder',
	'south',
    'django_extensions',
	'django.contrib.markup' # required for piston-documentation
)

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}
