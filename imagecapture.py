import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

def download_image(url, filename):
  """Downloads an image from the given URL and saves it to the specified filename."""
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    with open(filename, 'wb') as f:
      f.write(response.content)
    print(f"Downloaded {url} to {filename}")

  except requests.exceptions.RequestException as e:
    print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
  urls = []
  i = 1
  while True:
    url = os.getenv(f"URL_{i}")
    if url is None:
      break
    urls.append(url)
    i += 1

  try:
    while True:
      for i, url in enumerate(urls):
        endpoint_folder = f"./images/endpoint_{i+1}" 
        os.makedirs(endpoint_folder, exist_ok=True) 
        filename = f"{endpoint_folder}/image_{int(time.time())}.jpg" 
        download_image(url, filename)
      time.sleep(60)  # Wait for 60 seconds

  except KeyboardInterrupt:
    print("\nStopped by user.")