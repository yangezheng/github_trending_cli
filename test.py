import requests

r = requests.get("https://api.github.com/search/repositories?q=created%3A%3E%3D2026-01-01&sort=stars&order=desc&per_page=10")
res = r.json()
print(res)