import os
import sys
import tempfile
from django.conf import settings

def run_tests():
    # Use a temporary database for testing
    db_config = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
    
    # Configure test settings
    test_settings = {
        'DATABASES': {
            'default': db_config,
        },
        'MEDIA_ROOT': tempfile.mkdtemp(),
        'STATICFILES_STORAGE': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        'PASSWORD_HASHERS': [
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ],
        'EMAIL_BACKEND': 'django.core.mail.backends.locmem.EmailBackend',
        'CACHES': {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        },
        'CELERY_TASK_ALWAYS_EAGER': True,
        'CELERY_TASK_EAGER_PROPAGATES': True,
        'TEST_RUNNER': 'django.test.runner.DiscoverRunner',
    }
    
    # Apply test settings
    for key, value in test_settings.items():
        setattr(settings, key, value)
    
    # Initialize Django test runner
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    
    # Run tests
    failures = test_runner.run_tests(['combat_readiness'])
    
    # Exit with appropriate status code
    sys.exit(bool(failures))

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'combat_readiness.settings'
    import django
    django.setup()
    run_tests()
