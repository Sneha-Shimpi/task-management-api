![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-black)
![SQLite](https://img.shields.io/badge/SQLite-Database-green)
![Render](https://img.shields.io/badge/Hosted%20on-Render-purple)
📋 Task Management API

A modern Task Management API built using Flask, SQLAlchemy, and SQLite, featuring a clean web interface for managing tasks with full CRUD functionality.

🌐 Live Demo

Application

https://task-management-api-1-t3bk.onrender.com/

📸 Application Preview
Dashboard
![Dashboard](images/home.png)
Create Task
![Create Task](images/create-task.png)
Edit Task
![Edit Task](images/edit-task.png)
Filter Tasks
![Filter](images/filter.png)
✨ Features
Create Tasks
Update Tasks
Delete Tasks
Task Status Management
Priority Levels
Responsive Interface
REST API
SQLite Database
Input Validation
Unit Testing
Postman Collection
🛠 Tech Stack
Technology	Purpose
Python	Programming Language
Flask	Backend Framework
SQLAlchemy	ORM
Marshmallow	Validation
SQLite	Database
HTML	Frontend
CSS	Styling
JavaScript	Client-side Logic
Pytest	Testing
Postman	API Testing
📂 Folder Structure
task-management-api/
│
├── app/
├── tests/
├── images/
├── requirements.txt
├── run.py
├── postman_collection.json
├── README.md
└── .gitignore
🚀 Installation
git clone https://github.com/Sneha-Shimpi/task-management-api.git

cd task-management-api

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt

python run.py
🌍 API Endpoints
Method	Endpoint	Description
GET	/api/tasks	Get all tasks
GET	/api/tasks/<id>	Get single task
POST	/api/tasks	Create task
PUT	/api/tasks/<id>	Update task
DELETE	/api/tasks/<id>	Delete task
🧪 Testing

Run

pytest -v
📁 Postman Collection

Import

postman_collection.json

into Postman to test every endpoint.

💡 Project Highlights
Flask Application Factory Pattern
SQLAlchemy ORM
Marshmallow Validation
Modular Folder Structure
RESTful API Design
Responsive Frontend
SQLite Database
Unit Tested
👩‍💻 Developer

Sneha Shimpi

GitHub:
https://github.com/Sneha-Shimpi

⭐ Future Improvements
User Authentication
JWT Authorization
PostgreSQL Integration
Docker Support
CI/CD Pipeline
Cloud Database
Dark Mode
📜 License

This project was created for educational and internship purposes.
