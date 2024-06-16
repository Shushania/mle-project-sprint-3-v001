import requests
import time

for i in range(100):
    response = requests.get('http://localhost:8000/test')
    if i % 10:
        time.sleep(10)
    time.sleep(2)