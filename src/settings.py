import os
from utils.CourseUtils import CourseUtils


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_ROOT = os.path.join(PROJECT_ROOT, 'templates')
XSL_FILE = os.path.join(PROJECT_ROOT, 'xsl/openlearn2html.xsl')
BASE_COURSE = os.path.join(PROJECT_ROOT, 'base', 'BaseCourse')
BASE_SESSION = os.path.join(PROJECT_ROOT, 'base', 'BaseSession')
OUTPUT_PATH = ""
COURSE_DIR = ""



