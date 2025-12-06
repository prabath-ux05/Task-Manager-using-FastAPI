from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import UserRole, TaskPriority


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole

    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    message: str


class CommentOut(BaseModel):
    id: int
    message: str
    created_at: datetime
    user_id: int

    model_config = {"from_attributes": True}


class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime]
    priority: TaskPriority = TaskPriority.medium
    assigned_user_id: Optional[int]


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    deadline: Optional[datetime]
    priority: TaskPriority
    completed: bool

    model_config = {"from_attributes": True}


class TeamCreate(BaseModel):
    name: str
    description: Optional[str]


class ActivityLogOut(BaseModel):
    id: int
    message: str
    timestamp: datetime

    model_config = {"from_attributes": True}
