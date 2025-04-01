
import pprint
import nmap3

nm = nmap3.NmapScanTechniques(path=r"C:\Users\wippe\PycharmProjects\pythonProject\venv\Scripts\Nmap\nmap.exe")
results = nm.nmap_ping_scan('45.61.236.0/24',args='-sP')

# pprint.pprint(results)
# pprint.pprint(type(results))
for i in results:
    # pprint.pprint(results[i]['state']['reason'])
    try:
        if results[i]['state']['reason'] == 'echo-reply':
            print(i)
    except:
        pass