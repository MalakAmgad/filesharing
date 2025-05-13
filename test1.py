import requests
import time

for i in range(20):
    time.sleep(2)
    files = {'file': open('/Users/halasoliman/Desktop/Q1.docx', 'rb')}
    response = requests.post('http://localhost:8080/upload', files=files)
    print(f"Upload {i+1} response: {response.status_code}")
