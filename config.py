import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print BASE_DIR
# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + os.path.join(BASE_DIR,'app.db')

print SQLALCHEMY_DATABASE_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.getenv('CSRF_SESSION_KEY', 'abra-kadabra')

# Secret key for signing cookies
SECRET_KEY = os.getenv('SECRET_KEY', 'abra-kadabra')

BCRYPT_LOG_ROUNDS = os.getenv('BCRYPT_LOG_ROUNDS', 10)

# default token life to 2 hours
TOKEN_LIFESPAN_SEC = os.getenv('TOKEN_LIFESPAN_SEC', 7200)
