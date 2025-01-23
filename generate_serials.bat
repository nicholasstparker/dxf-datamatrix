@echo off
SET VENV_DIR=.venv
SET REQUIREMENTS=requirements.txt

python --version || (
    echo Python is not installed or not in PATH. Please install Python or add it to PATH.
    pause
    exit /b 1
)

IF NOT EXIST "%VENV_DIR%\Scripts\activate" (
    echo Virtual environment not found. Creating one...
    python -m venv "%VENV_DIR%"

    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )

    echo Activating virtual environment and installing packages...
    call "%VENV_DIR%\Scripts\activate"

    REM Check if requirements.txt exists
    IF EXIST "%REQUIREMENTS%" (
        pip install -r "%REQUIREMENTS%"
        IF %ERRORLEVEL% NEQ 0 (
            echo Failed to install pip packages.
            pause
            exit /b 1
        )
    ) ELSE (
        echo No requirements.txt found. Skipping package installation.
    )
) ELSE (
    echo Activating existing virtual environment...
    call "%VENV_DIR%\Scripts\activate"
)

python main.py
IF %ERRORLEVEL% NEQ 0 (
    echo Python script failed with error code %ERRORLEVEL%.
    pause
    exit /b 1
)

deactivate