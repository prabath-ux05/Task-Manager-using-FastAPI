# Task Manager using FastAPI

This project is a fully functional Task Management REST API developed using **FastAPI**. It provides secure user authentication with **JWT**, supports **role-based permissions** for Admins, Managers, and Members, and enables smooth management of teams and tasks. The system allows users to create teams, assign members, create tasks, set priorities and deadlines, and maintain clear task progress with comments and activity logs. It also includes a lightweight analytics layer that provides insights such as completed vs pending tasks and team productivity. All data is stored using **SQLite** with **SQLAlchemy ORM**, and validated using **Pydantic v2** to ensure clean and structured input.

Create and activate a virtual environment:

--python -m venv venv
--source venv/Scripts/activate   # On Git Bash / Windows


Install the required dependencies:
--pip install -r requirements.txt


Run the development server:
--uvicorn main:app --reload


Your API will be available at:
http://127.0.0.1:8000

Interactive API documentation:
http://127.0.0.1:8000/docs

# Output
![Home Page](screenshots/home.png)

![Register Response](screenshots/register.jpg)

![Analytics Response](screenshots/analytics.jpg)

![Schemas](screenshots/schemas.jpg)
