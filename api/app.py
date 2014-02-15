# -*- coding: utf-8 -*-
from frequencies import Frequencies
from textstats import TextStats
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

import json

corpus = Frequencies("en")

def process(nodes):
    stats = TextStats("en", corpus)
    for node in nodes:
        stats.add_node(node["text"], node["weighting"])

    stats.calculate_scores()
    words = stats.stats
    zsorted = sorted(words.values(), key=lambda k: k["z-score"], reverse=True) 

    return {"words":zsorted, "meta": stats.meta}


@Request.application
def application(request):
    results = {}
    mpa = dict.fromkeys(range(32))

    if request.method == "POST":
        data = request.data
        # Remove control characters
        data = json.loads(''.join(c for c in data if ord(c) >= 32))
        if "nodes" in data:
            results = process(data["nodes"])

    return Response(json.dumps(results), headers={"Content-Type": "application/json"})


if __name__ == "__main__":
    run_simple('localhost', 5000, application, use_reloader=True)
