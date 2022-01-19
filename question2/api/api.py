from sanic import Sanic, response
import json
import redis

app = Sanic("Api")

db = redis.Redis(host='redis', port=6379)
db.set('state',json.dumps({}))

async def request_food(request):
    if 'client-key' not in dict(request.headers):
        return response.json({"state": json.loads(db.get('state'))})
    state =  json.loads(db.get('state'))
    if dict(request.headers)['client-key'] not in state:
        state[dict(request.headers)['client-key']] = 1
    else:
        state[dict(request.headers)['client-key']] += 1
    db.set('state',json.dumps(state))
    return response.json({"state": json.loads(db.get('state'))})


if __name__ == "__main__":
    app.add_route(request_food, "/", methods=["GET"])
    app.run(host="0.0.0.0" , port = 80)
