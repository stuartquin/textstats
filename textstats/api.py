from frequencies import Frequencies
from textstats import TextStats

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

    res = sorted(words, key=lambda k: k[params["order_by"]], reverse=reverse) 
    return res[0:min(len(res), params["limit"])]

def process(data, args):
    # Remove control characters
    if "nodes" not in data:
        return {}

    params = get_parameters(args)
    stats = TextStats("en", corpus)

    nodes = data["nodes"]
    for node in nodes:
        stats.add_node(node["text"], node["weighting"])

    stats.calculate_scores()
    words = stats.stats
    results = apply_params(words.values(), params)

    return {"words":results, "meta": stats.meta}
