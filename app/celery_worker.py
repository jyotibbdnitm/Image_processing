# app/celery_worker.py
from celery import Celery
import requests
from io import BytesIO
from PIL import Image as PILImage
from app.database import get_db
from app.models import Image
import re

celery = Celery('app.celery_worker', broker='redis://localhost:6379/0')

# A helper function to validate the URL format
def is_valid_url(url):
    return re.match(r'^https?://', url) is not None

@celery.task(bind=True)
def process_image(self, image_id):
    db = get_db()
    image = db.query(Image).filter(Image.id == image_id).first()

    if not image or not is_valid_url(image.input_image_url):
        print(f"Invalid URL or missing image: {image.input_image_url}")
        return  # Skip processing if the URL is invalid

    try:
        # Fetch the image
        response = requests.get(image.input_image_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            try:
                img = PILImage.open(BytesIO(response.content))
                print(f"Successfully processed image: {image.input_image_url}")
                # Further processing...
            except PILImage.UnidentifiedImageError:
                print(f"Cannot identify image: {image.input_image_url}")
        else:
            print(f"Failed to fetch image: {image.input_image_url}, status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {image.input_image_url}. Error: {e}")
