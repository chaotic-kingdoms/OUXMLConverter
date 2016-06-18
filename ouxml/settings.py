import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
RESOURCES_PATH = os.path.join(PROJECT_ROOT, 'resources')
TEMPLATES_ROOT = os.path.join(RESOURCES_PATH, 'templates')
XSL_FILE = os.path.join(RESOURCES_PATH, 'xsl', 'openlearn2html.xsl')
BASE_COURSE = os.path.join(RESOURCES_PATH, 'base', 'course')
BASE_SESSION = os.path.join(RESOURCES_PATH, 'base', 'session')
TEMP_FOLDER = 'temp'

IMG_OPTIMIZED_WIDTH = 300

# Glossary image settings
GLOSSARY_THUMB_SIZE = (300, 220)
GLOSSARY_THUMB_FONT = os.path.join(RESOURCES_PATH, 'fonts', 'roboto.ttf')
GLOSSARY_BACKGROUND = (73, 85, 37)    # oppia dark color #495525
GLOSSARY_FOREGROUND = (154, 202, 60)  # oppia light color #9aca3c
GLOSSARY_TEXT_HORIZONTAL_PAD = 10
GLOSSARY_TEXT_MARGIN = 25
GLOSSARY_TEXT_FONTSIZE = 120
