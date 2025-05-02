
FROM python:3.9-slim
WORKDIR /app
COPY client.py .
COPY templates/ ./templates/
RUN pip install flask requests
EXPOSE 5000
CMD ["python", "client.py"]
