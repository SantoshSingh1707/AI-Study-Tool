@echo off
REM Windows batch script for running tests
REM Usage: run_tests.bat [--backend] [--frontend] [--coverage]

echo ============================================================
echo               Testing Runner (Windows)
echo ============================================================
echo.

SET BACKEND_ONLY=0
SET FRONTEND_ONLY=0
SET COVERAGE=0

IF "%1"=="--backend" SET BACKEND_ONLY=1
IF "%1"=="--frontend" SET FRONTEND_ONLY=1
IF "%1"=="--coverage" SET COVERAGE=1

REM Run Backend Tests
IF %BACKEND_ONLY%==1 (
    echo Running Backend Tests...
    cd backend
    call .venv\Scripts\activate || echo Virtual environment not found, using system Python
    pytest tests/
    cd ..
    goto :end
)

IF %FRONTEND_ONLY%==0 (
    echo Running Backend Tests...
    cd backend
    IF EXIST .venv\Scripts\activate (
        call .venv\Scripts\activate
    )
    pytest tests%COVERAGE% --cov=src%COVERAGE%
    cd ..
    echo.
)

REM Run Frontend Tests
IF %FRONTEND_ONLY%==1 (
    echo Running Frontend Tests...
    cd frontend
    npm test -- --run%COVERAGE%
    cd ..
    goto :end
)

IF %BACKEND_ONLY%==0 (
    echo Running Frontend Tests...
    cd frontend
    npm test -- --run%COVERAGE%
    cd ..
)

:end
echo.
echo ============================================================
echo Tests Complete!
echo ============================================================
pause
