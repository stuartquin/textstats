# -*- coding: utf-8 -*-
from frequencies import Frequencies
from textstats import TextStats
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

import json

corpus = Frequencies("en")

valid_keys = ["z-score", "word", "is_stop", "tf", "idf", "corpus_frequency",
              "weighted_frequency"]

def get_parameters(args):
    params = {
        "order_by":  args.get("order_by", "z-score"),
        "limit": int(args.get("limit", 10)),
        "direction": args.get("direction", "desc")
    }

    if params["order_by"] not in valid_keys:
        raise Exception("Invalid order by")

    return params

def apply_params(words, params):
    reverse = False
    if params["direction"] == "desc":
        reverse = True

    results = sorted(words, key=lambda k: k[params["order_by"]], reverse=reverse) 
    return results[0:min(len(results), params["limit"])]

def process(request):
    data = request.data
    # Remove control characters
    data = json.loads(''.join(c for c in data if ord(c) >= 32))
    if "nodes" not in data:
        return {}

    params = get_parameters(request.args)
    stats = TextStats("en", corpus)

    nodes = data["nodes"]
    for node in nodes:
        stats.add_node(node["text"], node["weighting"])

    stats.calculate_scores()
    words = stats.stats
    results = apply_params(words.values(), params)

    return {"words":results, "meta": stats.meta}


@Request.application
def application(request):
    results = {}
    mpa = dict.fromkeys(range(32))

    if request.method == "POST":
        results = process(request)

    return Response(json.dumps(results),
                    headers={"Content-Type": "application/json"})


if __name__ == "__main__":
    run_simple('localhost', 5000, application, use_reloader=True)
