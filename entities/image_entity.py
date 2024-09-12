# image_entity.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from entities.base import Base  # Import the shared Base

class ImageEntity(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True, index=True)  # Using the S3 object key as ID
    url = Column(String, nullable=False)
    user_email = Column(String, nullable=False)

    # Relationship to UserEntity
    #user = relationship("UserEntity", back_populates="images")

    def __init__(self, id: str, url: str, user_email: str):
        self.id = id
        self.url = url
        self.user_email = user_email

    def __str__(self):
        return f"ImageEntity(id={self.id}, url='{self.url}', user_email={self.user_email})"
