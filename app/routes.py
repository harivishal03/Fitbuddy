from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import markdown

from app.database import SessionLocal
from app.models import User

from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@router.post("/generate-workout")
def generate_workout(
    request: Request,
    user_id: str = Form(...),
    username: str = Form(...),
    age: int = Form(...),
    weight: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    try:
        workout_plan = generate_workout_gemini(
            age,
            weight,
            goal,
            intensity
        )
    except Exception as e:
        workout_plan = f"Workout generation failed: {str(e)}"

    try:
        nutrition_tip = generate_nutrition_tip_with_flash(goal)
    except Exception:
        nutrition_tip = "Nutrition tip unavailable. Gemini quota exceeded."

    workout_html = markdown.markdown(workout_plan)

    db: Session = SessionLocal()

    try:

        existing_user = db.query(User).filter(
            User.user_id == user_id
        ).first()

        if not existing_user:

            user = User(
                user_id=user_id,
                username=username,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
                original_plan=workout_plan,
                updated_plan=""
            )

            db.add(user)
            db.commit()

    except IntegrityError:
        db.rollback()

    finally:
        db.close()

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user_id": user_id,
            "username": username,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_html,
            "nutrition_tip": nutrition_tip
        }
    )


@router.post("/submit-feedback")
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):

    db: Session = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user:

        updated_plan = update_workout_plan(
            user.original_plan,
            feedback
        )

        user.updated_plan = updated_plan

        db.commit()

        updated_html = markdown.markdown(updated_plan)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user_id": user.user_id,
                "username": user.username,
                "goal": user.goal,
                "intensity": user.intensity,
                "workout_plan": updated_html,
                "nutrition_tip": generate_nutrition_tip_with_flash(
                    user.goal
                )
            }
        )

    db.close()

    return {"message": "User not found"}


@router.get("/view-all-users")
def view_all_users(request: Request):

    db: Session = SessionLocal()

    users = db.query(User).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users
        }
    )