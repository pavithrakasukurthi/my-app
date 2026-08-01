FROM python:3.12-alpine
WORKDIR /opt/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py .
COPY templates ./templates
CMD ["app.py"]
ENTRYPOINT ["python"]