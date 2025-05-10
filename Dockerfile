FROM python:3.9
WORKDIR /usr/local/app
COPY kube_test_app/ ./
RUN pip install fastapi uvicorn
EXPOSE 8000
CMD ["uvicorn",  "main:app",  "--reload", "--port", "8000"]