
FROM python:3.9-slim
WORKDIR /app
COPY load_balancer.py .
RUN pip install flask requests
EXPOSE 5000
CMD ["python", "load_balancer.py"]
