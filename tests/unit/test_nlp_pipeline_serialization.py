"""FT-F07: SentimentResult.to_dict() serialises aspects (asdict was never imported)."""

from eoip.nlp.pipeline import AspectSentiment, SentimentAnalyzer, SentimentResult


def test_sentiment_result_to_dict_serialises_aspects():
    result = SentimentResult(
        overall_score=0.5,
        overall_label="POSITIVE",
        aspects=[AspectSentiment(aspect="latency", score=0.9, label="POSITIVE", evidence="fast")],
    )
    assert result.to_dict() == {
        "overall_score": 0.5,
        "overall_label": "POSITIVE",
        "aspects": [{"aspect": "latency", "score": 0.9, "label": "POSITIVE", "evidence": "fast"}],
    }


def test_analyzer_output_round_trips_through_to_dict():
    out = SentimentAnalyzer().analyze("The search is fast and reliable but the setup is painful.",
                                      aspects=["search", "setup"])
    data = out.to_dict()
    assert set(data) == {"overall_score", "overall_label", "aspects"}
    assert all(set(a) == {"aspect", "score", "label", "evidence"} for a in data["aspects"])
