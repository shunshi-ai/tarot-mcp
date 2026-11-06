import pytest
from shunshi_tarot import card, list_cards, draw

@pytest.mark.parametrize("locale", ["zh-cn","zh-tw","en","ja","ko"])
def test_complete_deck(locale):
    cards = list_cards(locale)
    assert len(cards) == len({c["slug"] for c in cards}) == 78
    assert sum(c["arcana"] == "major" for c in cards) == 22
    for c in cards:
        detail = card(c["slug"], locale)
        assert detail["name"] and detail["waite_1910"]["upright"]

def test_missing_source_is_not_invented():
    assert card("two-of-cups")["waite_1910"]["reversed"] is None

def test_no_replacement_and_correct_meaning():
    for _ in range(20):
        result = draw([f"Position {i}" for i in range(10)])
        assert len({c["card"]["slug"] for c in result}) == 10
        for c in result:
            assert c["selected_waite_meaning"] == c["card"]["waite_1910"][c["orientation"]]

def test_reference_does_not_mutate_shared_data():
    c = card("the-fool")
    original = c["names"]["en"]
    c["names"]["en"] = "changed"
    assert card("the-fool")["names"]["en"] == original
