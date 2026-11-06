"""Offline Rider–Waite–Smith reference data and secure random draws."""
from copy import deepcopy
from functools import lru_cache
from importlib.resources import files
import json
import secrets

LOCALES = ("zh-cn", "zh-tw", "en", "ja", "ko")

@lru_cache(maxsize=1)
def _deck():
    root = files(__package__).joinpath("data")
    deck = json.loads(root.joinpath("cards.json").read_text(encoding="utf-8"))
    waite = json.loads(root.joinpath("waite_pkt.json").read_text(encoding="utf-8"))
    return {c["slug"]: c for c in deck["cards"]}, waite

def _locale(locale):
    if locale not in LOCALES:
        raise ValueError("unsupported locale")
    return locale

def card(slug, locale="en"):
    _locale(locale)
    deck, waite = _deck()
    if slug not in deck:
        raise ValueError("unknown card slug; use listCards first")
    out = deepcopy(deck[slug])
    for key in ("image", "thumb"):
        out[key] = "https://shunshi.ai" + out[key]
    out["name"] = out["names"][locale]
    out["waite_1910"] = deepcopy(waite[slug])
    out["reference_url"] = "https://shunshi.ai/" + locale + "/tarot-cards/" + slug
    return out

def list_cards(locale="en"):
    _locale(locale)
    return [{"slug": c["slug"], "name": c["names"][locale], "arcana": c["arcana"], "suit": c["suit"]}
            for c in _deck()[0].values()]

def draw(positions, locale="en", allow_reversed=True):
    _locale(locale)
    if not 1 <= len(positions) <= 10 or any(not p.strip() or len(p) > 120 for p in positions):
        raise ValueError("provide 1–10 nonempty positions, each at most 120 characters")
    slugs = secrets.SystemRandom().sample(list(_deck()[0]), len(positions))
    out = []
    for position, slug in zip(positions, slugs):
        c = card(slug, locale)
        reversed_ = bool(secrets.randbelow(2)) if allow_reversed else False
        out.append({"position": position, "orientation": "reversed" if reversed_ else "upright", "card": c,
                    "selected_waite_meaning": c["waite_1910"]["reversed" if reversed_ else "upright"]})
    return out
