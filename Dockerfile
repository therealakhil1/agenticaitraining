FROM python:3.9
WORKDIR /usr/local/app
COPY kube_test_app/ ./
RUN pip install fastapi uvicorn
EXPOSE 8000
CMD ["uvicorn",  "main:app",  "--reload", "--host", "0.0.0.0", "--port", "8000"]