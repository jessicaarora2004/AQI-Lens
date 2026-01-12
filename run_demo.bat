@echo off
REM ---- Activate virtual environment ----
call venv\Scripts\activate

REM ---- Start backend in new terminal ----
start cmd /k "cd backend && python -m uvicorn app:app --reload"

REM ---- Start frontend server in new terminal ----
start cmd /k "cd frontend && python -m http.server 5500"

REM ---- Wait 3 seconds for servers to start, then open browser ----
timeout /t 3
start http://127.0.0.1:5500
