# -*- coding: utf-8 -*-
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

import json
import api

@Request.application
def application(request):
    results = {}
    if request.method == "POST":
        data = json.loads(''.join(c for c in request.data if ord(c) >= 32))
        results = api.process(data, request.args)

    return Response(json.dumps(results),
                    headers={"Content-Type": "application/json"})

def run():
    run_simple('localhost', 5000, application, use_reloader=True)
