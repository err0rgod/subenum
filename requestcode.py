import requests

url = "https://youtube.com"
try:
    response = requests.get(url)
    print(f"Response from {url}: {response.status_code}")

except requests.ConnectionError:
    print(f"Could not connect to the URL: {url}")


    