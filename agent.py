"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import re

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
        "notice": None,              # set when the search came back empty
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    # 1. Start a session.
    session = new_session(query, wardrobe)

    # 2. Count each step, and check the count before taking it.
    count = 0

    count += 1
    trace.check_iterations(count)

    # 3. Parse the query (regex — see _parse_query).
    session["parsed"] = _parse_query(query)
    parsed = session["parsed"]

    # Invalid input is session["error"]: there is nothing to search for, so no
    # search runs. (An empty search result is a different case — see below.)
    if not parsed["description"]:
        session["error"] = (
            "I couldn't find what you're looking for in that. Describe the "
            "item, e.g. 'vintage graphic tee under $30, size M'."
        )
        return session
    if parsed["max_price"] is not None and parsed["max_price"] <= 0:
        session["error"] = "The max price has to be more than $0. Try a price like 'under $30'."
        return session

    # 4. Search.
    count += 1
    trace.check_iterations(count)
    session["search_results"] = search_listings(
        parsed["description"], parsed["size"], parsed["max_price"]
    )

    # THE BRANCH. Empty list: put the suggestion in session["notice"] and
    # return, so the user can take it or refine their search.
    # suggest_outfit is never called with nothing.
    if not session["search_results"]:
        session["notice"] = (
            f"No listings matched \"{parsed['description']}\". Let's try "
            f"something like '{FALLBACK_DESCRIPTION}', or refine your "
            f"description, size, or price and search again."
        )
        return session

    # 5. Non-empty list: the first (best) result is the item.
    session["selected_item"] = session["search_results"][0]

    # 6. Outfit.
    count += 1
    trace.check_iterations(count)
    session["outfit_suggestion"] = suggest_outfit(
        session["selected_item"], session["wardrobe"]
    )

    # 7. Fit card.
    count += 1
    trace.check_iterations(count)
    session["fit_card"] = create_fit_card(
        session["outfit_suggestion"], session["selected_item"]
    )

    # 8. Done.
    return session


# ── query parsing ─────────────────────────────────────────────────────────────

FALLBACK_DESCRIPTION = "leather boots"

_PRICE_AFTER_WORD = re.compile(
    r"(?:under|below|less than|up to|at most|max(?:imum)?(?: of)?|<=?)\s*\$?\s*(\d+(?:\.\d+)?)",
    re.IGNORECASE,
)
_PRICE_BARE = re.compile(r"\$\s*(\d+(?:\.\d+)?)")
_SIZE = re.compile(
    r"\bsize:?\s+(xxs|xs|xxl|xl|s|m|l|one size|us\s*\d+(?:\.\d+)?|w\d+(?:\s*l\d+)?)\b",
    re.IGNORECASE,
)


def _parse_query(query: str) -> dict:
    """
    Pull description, size, and max_price out of plain text with regex.

        "vintage graphic tee under $30, size M"
            -> {"description": "vintage graphic tee", "size": "M", "max_price": 30.0}

    Anything not found comes back as None. The description is what's left
    after the price and size phrases are cut out.
    """
    text = query

    max_price = None
    price = _PRICE_AFTER_WORD.search(text) or _PRICE_BARE.search(text)
    if price:
        max_price = float(price.group(1))
        text = text.replace(price.group(0), " ")

    size = None
    size_match = _SIZE.search(text)
    if size_match:
        size = size_match.group(1).strip().upper()
        text = text.replace(size_match.group(0), " ")

    description = re.sub(r"[\s,]+", " ", text).strip(" ,.")
    return {"description": description, "size": size, "max_price": max_price}


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    if session["notice"]:
        print(f"  stopped: {session['notice']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
