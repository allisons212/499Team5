# Used for gcloud run build
FROM python:3.8
ENV PYTHONUNBUFFERED True


ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
COPY ./credentials ./credentials

RUN pip install Flask flask_navigation configparser werkzeug firebase-admin gunicorn
EXPOSE $PORT

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app