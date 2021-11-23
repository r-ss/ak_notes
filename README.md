# ak_notes

Backend for hypothetical Notes app  
Part of Artur Karapetov's assignment as a practice with REST, FastAPI and Pydantic.  
This project requires Python 3.10  
Free tier of MongoDB Atlas used here

[![Maintainability](https://api.codeclimate.com/v1/badges/53f9891d099578172022/maintainability)](https://codeclimate.com/github/r-ss/ak_notes/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/53f9891d099578172022/test_coverage)](https://codeclimate.com/github/r-ss/ak_notes/test_coverage)

## 16 ноября — 23 ноября:

- DAO. Все манипуляции с БД через отдельный стой абстракции.
- Теги: CRUD, выбор заметок по тегу и т.д.
- Избавился от некрасивого распарсинга json, теперь используются методы Pydantic from_orm для парсинга объектов из бд.
- Структура URI-адресов приведена в более близкий к философии REST вид.
- Модель Dataflow изменена на User -Category -Note -File. В наследниках отсутствуют поля owner, в родителях записываются наследники в виде массива.
- Фильтрация заметок по полям, GET /notes?filter=pizda
- Пагинация. GET /notes?filter=huy&limit=10&offset=15
- Добавлены refresh-токены
- Добавил теги для странички /docs, описания вьюшек
- Добавлены методы PATCH для обновления записей по частично переданной модели данных. Для обновления по полной модели используется PUT (например для заметок доступны PUT и PATCH, последний будет работать если для обновления передан, скажем, только заголовок заметки)

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