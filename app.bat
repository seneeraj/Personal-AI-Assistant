@echo off
echo ====================================
echo Starting Personal AI Assistant
echo ====================================

echo Starting Backend Server...
start cmd /k "uvicorn backend.main:app --host 0.0.0.0 --port 8010"

timeout /t 5

echo Starting Frontend (Streamlit)...
start cmd /k "streamlit run frontend/app.py"

echo.
echo Application started successfully!
echo Open your browser and go to:
echo http://localhost:8501
echo.

pause