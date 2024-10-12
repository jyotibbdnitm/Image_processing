from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Read from environment variables or default values
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:0906@localhost/image_processing')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# You can also add other configurations like:
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
