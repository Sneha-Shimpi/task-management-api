![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![Render](https://img.shields.io/badge/Hosted%20on-Render-46E3B7?logo=render)
![License](https://img.shields.io/badge/License-MIT-green)

# 📋 Task Management API

A full-stack **Task Management Application** built using **Flask**, **SQLAlchemy**, and **SQLite**. The application allows users to create, update, delete, and organize tasks through a clean and responsive web interface while exposing RESTful API endpoints for task management.

---

## 🌐 Live Demo

🔗 **Application:**  
https://task-management-api-1-t3bk.onrender.com/

🔗 **GitHub Repository:**  
https://github.com/Sneha-Shimpi/task-management-api

---

## ✨ Features

- Create new tasks
- Edit existing tasks
- Delete tasks
- Update task status
- Set task priorities (Low, Medium, High)
- Filter tasks by priority
- Responsive and user-friendly interface
- RESTful API
- SQLite database integration
- Data validation using Marshmallow
- Unit testing with Pytest
- Postman collection for API testing

---

## 🛠️ Tech Stack

| Technology | Description |
|------------|-------------|
| Python | Programming Language |
| Flask | Backend Framework |
| SQLAlchemy | ORM |
| SQLite | Database |
| Marshmallow | Data Validation |
| HTML | Frontend |
| CSS | Styling |
| JavaScript | Client-side Logic |
| Pytest | Unit Testing |
| Postman | API Testing |
| Render | Deployment |

---

## 📂 Project Structure

```text
task-management-api/
│
├── app/
│   ├── static/
│   ├── templates/
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   ├── config.py
│   ├── extensions.py
│   └── __init__.py
│
├── tests/
├── images/
├── requirements.txt
├── postman_collection.json
├── run.py
├── README.md
└── .gitignore
```

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/Sneha-Shimpi/task-management-api.git
```

### Navigate to the Project

```bash
cd task-management-api
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python run.py
```

Open your browser and visit:

```text
http://localhost:5000
```

---

## 📮 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/tasks` | Retrieve all tasks |
| GET | `/api/tasks/<id>` | Retrieve a task by ID |
| POST | `/api/tasks` | Create a new task |
| PUT | `/api/tasks/<id>` | Update an existing task |
| DELETE | `/api/tasks/<id>` | Delete a task |

---

## 🧪 Running Tests

Run the test suite using:

```bash
pytest -v
```

---

## 📁 API Testing

A ready-to-use **Postman Collection** is included in this repository.

Import the `postman_collection.json` file into Postman to test all API endpoints.

---

## 🚀 Future Improvements

- User Authentication (JWT)
- PostgreSQL Support
- Docker Containerization
- CI/CD Pipeline
- Task Due Dates
- Search & Sorting
- Email Notifications
- Dark Mode

---

## 👩‍💻 Author

**Sneha Shimpi**

- **GitHub:** https://github.com/Sneha-Shimpi
- **Project:** https://github.com/Sneha-Shimpi/task-management-api
- **Live Demo:** https://task-management-api-1-t3bk.onrender.com/


## 📄 License

This project was developed for learning and internship purposes.
