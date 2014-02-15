# Text Stats

A simple API which takes weighted chunks of text and performs tf-idf
calculation to produce ordered z-scores of phrases

*Note:* The score calculation is by no means perfect, use at your own risk

Thanks to http://invokeit.wordpress.com/frequency-word-lists/ for the great
word list and frequency data.

## Installation

Clone the repo, setup your virtualenv and run 

`pip install -r requirements`

## Running

`python .`

This will launch the app listening on port 5000

## Using

There is currently a single `POST` endpoint:

`http://localhost:5000/stats`

Which takes a JSON body:

```json
{
  "nodes": [
    {"weighting": 1, "text": "this is some test text to test the text stats"},
    {"weighting": 2, "text": "text stats test title"}
  ]
}
```

And responds with:

```json
{
    "meta": {
        "max_z_score": 1.5587513832241522,
        "min_z_score": -0.8420405880890874
    },
    "words": [
        {
            "is_stop": false,
            "word": "text",
            "idf": 4.182197640705562,
            "score": 0.5842977742873823,
            "weighted_frequency": 4,
            "tf": 0.2857142857142857,
            "z-score": 1.5587513832241522,
            "corpus_frequency": 1655
        },
        ...
    ]
}
```

### Query Params

Param     | Default
--------- | ---------
limit     | 10
order_by  | "z-score"
direction | "desc"
