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
Notifications are sent to this address (automatically):
```python
API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id=@notifired'
```
Distribution channel used --> `@notifired`
*Please add it to telegrams or replace it with yours!*
