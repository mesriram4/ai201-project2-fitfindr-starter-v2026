"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── size helpers ──────────────────────────────────────────────────────────────
# Letter sizes in order, so "one size away" means one step along this list.
SIZE_ORDER = ["xxs", "xs", "s", "m", "l", "xl", "xxl"]


def _size_parts(size: str) -> set[str]:
    """
    IMPORTANT NOTE: FUNCTION CREATED BY CLAUDE FOR SEARCH_LISTINGS()
    """
    """
    Break a size string into the whole sizes it names, lowercased.

        "S/M"                  -> {"s", "m"}
        "XL (fits oversized)"  -> {"xl"}
        "One Size / Oversized" -> {"one size", "oversized"}
        "W30 L30"              -> {"w30 l30", "w30"}
        "US 8.5"               -> {"us 8.5"}

    Parts are whole sizes, never substrings, so "s" can't match "us 9" and
    "l" can't match "xl".
    """
    cleaned = re.sub(r"\(.*?\)", "", size.lower())
    parts = {p.strip() for p in cleaned.split("/") if p.strip()}
    for part in list(parts):
        # "w30 l30" should also answer to a plain "w30" request.
        if re.fullmatch(r"w\d+ l\d+", part):
            parts.add(part.split()[0])
    return parts

def size_distance(listing_size: str, wanted: str) -> int | None:
    """
    IMPORTANT NOTE: FUNCTION CREATED BY CLAUDE FOR SEARCH_LISTINGS()
    """
    """
    How far a listing's size is from the requested one.

    Returns:
        0     the listing names the requested size (a range counts: "M" is a
              match for "S/M" and "M/L")
        1     the closest letter size in the listing is one step away on
              SIZE_ORDER (asking for "S" and the listing is "XS" or "M")
        None  anything else, including numeric sizes ("US 8", "W30"), which
              are only ever exact matches

    Use it as a tiebreaker when ranking, not as a filter: sort equally good
    keyword/price matches by this number, smallest first.
    """
    have = _size_parts(listing_size)
    want = _size_parts(wanted)
    if have & want:
        return 0
    want_idx = [SIZE_ORDER.index(w) for w in want if w in SIZE_ORDER]
    have_idx = [SIZE_ORDER.index(h) for h in have if h in SIZE_ORDER]
    if want_idx and have_idx:
        gap = min(abs(w - h) for w in want_idx for h in have_idx)
        if gap == 1:
            return 1
    return None


def size_matches(listing_size: str, wanted: str) -> bool:
    """
    IMPORTANT NOTE: FUNCTION CREATED BY CLAUDE FOR SEARCH_LISTINGS()
    """
    """True when the listing names the requested size exactly (distance 0)."""
    return size_distance(listing_size, wanted) == 0


# ── keyword helper ────────────────────────────────────────────────────────────

# Words that describe the request rather than the item.
_STOPWORDS = {
    "a", "an", "and", "the", "for", "with", "in", "on", "of", "to", "i", "me",
    "my", "want", "need", "looking", "find", "something", "under", "over",
    "below", "above", "less", "than", "max", "size", "price", "budget",
}


def _keywords(text: str) -> set[str]:
    """
    IMPORTANT NOTE: FUNCTION CREATED BY CLAUDE FOR SEARCH_LISTINGS()
    """
    """
    Lowercase whole words from `text`, minus stopwords and bare numbers, with a
    trailing plural "s" dropped so "jeans" and "jean" can meet.
    Whole words only: "tee" does not match "street".
    """
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {
        w[:-1] if len(w) > 3 and w.endswith("s") else w
        for w in words
        if w not in _STOPWORDS and not w.isdigit()
    }


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:

    """
    IMPORTANT NOTE: FUNCTION CONFIGURED BY CLAUDE
    """
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    # 1. Load every listing.
    listings = load_listings()

    # 2. Filter. Price is a hard ceiling (inclusive). Size keeps the exact size
    #    and anything one step away on SIZE_ORDER; size_distance is the
    #    tiebreaker when the results are ranked below.
    def size_gap(item: dict) -> int | None:
        return 0 if size is None else size_distance(item["size"], size)

    filtered = [
        item for item in listings
        if (max_price is None or item["price"] <= max_price)
        and size_gap(item) is not None
    ]

    # 3. Score what's left by keyword overlap with the description.
    keywords = _keywords(description)
    scored = []
    for item in filtered:
        searchable = " ".join([
            item["title"],
            item["description"],
            item["category"],
            " ".join(item["style_tags"]),
            " ".join(item["colors"]),
        ])
        score = len(keywords & _keywords(searchable))

        # 4. Drop anything scoring zero.
        if score > 0:
            scored.append((score, size_gap(item), item))

    # 5. Best score first; equal scores go to the closer size. sorted() is
    #    stable, so ties after that keep the order they have in the data.
    scored.sort(key=lambda s: (-s[0], s[1]))
    return [item for _, _, item in scored[:config.SEARCH_RESULT_LIMIT]]


def format_listings(listings: list[dict]) -> str:
    """
    Turn search_listings() output into text a person can scan. For printing and
    testing only — search_listings() itself still returns the list of dicts.

        print(format_listings(search_listings('graphic tee', max_price=30)))
    """
    if not listings:
        return "No listings found."

    blocks = [f"{len(listings)} listing(s), best match first:"]
    for rank, item in enumerate(listings, 1):
        brand = item.get("brand") or "no brand listed"
        blocks.append(
            f"\n{rank}. {item['title']}  [{item['id']}]\n"
            f"   ${item['price']:.2f} · size {item['size']} · "
            f"{item['condition']} · {item['platform']}\n"
            f"   {item['category']} · {brand}\n"
            f"   colors: {', '.join(item['colors'])}\n"
            f"   style:  {', '.join(item['style_tags'])}\n"
            f"   {item['description']}"
        )
    return "\n".join(blocks)


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────
def _describe_listing(item: dict) -> str:
    """One readable block for the prompt. Tolerates a missing brand."""
    lines = [
        f"- {item.get('title', 'Unknown item')} "
        f"(${item.get('price', '?')}, size {item.get('size', '?')})",
        f"- Category: {item.get('category', '?')}",
        f"- Colors: {', '.join(item.get('colors') or []) or 'not listed'}",
        f"- Style: {', '.join(item.get('style_tags') or []) or 'not listed'}",
        f"- Details: {item.get('description', '')}",
    ]
    if item.get("brand"):
        lines.insert(1, f"- Brand: {item['brand']}")
    return "\n".join(lines)

def _describe_wardrobe_item(piece: dict) -> str:
    """One wardrobe line: name, category, colors, style, and notes if any."""
    text = (
        f"- {piece.get('name', 'Unnamed piece')} "
        f"[{piece.get('category', '?')}; "
        f"{', '.join(piece.get('colors') or [])}; "
        f"{', '.join(piece.get('style_tags') or [])}]"
    )
    if piece.get("notes"):
        text += f" — {piece['notes']}"
    return text

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    item_text = _describe_listing(new_item)

    # 1. A wardrobe can be {"items": []} or just {} — both count as empty.
    wardrobe_items = (wardrobe or {}).get("items") or []

    if not wardrobe_items:
        # 2. Nothing to build from, so give general styling ideas for the item.
        system = (
            "You are a thrift-fashion stylist. The user has not entered a "
            "wardrobe, so do not pretend to know what they own."
        )
        prompt = (
            f"A shopper is considering this thrifted piece:\n{item_text}\n\n"
            "Suggest one or two outfits that would work with it, using general "
            "wardrobe staples (e.g. 'dark straight-leg jeans', 'white "
            "sneakers'). Name each outfit's pieces, then add one sentence on "
            "the overall vibe. Keep it under 120 words."
        )
    else:
        # 3. Put the wardrobe in the prompt and ask for pieces they already own.
        wardrobe_text = "\n".join(_describe_wardrobe_item(w) for w in wardrobe_items)
        system = (
            "You are a thrift-fashion stylist. Build outfits only from the "
            "pieces the user lists as owned, plus the new thrifted item."
        )
        prompt = (
            f"A shopper is considering this thrifted piece:\n{item_text}\n\n"
            f"Here is their wardrobe:\n{wardrobe_text}\n\n"
            "Suggest one or two outfits that combine the thrifted piece with "
            "items from this wardrobe. Name the wardrobe pieces exactly as "
            "listed, and do not invent items they don't own. Add one sentence "
            "on the vibe of each. Keep it under 150 words."
        )

    # 4. Return the model's answer, never an empty string.
    outfit = generate(prompt, system=system).strip()
    return outfit or (
        "Couldn't generate outfit ideas this time. Try pairing the piece with "
        "simple basics in a neutral color and let it be the statement."
    )


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    # 1. Nothing to write about: say so, don't raise and don't call the model.
    if not isinstance(outfit, str) or not outfit.strip():
        return (
            "No outfit was provided, so there's nothing to caption yet. "
            "Run suggest_outfit first and pass its result in."
        )

    # 2. Build the prompt from the listing and the outfit.
    title = new_item.get("title", "this piece")
    price = new_item.get("price")
    price_text = "an unlisted price" if price is None else (
        f"${price:.0f}" if float(price).is_integer() else f"${price:.2f}"
    )
    platform = new_item.get("platform", "a thrift app")
    size = new_item.get("size")
    vibe = ", ".join(new_item.get("style_tags") or []) or "not listed"

    system = (
        "You write short social captions for thrift finds. Sound like a real "
        "person posting a fit pic, not a product description."
    )
    prompt = (
        f"The find: {title}, {price_text} on {platform}"
        f"{f', size {size}' if size else ''}.\n"
        f"Its style tags: {vibe}.\n\n"
        f"The outfit it's styled in:\n{outfit.strip()}\n\n"
        "Write a caption of two to four sentences. Mention the item, its "
        "price, and the platform once each, and be specific about the vibe "
        "of the outfit. Use the outfit's actual pieces, not generic filler. "
        "No hashtags and no bullet points."
    )

    # 3. Return the model's caption, never an empty string.
    caption = generate(prompt, system=system).strip()
    return caption
    """
    return caption or (
        f"Found {title} for {price_text} on {platform} and I'm obsessed."
    )
    """
