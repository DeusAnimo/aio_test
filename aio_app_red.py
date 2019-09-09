import json
from aiohttp import web
from red_image import encoded_image
from models import Medias, session
from count_func import red_count
import requests

TOKEN = '925360368:AAFSmEeIJx83kueu_ilb_SVD050SWlhXNxs'
API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id=@notifired'


def send_message():
    """
    send to telegram chanel @notifired
    use your proxies in the request post.
    :return:
    """
    last_post = session.query(Medias).order_by(Medias.id.desc()).first()
    headers = {
        'Content-Type': 'application/json'
    }
    message = {
        'text': f'😋 Account id: <b>{last_post.account_id}</b>\n'
        f'🏷️ Tag: <b>{last_post.tag}</b>\n'
        f'🆔 Image: <b>{last_post.image_id}</b>\n'
        f'🎯 RED: <b>{last_post.red} %</b>',
        'parse_mode': 'HTML'
    }

    requests.post(API_URL,
                  proxies=dict(http='http://203.160.175.178:8080',
                               https='https://203.160.175.178:8080'),
                  data=json.dumps(message), headers=headers
                  )


async def get_image(request):
    """
    :param request: search for parameters by 'image_id'
    :return: json response
    """
    image_id = request.match_info.get('image_id')
    user = session.query(Medias).filter(Medias.image_id == image_id).first()
    if not user:
        return web.Response(status=404,
                            body=json.dumps({'not found': 404}),
                            content_type='application/json'
                            )
    response_obj = {
        'medias': [{
            'image_id': user.image_id, 'red': user.red,
            'account_id': user.account_id, 'tag': user.tag
        }]
    }
    return web.Response(status=200,
                        body=json.dumps(response_obj),
                        content_type='application/json'
                        )


async def count_image(request):
    """
    :param request: user parameters, tag optional
    :return: int(count image.red > red_gt)
    """
    try:
        tag = None
        account_id = None
        if 'tag' in request.query:
            tag = request.query['tag']
        if 'account_id' in request.query:
            account_id = request.query['account_id']
        red_gt = request.query['red_gt']
        count = red_count(account_id, tag, float(red_gt))
        response_obj = {
            'medias': [{
                'count': count
            }]
        }
        return web.Response(status=200,
                            body=json.dumps(response_obj)
                            )
    except:
        return web.Response(status=404, text='Wrong parameters!')


async def post_image(request):
    """
    :param request: user parameters, tag optional
    :return: json object with saver data
    """
    try:
        account_id = request.query['account_id']
        tag = None
        if 'tag' in request.query:
            tag = request.query['tag']
        reader = await request.read()
        red = await encoded_image(reader)

        media = Medias(account_id=account_id, tag=tag, red=red)
        session.add(media)
        session.commit()
        send_message()

        user = session.query(Medias).filter(Medias.account_id == account_id)[-1]
        response_obj = {
            'medias': [{
                'image_id': user.image_id, 'red': user.red
            }]
        }
        return web.Response(status=201,
                            body=json.dumps(response_obj),
                            content_type='application/json'
                            )
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.Response(status=500,
                            text=json.dumps(response_obj)
                            )


async def delete_image(request):
    """
    :param request: 'url/image_id' for delete your image
    :return: status successful if the object is deleted
    """
    image_id = request.match_info.get('image_id')
    media = session.query(Medias).filter(Medias.image_id == image_id).first()
    if not media:
        return web.Response(status=404,
                            text=f"Image {image_id} doesn't exist"
                            )
    session.delete(media)
    session.commit()
    return web.Response(status=204)


app = web.Application()
app.add_routes([
    web.get('/images/{image_id}', get_image),
    web.get('/images/count/', count_image),
    web.post('/images', post_image),
    web.delete('/images/{image_id}', delete_image),
])

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=3030)
