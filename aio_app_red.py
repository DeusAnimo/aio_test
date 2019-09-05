import json
from aiohttp import web, ClientSession
from red_image import encoded_image
from models import Medias, session
from rand import uuid_url64
from count_func import red_count


EXAMPLE = 'https://s9.stc.all.kpcdn.net/share/i/12/10976186/inx960x640.jpg'


async def client_url(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            binary = await response.read()
            return await encoded_image(binary)


async def get_image(request):
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
    account_id = request.match_info.get('account_id')
    tag = request.match_info.get('tag')
    red_gt = request.match_info.get('red_gt')
    count = red_count(account_id=account_id, tag=tag, red_gt=red_gt)
    response_obj = {
        'medias': [{
            'count': count
        }]
    }
    return web.Response(status=200,
                        body=json.dumps(response_obj)
                        )


async def post_image(request):
    try:
        tag = request.query['tag']
        account_id = request.query['account_id']
        url = request.query['url']
        red = await client_url(url)
        media = Medias(account_id=account_id, tag=tag, red=red, image_id=uuid_url64())
        session.add(media)
        session.commit()

        user = session.query(Medias).filter(Medias.account_id == account_id).first()
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
    web.get('/images/count', count_image),
    web.post('/images', post_image),
    web.delete('/images/{image_id}', delete_image)
])

if __name__ == '__main__':

    web.run_app(app)
