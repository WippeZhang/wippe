import ipinfo
from pprint import pprint

access_token = '2f313c870fad1f'
handler = ipinfo.getHandler(access_token)
ip_address = '52.56.247.107'
details = handler.getDetails(ip_address)

print(details.country_name, details.city)
