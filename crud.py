from sqlalchemy.orm import Session
from models import (
    User, Team, TeamMember, Task, Comment,
    ActivityLog, UserRole
)
from schemas import TaskCreate, CommentCreate, TeamCreate


def create_team(db: Session, team: TeamCreate, creator_id: int):
    new_team = Team(name=team.name, description=team.description)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    lead = TeamMember(team_id=new_team.id, user_id=creator_id, role=UserRole.admin)
    db.add(lead)
    db.commit()

    return new_team


def add_user_to_team(db: Session, team_id: int, user_id: int, role: UserRole):
    member = TeamMember(team_id=team_id, user_id=user_id, role=role)
    db.add(member)
    db.commit()
    return member


def create_task(db: Session, data: TaskCreate, team_id: int):
    task = Task(
        title=data.title,
        description=data.description,
        deadline=data.deadline,
        priority=data.priority,
        assigned_user_id=data.assigned_user_id,
        team_id=team_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    db.add(ActivityLog(task_id=task.id, message="Task created"))
    db.commit()

    return task


def add_comment(db: Session, task_id: int, user_id: int, data: CommentCreate):
    comment = Comment(
        task_id=task_id,
        user_id=user_id,
        message=data.message
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    db.add(ActivityLog(task_id=task_id, message="Comment added"))
    db.commit()

    return comment


def get_team_analytics(db: Session, team_id: int):
    total = db.query(Task).filter(Task.team_id == team_id).count()
    completed = db.query(Task).filter(Task.team_id == team_id, Task.completed == True).count()
    pending = total - completed
    high_priority = db.query(Task).filter(Task.team_id == team_id, Task.priority == "high").count()

    return {
        "total_tasks": total,
        "completed": completed,
        "pending": pending,
        "high_priority": high_priority,
    }
