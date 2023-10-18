# flask connecting postgres and using orm 

## Installation

```
python -m venv .venv

source /.venv
```

```
pip install -r requirement.txt

```

create .env file following .env_example


```
export FLASK_APP=app.py
```

## initializing the database and enabling migrations. 


```
 flask db init
 flask db migrate
 flask db upgrade
```

run flask

```
flask run
```