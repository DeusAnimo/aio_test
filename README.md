# Aio_test
Calculating red pixels in an image with [aiohttp](https://github.com/aio-libs/aiohttp)

## Getting started
This api is tested with Python 3.7+ and Pypy 3.
* Installation from source (git):
```
$ git clone https://github.com/DeusAnimo/aio_test.git
$ pip3 install -r requirements.txt
```
* Create db and run app:
```
$ python3 models.py
$ python3 aio_app_red.py
```
*Note: __check proxy__ availability and operation in the file __aio_app_red.py__*
```python
def send_message():
  requests.post(API_URL,
                proxies=dict(http='http://host:port',
                             https='https://host:port'),
                             data=json.dumps(message), headers=headers
                )
```
## Usage
To install / register webhook’s, you need to perform the following HTTP request:
```python
https://api.telegram.org/botTOKEN/setWebhook?url=https://YOUR.DOMAIN:PORT
```
Take __TOKEN__ from file __aio_app_red.py__

For domain verification I use: [ngrok](https://ngrok.com/download)

Put the file __ngrok.exe__ in the directory with the "app.py" and run:
```
$ ./ngrok http <our_server_port> 
$ ./ngrok http 8080
```
