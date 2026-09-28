from pydantic import BaseModel

class UserInput(BaseModel):
    user_id: str
    username: str
    age: int
    weight: int
    goal: str
    intensity: str

class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str