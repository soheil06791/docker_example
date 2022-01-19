from sanic import Sanic, response
import redis
import json
import time
import asyncio

app = Sanic("Api")

db = redis.Redis(host='redis', port=6379)
db.set('state',json.dumps({}))

requests = {}

async def set_req(client, end_time):
    while time.time() <end_time:
        await asyncio.sleep(0.002)
    requests[client]['request'] = 0
    requests[client]['end_time'] = time.time() + 60
    requests[client]['set_req'] = False

async def request_food(request):
    if 'client-key' not in dict(request.headers):
        return response.json({"state": json.loads(db.get('state'))})
    state =  json.loads(db.get('state'))
    if dict(request.headers)['client-key'] not in state:
        state[dict(request.headers)['client-key']] = 1
        requests[dict(request.headers)['client-key']] = {}
        requests[dict(request.headers)['client-key']]['request'] = 0
        requests[dict(request.headers)['client-key']]['end_time'] = time.time() + 60
        requests[dict(request.headers)['client-key']]['set_req'] = False

    else:
        if time.time() < requests[dict(request.headers)['client-key']]['end_time'] and requests[dict(request.headers)['client-key']]['request'] == 10:
            if requests[dict(request.headers)['client-key']]['set_req'] == False:
                requests[dict(request.headers)['client-key']]['set_req'] = True
                asyncio.create_task(set_req(dict(request.headers)['client-key'],time.time()+60))
            return response.json({"message": f"Too many request from {dict(request.headers)['client-key']}"}, status = 429)
        if time.time() > requests[dict(request.headers)['client-key']]['end_time']:
            requests[dict(request.headers)['client-key']]['request'] = 0
            requests[dict(request.headers)['client-key']]['end_time'] = time.time() + 60
        requests[dict(request.headers)['client-key']]['request'] += 1           
        state[dict(request.headers)['client-key']] += 1
    db.set('state',json.dumps(state))
    return response.json({"state": json.loads(db.get('state'))})
    
if __name__ == "__main__":
    app.add_route(request_food, "/", methods=["GET"])
    app.run(host="0.0.0.0" , port = 80)