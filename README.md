# ak_notes

Backend for hypothetical Notes app  
Part of Artur Karapetov's assignment as a practice with REST, FastAPI and Pydantic.  
This project requires Python 3.10  
Free tier of MongoDB Atlas used here

[![Maintainability](https://api.codeclimate.com/v1/badges/53f9891d099578172022/maintainability)](https://codeclimate.com/github/r-ss/ak_notes/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/53f9891d099578172022/test_coverage)](https://codeclimate.com/github/r-ss/ak_notes/test_coverage)

## December 1:

- CI/CD. With each commit, if the autotests pass successfully, the new version is rolled out to production ([aknotes.ress.ws/docs](https://aknotes.ress.ws/docs))

## November 16 - November 23:

- DAO. Without exception, all manipulations with the database now works through a separate layer of abstraction.
- Tags: CRUD, selection of notes by tag, etc.
- Got rid of ugly json parsing, Pydantic's from_orm methods are now used to parse objects from the database.
- The structure of URI addresses has been brought closer to the REST philosophy.
- Dataflow model changed to User → Category → Note → File.\
In the childrens there are no owner fields, in the parents the childrens are written in the form of an array.
- Filtering notes by fields, GET /notes?filter=milk
- Pagination. GET /notes?filter=lego&limit=10&offset=15
- Added refresh tokens for auth
- For uploaded files, write weight, mime-type, hash to the database
- Added tags for page /docs, descriptions of views
- Added PATCH methods to update records on a partially passed data model.
To update the full model, PUT is used (for example, PUT and PATCH are available for notes, the latter will work if, say, only the note title is passed for updating)

### Current dataflow model:

    ┌────────────┐    ┌────────────┐    ┌────────────┐
    │            │    │            │    │            ├────────────────────────┐
    │    User    ├───►│  Category  ├───►│    Note    │                        │
    │            │    │            │    │            ├────────┐               │
    └────────────┘    └────────────┘    └────────────┘        │               │
                                                              ▼               ▼
     uuid              uuid              uuid           ┌────────────┐  ┌───────────┐
     username          name              title          │    File    │  │    Tag    │
     hash              notes []          body           └────────────┘  └───────────┘
     categories []                       tags []
                                         files []        uuid            uuid
                                                         filename        name
                                                         size            color
                                                         mime



## Explore API

[aknotes.ress.ws/docs](https://aknotes.ress.ws/docs)

ask me for test user credentials

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
2. When files will be saved in AWS instead of local filesystem, can we call application as "stateless"?

## TODO

1. Save files in a cloud instead of local disk
2. On note deletion also remove all assotiated files
3. CI/CD. Currently docker build and docker run triggers manually
3. JSON parsing-unparsing in a some views does not looks good - needs to be refactored
4. Some restrictions for file uploads - by extension / mime-type / size