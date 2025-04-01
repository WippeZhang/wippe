import requests
import re


last_url = "https://en.greatfire.org/search/domains?page=0"
response = requests.get(last_url)
context = response.text
page = re.compile('<li class="pager-last last">.*page=(\d+)">')
context_find = page.findall(context)
last_page = context_find[0]
print(last_page)