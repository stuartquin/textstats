# -*- coding: utf-8 -*-
from frequencies import Frequencies
from textstats import TextStats
import json

import flask
app = flask.Flask(__name__)

corpus = Frequencies("en")

def process(nodes):
    stats = TextStats("en", corpus)
    for node in nodes:
        stats.add_node(node["text"], node["weighting"])

    stats.calculate_scores()
    words = stats.stats
    zsorted = sorted(words.values(), key=lambda k: k["z-score"], reverse=True) 

    return {"words":zsorted, "meta": stats.meta}


@app.route("/stats", methods=["GET", "POST"])
def stats():
    results = {}
    mpa = dict.fromkeys(range(32))

    if flask.request.method == "POST":
        data = flask.request.data
        # Remove control characters
        data = json.loads(''.join(c for c in data if ord(c) >= 32))
        if "nodes" in data:
            results = process(data["nodes"])

    return flask.jsonify(results=results)


if __name__ == "__main__":
    app.run(debug=True)
