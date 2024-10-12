from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    request_id = Column(String, unique=True, index=True)
    status = Column(String, default="PENDING")

    images = relationship("Image", back_populates="product")


class Image(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True, index=True)
    input_image_url = Column(String)
    output_image_url = Column(String, nullable=True)
    status = Column(String, default="PENDING")
    
    product_id = Column(Integer, ForeignKey('products.id'))

    product = relationship("Product", back_populates="images")
