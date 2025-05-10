FROM python:3.9
WORKDIR /usr/local/app
COPY kube_test_app/ ./
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn",  "app:app", "--host", "0.0.0.0", "--port", "8000"]