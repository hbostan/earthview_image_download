import requests
import json
import threading

base = "https://earthview.withgoogle.com"
pict = "/_api/nizip-turkey-1356.json"
data = json.loads((requests.get(base+pict)).text)
COUNT = 200
down = {}


def download_item(down_url, slug):
  pic_resp = requests.get(down_url, stream=True)
  if(pic_resp.status_code == 200):
    with open("photos/"+slug+".jpg", "wb") as f:
      for chunk in pic_resp.iter_content(1024):
        f.write(chunk)

def main():
  global base, pict, data, COUNT, down
  for i in range(COUNT):
    data = json.loads((requests.get(base+pict)).text)
    down_url = base + data['downloadUrl']
    slug = data['slug']
    if slug not in down:
      down[slug]=True
      th = threading.Thread(target=download_item, args=(down_url, slug))
      th.daemon = True
      th.start()
    pict = data['nextApi']
    print(i, slug)

if __name__ == "__main__":
  main()