from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine
from models import UserRole
from schemas import UserCreate, UserLogin, TaskCreate, CommentCreate, TeamCreate
from auth import (
    get_db, register_user, authenticate_user,
    create_access_token, get_current_user, require_role
)
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advanced Task Manager")


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user.username, user.email, user.password)


@app.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"id": user.id})
    return {"access_token": token}


@app.post("/teams")
def create_team(team: TeamCreate, user=Depends(require_role(UserRole.admin)), db: Session = Depends(get_db)):
    return crud.create_team(db, team, creator_id=user.id)


@app.post("/teams/{team_id}/tasks")
def create_task(team_id: int, task: TaskCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_task(db, task, team_id)


@app.post("/tasks/{task_id}/comment")
def comment(task_id: int, msg: CommentCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.add_comment(db, task_id, user.id, msg)


@app.get("/teams/{team_id}/analytics")
def analytics(team_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_team_analytics(db, team_id)
