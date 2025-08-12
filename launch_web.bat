@echo off
echo.
echo ======================================================================
echo 🌐 AGRICULTURE AI SYSTEM - WEB DEPLOYMENT 🌐
echo ======================================================================
echo.
echo Starting web server for Agriculture AI System...
echo Once started, open your web browser and go to: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server.
echo ======================================================================
echo.

REM Launch the web server
"%LOCALAPPDATA%\Programs\Python\Python39\python.exe" web_api.py

echo.
echo ======================================================================
echo Web server stopped.
echo ======================================================================
pause
