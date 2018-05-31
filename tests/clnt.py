import requests

code = requests.get('http://localhost:5000').text
exec(code)  # <-----