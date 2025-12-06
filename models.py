from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

# --------- Enums ---------
class UserRole(enum.Enum):
    admin = "admin"
    manager = "manager"
    member = "member"

class TaskPriority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

# --------- Models ---------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.member)

    teams = relationship("TeamMember", back_populates="user")
    tasks = relationship("Task", back_populates="assigned_user")
    comments = relationship("Comment", back_populates="user")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    members = relationship("TeamMember", back_populates="team")
    tasks = relationship("Task", back_populates="team")


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(Enum(UserRole), default=UserRole.member)

    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="teams")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    deadline = Column(DateTime)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium)
    completed = Column(Boolean, default=False)

    team_id = Column(Integer, ForeignKey("teams.id"))
    assigned_user_id = Column(Integer, ForeignKey("users.id"))

    team = relationship("Team", back_populates="tasks")
    assigned_user = relationship("User", back_populates="tasks")
    comments = relationship("Comment", back_populates="task")
    logs = relationship("ActivityLog", back_populates="task")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    message = Column(Text)
    timestamp = Column(DateTime, server_default=func.now())

    task = relationship("Task", back_populates="logs")
