FROM python:3.8
COPY . /app
EXPOSE 5005
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "manage.py"]
