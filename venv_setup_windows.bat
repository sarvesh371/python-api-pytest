set PYTHONHTTPSVERIFY=0
del /f /s /q venv 1>nul
rmdir /s /q venv
python -m pip install virtualenv
python -m virtualenv venv
CALL venv\Scripts\activate
python -m pip install -U pip
python -m pip install -U virtualenv
python -m pip install --progress-bar pretty --requirement requirements.txt