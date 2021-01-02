FROM python:latest
RUN mkdir -p /duty_scheduler
WORKDIR /duty_scheduler
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000