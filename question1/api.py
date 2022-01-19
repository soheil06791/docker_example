from sanic import Sanic, response

app = Sanic("Api")

requests= {}
async def request_food(request):
    if 'client-key' not in dict(request.headers):
        return response.json({"state": requests})
    if dict(request.headers)['client-key'] not in requests:
        requests[dict(request.headers)['client-key']] = 1
    else:
        requests[dict(request.headers)['client-key']] += 1
    return response.json({"state": requests})


if __name__ == "__main__":
    app.add_route(request_food, "/", methods=["GET"])
    app.run(host="0.0.0.0", port=80)
