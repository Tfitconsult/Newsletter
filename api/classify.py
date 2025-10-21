import re
from collections import Counter

BUCKETS = {
    "policy": [
        "eu",
        "commission",
        "parliament",
        "subsidy",
        "mandate",
        "tax",
        "regulation",
        "incentive",
        "ban",
    ],
    "tech": [
        "battery",
        "solid-state",
        "lfp",
        "nmc",
        "anode",
        "cathode",
        "bms",
        "thermal",
        "motor",
        "ota",
        "chemistry",
    ],
    "experiences": [
        "road trip",
        "test drive",
        "service",
        "delivery",
        "winter",
        "charging",
        "preconditioning",
        "real-world",
        "ownership",
    ],
    "tips": [
        "how to",
        "trick",
        "tip:",
        "checklist",
        "etiquette",
        "pre-heat",
        "preheat",
        "tire",
        "insurance",
        "cost",
        "save",
    ],
}
NUMERIC_HINT = re.compile(r"(\d+\.?\d*|%|kWh|€)")
PREFERRED = ["experiences", "tips", "tech", "policy"]


def classify(text: str):
    tl = (text or "").lower()
    scores = Counter()
    for bucket, kws in BUCKETS.items():
        for kw in kws:
            if kw in tl:
                scores[bucket] += 1
    score = sum(scores.values()) + (1 if NUMERIC_HINT.search(text or "") else 0)
    if not scores:
        return "tech", 0.1
    best = sorted(scores.items(), key=lambda kv: (-kv[1], PREFERRED.index(kv[0])))[0][0]
    return best, float(score)


def propose_title_blurb(text: str):
    import re

    first_sentence = re.split(r"[.!?]", (text or "").strip(), maxsplit=1)[0]
    title = (first_sentence[:70] or "Update").strip().rstrip(":;")
    if len(title.split()) < 3:
        title = f"Update: {title}"
    blurb = re.sub(r"\s+", " ", (text or "").strip())
    if len(blurb) > 180:
        blurb = blurb[:177] + "…"
    return title, blurb
