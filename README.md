# Image Processing Project

## Project Overview

This project is a **FastAPI** application that performs image processing tasks. The app allows users to upload CSV files containing product names and image URLs. It processes images using **Celery** for asynchronous tasks and **MySQL** for data storage. The goal is to efficiently handle image data and track their status.

### Key Features

- **CSV Upload**: Upload a CSV file containing product names and image URLs.
- **Asynchronous Processing**: Process images in the background using Celery.
- **Database Integration**: Store product information and image URLs in MySQL.
- **Image Status**: Track the status of each product and image through the app.

---

## Requirements

- Python 3.7 or above
- FastAPI
- Celery
- MySQL
- Redis (for Celery message broker)

---

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/jyotibbdnitm/Image_processing.git
cd Image_processing


## API Endpoints

### 1. **POST /upload/**
- **Description**: Upload a CSV file containing product names and image URLs.
- **Request**: 
  - `file` (required): CSV file with columns (S.No, Product Name, Input Image URLs).
- **Response**: Returns a `request_id` for tracking the image processing.
  
**Example Request**:
```http
POST /upload/ HTTP/1.1
Content-Type: multipart/form-data
{
  "file": <CSV file>
}
