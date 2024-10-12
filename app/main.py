from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
import csv
import uuid
from app.database import get_db
from app.models import Product, Image
from app.celery_worker import process_image

# Initialize the FastAPI app
app = FastAPI()

# Define the CSV file upload route
@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        request_id = str(uuid.uuid4())

        # Read the file content
        content = await file.read()
        decoded_content = content.decode('utf-8').splitlines()
        reader = csv.reader(decoded_content)

        # Skip the header row
        next(reader)

        # Loop through the rows of the CSV
        for row_num, row in enumerate(reader, start=1):
            print(f"Row {row_num}: {row}")  # Debugging: print each row

            if len(row) < 3:
                raise HTTPException(
                    status_code=400,
                    detail=f"Row {row_num} is missing required columns: {row}"
                )

            product_name = row[1].strip()  # Product name in the second column
            input_image_url = row[2].strip()  # Image URL in the third column

            # Add product to the database
            product = Product(product_name=product_name, request_id=request_id)
            db.add(product)
            db.commit()

            # Add image to the database
            image = Image(product_id=product.id, input_image_url=input_image_url)
            db.add(image)
            db.commit()

            # Process image asynchronously using Celery
            process_image.delay(image.id)

        return {"request_id": request_id}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# Define the status check route
@app.get("/status/{request_id}")
def get_status(request_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.request_id == request_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    images = db.query(Image).filter(Image.product_id == product.id).all()

    return {
        "product_name": product.product_name,
        "status": product.status,
        "images": [{"input": img.input_image_url, "output": img.output_image_url, "status": img.status} for img in images]
    }
