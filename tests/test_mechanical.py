"""mechanical.py: deterministic checks."""
from scorers.naive import mechanical


def checks(result):
    return {f["check"] for f in result["findings"]}


def test_good_short_draft_passes():
    r = mechanical.check(
        "Hi Dana,\nSaw your crew just took on the Fremont remodel. "
        "Do you need a second drywall team for it?",
        recipient_context="Owner of a remodeling firm, just started the Fremont remodel",
    )
    assert r["score"] == 100
    assert "fremont" in r["recipient_terms_found"]


def test_long_cold_email_capped():
    r = mechanical.check("word " * 200 + "?")
    f = next(f for f in r["findings"] if f["check"] == "length")
    assert f["cap"]


def test_follow_up_ceiling_is_shorter():
    assert mechanical.check("word " * 80 + "?", message_type="follow_up")["findings"]
    assert not mechanical.check("word " * 80 + "?", message_type="cold")["findings"]


def test_no_ask_and_many_asks():
    assert "ask" in checks(mechanical.check("You will like this."))
    assert "ask" in checks(mechanical.check("You? You? You?"))


def test_sender_focused_draft_flagged():
    assert "you_i_ratio" in checks(mechanical.check("We are great. Our team is great. Can I call?"))


def test_no_recipient_detail_is_a_cap():
    r = mechanical.check("Do you want a demo?", recipient_context="Runs a bakery in Tacoma")
    f = next(f for f in r["findings"] if f["check"] == "personalization")
    assert f["cap"]


def test_company_name_alone_is_not_personalization():
    r = mechanical.check(
        "Hi Dana, Northside Remodeling looks great. Want a demo?",
        recipient_context="Dana owns Northside Remodeling in Seattle",
        recipient_name="Dana", recipient_company="Northside Remodeling",
    )
    assert "personalization" in checks(r)


def test_recipient_terms_skip_generic_words():
    terms = mechanical.recipient_terms(
        "Runs a 14-person shop in Tacoma. Spreadsheets aren't cutting it for scheduling.")
    assert terms == ["tacoma", "spreadsheets", "scheduling"]


def test_uniform_sentence_length_flagged():
    even = ("We build tools for busy teams. They save hours every single week. "
            "Our clients love the simple setup. Can we show you a demo?")
    assert "uniform_sentences" in checks(mechanical.check(even))


def test_varied_sentence_length_passes():
    varied = ("Saw the Fremont job. Scheduling two crews across three sites while "
              "the inspector keeps moving dates is brutal, and we fixed exactly that "
              "for a shop your size last spring. Worth ten minutes?")
    assert "uniform_sentences" not in checks(mechanical.check(varied))


def test_no_contractions_flagged():
    stiff = "I am writing because we are a good fit. It is quick. Do you want a call?"
    assert "no_contractions" in checks(mechanical.check(stiff))
    assert "no_contractions" not in checks(mechanical.check(
        "I'm writing because we're a good fit. It is quick. Want a call?"))
