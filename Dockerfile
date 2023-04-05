# pull official base image
FROM python:3.10.10-alpine


RUN adduser -D worker
USER worker
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
ENV PATH="/home/worker/.local/bin:${PATH}"
RUN pip install --upgrade pip
COPY --chown=worker:worker ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY --chown=worker:worker . /usr/src/app/

EXPOSE 8000

ENTRYPOINT [ "gunicorn", "-w", "4", "'main:create_app()'" ]