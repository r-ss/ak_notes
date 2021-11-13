FROM python:3.10

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

# RUN apt update

# RUN make /app
# ENV PORT 5000

ENTRYPOINT exec uvicorn main:app --port 5001 --app-dir src


# TUTORIALS

# Avoiding Permission Issues With Docker-Created Files
# https://vsupalov.com/docker-shared-permissions/