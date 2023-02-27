AUTHOR = 'Association «Les mots du Gène»'
SITENAME = 'Les mots du Gène'
SITESUBTITLE = 'Collection de planches gravées par Eugène Vicat'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'fr'

STATIC_PATHS = ['images', 'videos', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

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
    ('Notes', '/pages/quelques-notes-a-propos-des-mots-d-eugene.html'),
    ("Association «Les mots du Gène»", '/pages/presentation-de-l-association.html'),
)

# Blogroll
LINKS = (
    ('Contact', '/pages/contact.html'),
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
