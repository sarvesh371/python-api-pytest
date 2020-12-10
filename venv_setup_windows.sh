export PYTHONHTTPSVERIFY=0
export PYTHON_VENV=venv
rm -rf $PYTHON_VENV
python -m pip install virtualenv
python -m virtualenv $PYTHON_VENV
source $PYTHON_VENV/Scripts/activate
python -m pip install -U pip
python -m pip install -U virtualenv
python -m pip install --progress-bar pretty --requirement requirements.txt
