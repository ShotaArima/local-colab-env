FROM python:3.13-bookworm

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

CMD ["sleep", "infinity"]