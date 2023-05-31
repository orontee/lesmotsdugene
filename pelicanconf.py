SITENAME = 'Les mots du Gène'
SITESUBTITLE = 'Planches gravées et sculptures par Eugène Vicat'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'fr'

STATIC_PATHS = ['images', 'videos', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

# Disable generation of some pages
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
# CATEGORY_SAVE_AS = ''
# CATEGORIES_SAVE_AS = ''
ARCHIVE_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
TAG_SAVE_AS = ''
TAGS_SAVE_AS = ''

DIRECT_TEMPLATES = []

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False

MENUITEMS = (
    ('Eugène Vicat', '/index.html'),
    ('Planches', '/pages/les-planches.html'),
    ('Sculptures', '/pages/les-sculptures.html'),
    ('Notes', '/pages/quelques-notes-a-propos-des-mots-d-eugene.html'),
    ("Association", '/category/l-association.html'),
)

# Blogroll
LINKS = (
    ('Contact', '/pages/contact.html'),
    ('Mentions légales', '/pages/mentions.html'),
)

# Social widget
SOCIAL = (
    ('You can add links in your config file', '#'),
    ('Another social link', '#'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'themes/lmdg'
