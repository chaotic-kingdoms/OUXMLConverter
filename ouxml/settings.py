import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
RESOURCES_PATH = os.path.join(PROJECT_ROOT, 'resources')
TEMPLATES_ROOT = os.path.join(RESOURCES_PATH, 'templates')
XSL_FILE = os.path.join(RESOURCES_PATH, 'xsl', 'openlearn2html.xsl')
BASE_COURSE = os.path.join(RESOURCES_PATH, 'base', 'course')
BASE_SESSION = os.path.join(RESOURCES_PATH, 'base', 'session')
TEMP_FOLDER = 'temp'
