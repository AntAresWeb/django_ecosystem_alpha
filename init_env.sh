python3.11 -m venv venv
source venv/bin/activate
python3.11 -m pip install --upgrade pip
pip install -r requirements.txt
python3 manage.py migrate
python3 productshop/manage.py runserver
