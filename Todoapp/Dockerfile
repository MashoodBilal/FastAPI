
FROM python:3.12
RUN pip install poetry
LABEL MAINTAINER="Mashood"
WORKDIR /code
COPY . /code/
RUN poetry install
EXPOSE 8000
CMD [ "poetry", "run", "uvicorn", "todoapp.main:app", "--host", "0.0.0.0" ]
