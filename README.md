# ak_notes

Backend for hypothetical Notes app as part of Artur Karapetov's assignment.  
This project requires python3.10  
Free tier of MongoDB Atlas used here

[![Maintainability](https://api.codeclimate.com/v1/badges/53f9891d099578172022/maintainability)](https://codeclimate.com/github/r-ss/ak_notes/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/53f9891d099578172022/test_coverage)](https://codeclimate.com/github/r-ss/ak_notes/test_coverage)


## Installing on a local machine

Clone repository:
```sh
git clone https://github.com/r-ss/ak_notes.git
cd ak_notes
```

Virtual Environment:
```sh
python3.10 -m venv env
source env/bin/activate
```

Install requirements:
```sh
pip install -r requirements.txt
```

You'll need to set env secrets:
```
SECRET_KEY as string
DBHOST_DEV as mongodb+srv URI with database credentials
```

Style Guide check:
```sh
flake8
```

Lint:
```sh
oitnb --exclude testutils\.py src
```
<small>one file here goes to exclude because it contains new python 3.10 match method which don't supported by linter yet.</small>

Test:
```sh
pytest -rP
```

Development server:
```sh
uvicorn main:app --reload --app-dir src
```

## What to discuss

1. Which pattern I got? MVC, MVP? or MVS? (Model-View-Shit)
2. 