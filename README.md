# Sweet Shop Management System
## 🚀 Live Demo

Backend API (FastAPI Swagger UI):  
👉 https://sweet-shop-kcz9.onrender.com/docs

This project is a simple Sweet Shop Management System developed as part of the assignment.

The application consists of a backend API built using FastAPI and a frontend built using React (Vite). The system allows users to view available sweets and purchase them. Stock updates are reflected immediately after purchase.

---

## Features

- View list of available sweets
- Display sweet name, category, price, and quantity
- Purchase a sweet (quantity decreases)
- REST API secured using JWT authentication
- Simple React-based frontend

---

## Tech Stack

### Backend
- Python
- FastAPI
- SQLite
- JWT Authentication
- Uvicorn

### Frontend
- React
- Vite
- JavaScript
- Fetch API

---

## Project Structure

sweet-shop/
│
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── auth.py
│ │ ├── models.py
│ │ ├── schemas.py
│ │ └── database.py
│ └── requirements.txt
│
├── frontend/
│ ├── src/
│ │ ├── App.jsx
│ │ └── api.js
│ ├── index.html
│ └── package.json
│
└── README.md


---

## How to Run the Project

### Backend

1. Navigate to backend directory:
cd backend
2. Activate virtual environment:
.venv\Scripts\activate
3. Start the server:
uvicorn app.main:app --reload --port 8000

4. Open Swagger UI:
http://127.0.0.1:8000/docs


---

### Frontend

1. Navigate to frontend directory:
cd frontend


2. Start development server:


npm run dev


3. Open browser:


http://localhost:5173


---

## Screenshots

A separate folder named `screenshots` is included in the project which contains:
- Backend API testing screenshots
- Swagger UI screenshots
- Frontend UI screenshots
- Purchase functionality proof


## Notes

- API authentication is handled using JWT tokens.
- Purchase operation updates the stock in real time.
- This project focuses on functionality and clarity.

