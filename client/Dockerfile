FROM python:3.9-slim

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "client.py"]