from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String, unique=True)
    username = Column(String)

    age = Column(Integer)
    weight = Column(Integer)

    goal = Column(String)
    intensity = Column(String)

    original_plan = Column(Text)
    updated_plan = Column(Text)