import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'my precious'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')


LDAP_HOST = '173.36.129.204'
LDAP_PORT = '389'
LDAP_DOMAIN = 'cisco.com'
LDAP_SEARCH_BASE = 'ou=active,ou=employees,ou=people,o=cisco.com'

#session management 
SESSION_PROTECTION = 'strong'

# HTTP session timeout (seconds)
SESSION_TIMEOUT = 3600

# Memory cache
MEMCACHED_URI = '127.0.0.1:11211'

