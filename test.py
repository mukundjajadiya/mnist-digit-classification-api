import requests
url = 'http://192.168.0.127:81/'
img_file = {
    "files[]": open('img/1.png', 'rb'),
}
# r=  requests.get(url)
r = requests.post(url, files=img_file)
print(r.text)