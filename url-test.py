import requests

r = requests.get('https://doc.6wind.com/turbo-router-3/latest/turbo-router/')
print(r.text)