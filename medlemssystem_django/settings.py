# Django project settings loader
import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# You can key the configurations off of anything - I use project path.
configs = {
    '/home/cyb/Documents/medlemssystem_django_nojs/medlemssystem_django': 'prod',
}

if not ROOT_PATH in configs:
    configs[ROOT_PATH] = 'dev'

# Import the configuration settings file - REPLACE projectname with your project
config_module = __import__('settings_{}'.format(configs[ROOT_PATH]), globals(), locals(), 'projectname')

# Load the config settings properties into the local scope.
for setting in dir(config_module):
    if setting == setting.upper():
        locals()[setting] = getattr(config_module, setting)
