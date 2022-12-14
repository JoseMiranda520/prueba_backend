FROM python:3.7.4
ENV PYTHONUNBUFFERED 1

WORKDIR /api/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8004