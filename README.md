# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

1) search_listings(description, size, max_price)

+ Purpose: 
     = Searches and returns a listing based on the description, optionally can include size and max price of item as well. Only function that doesn't call the model.

+ Input: 
     = description --> str 
     = size --> str | None 
     = max_price --> float | None 

+ Returns: 
     = List --> dictionaries with matching listings, best match first. 
          + Key is the field name
          + Value are field values
     = If size and max_price are not given, then the best match should be an item with keywords in its description that best matches the description input. 
     = Else, if size and max_price is given, then the best match listing should have a description that shares keywords with the input descritpion, as well as having the closest corresponding sizes and max price (prioritize prices, and if prices are not close, then prioritize choosing best listing based on size.)

     Ex Listing: 

          {
          "id": "lst_002",
          "title": "Y2K Baby Tee — Butterfly Print",
          "description": "Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.",
          "category": "tops",
          "style_tags": ["y2k", "vintage", "graphic tee", "cottagecore"],
          "size": "S/M",
          "condition": "excellent",
          "price": 18.00,
          "colors": ["white", "pink", "purple"],
          "brand": null,
          "platform": "depop"
          }


+ If Empty...: 
     = Returns an empty list


2) suggest_outfit(new_item, wardrobe)

+ Purpose: 
     = Recommends one or two outfits given the user's wardrobe and thrifted item. Does call the model through generate(). 

+ Input: 
     = new_item --> listing dict
          + Key: Id or Title 
          + Value: Rest of the fields 
     = wardrobe --> wardrobe dict | Empty dict
          + Key: Items key
          + Value: A list of items
     
     Ex Wardrobe: 
          {
          "items": [
          {
               "id": "w_001",
               "name": "Baggy straight-leg jeans, dark wash",
               "category": "bottoms",
               "colors": ["dark blue", "indigo"],
               "style_tags": ["denim", "streetwear", "baggy"],
               "notes": "High-waisted, sits above the hip"
          },
          {
               "id": "w_003",
               "name": "White ribbed tank top",
               "category": "tops",
               "colors": ["white"],
               "style_tags": ["basics", "minimal", "fitted"],
               "notes": "Goes with everything"
          },
          {
               "id": "w_007",
               "name": "Chunky white sneakers",
               "category": "shoes",
               "colors": ["white"],
               "style_tags": ["sneakers", "chunky", "streetwear"],
               "notes": null
          }
          ]
          }


+ Returns: 
     = string with outfit suggestions 

+ If Empty...: 
     = Will just return general outfit advice


3) create_fit_card(outfit, new_item)

+ Purpose: 
     = Returns a description that people can post about the fit recommended

+ Input: 
     = outfit --> str
     = new_item --> listing dict  

+ Returns: 
     = two to four sentence caption or description about the outfit

+ If Empty...: 
     = Will still return a general description.
---

Additional Rules (Branch Loop): 
+ If search_listings returns an empty list: 
     a) Instead of raising a session["error"], the system sets to session["notice"] and recommends a description "let's try something like 'leather boots'" to the user instead, then returning the session. That way the user can either use the recommended search returned or refine their original description to get a non-empty list.
     
+ If search_listings returns with a non-empty list: 
     a) The non-empty list gets automatically inputted into suggest_outfit.

+ NOTE: Both scenarios call agent.py::run_agent.

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**
     + Given a description, and optionally a max price and ideal size, the function filters out items from load_listings() that do not match the desired description and given max price/size and only returns a list of dictionaries that closely match the description of the item and other constraints. Users have the option to not input a price ceiling or size, so long as they import a description.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
     + description (str)
     + size (str | None)
     + max_price (float | None)
- **Returns:**
     + Either a listing dictionary of items closely resembling the description (will also return items within desirable size and at/below max price if given).
     + ...
- **When it has nothing:**
     + Will return an empty list if the description is vague or doesn't align with descriptions of existing items returned by load_listings().
     + If no description is given, the tool by itself (without the branch loop in run_agent()) will return an error, requiring the argument 'description'.

### `suggest_outfit`

- **What it does:**
     + Takes an item from the listing dict returned by search_listings and a wardrobe dictionary (can be empty), using the model to generate 1 or 2 outfits using that item as a base. Unlike search_listing, this tool calls the model.
- **Inputs:**
     + new_item (dict)
     + wardrobe (dict)
- **Returns:**
     + Will return a string with outfit suggestions based on what exists within the wardrobe. 
- **When it has nothing:**
     + When inputting an empty wardrobe dict into the tool, will return general outfit advice based around the chosen item from listing dict. 

### `create_fit_card`

- **What it does:**
     + Takes outfit advice and the chosen item from list dictionary and generates a post-ready caption about the outfit. 
- **Inputs:**
     + outfit (str)
     + new_item (dict)
- **Returns:**
     + A string item with the detailed caption about the outfit
- **When it has nothing:**
     + This is entirely dependent on tool 2. create_fit_card() must have inputs ready in order to session to follow through with all three Tools. Therefore, if a wardrobe is not given in Tool 2, the second tool will generate general outfit advice. Tool 3 will just create a caption based around that general outfit advice that does not reference the wardrobe.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
+ Unclear description, search_listings will return a statement letting the user know their request is unclear, then recommend a prompt that will generate a listing dict that can pass onto the next tool.

**Where it lives:** `
+ Lives in agent.py::run_agent() --> starting from line 143

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
+ Used regex to parse description.

**What moves through the session:** <!-- which fields, in what order -->
     The session starts with a string query (a description), which then returns a listing dictionary. One item from that listing dictionary is then inputted into the second tool along side a given wardrobe, the tool then returns a string outfit suggestion. That string is inputted into the third tool along with the selected item from the listing dictionary from the first tool, which is then used to generate a postable caption. The branch loop happens if the query doesn't match any of the listings, asking the user to try another description until a wardrobe items can be passed onto the next tool. In case the wardrobe dict is empty, the second tool will instead pass a general outfit advice string, which can then be used to generate a caption when passed through the third tool.
---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under 30, size M'
{
  "query": "denim jacket under 50",
  "parsed": {
    "description": "denim jacket",
    "size": null,
    "max_price": 50.0
  },
  "search_results": [
    [
      "lst_007",
      "Denim Jacket — Light Wash, Cropped",
      "S",
      42.0
    ],
    [
      "lst_001",
      "Vintage Levi's 501 Jeans — Medium Wash",
      "W30 L30",
      38.0
    ],
    [
      "lst_004",
      "90s Track Jacket — Navy/White Stripe",
      "M",
      45.0
    ],
    [
      "lst_016",
      "High-Waisted Denim Shorts — Cutoff",
      "W27",
      24.0
    ],
    [
      "lst_032",
      "Shacket — Olive Canvas",
      "M/L",
      33.0
    ],
    [
      "lst_037",
      "Straight Leg Black Jeans — Faded",
      "W28",
      30.0
    ],
    [
      "lst_038",
      "Denim Vest — Medium Wash, Studded",
      "M",
      27.0
    ]
  ],
  "selected_item": {
    "id": "lst_007",
    "title": "Denim Jacket — Light Wash, Cropped",
    "description": "Cropped denim jacket in a light wash. Great structured shoulders. Blank canvas — no patches or pins but would be perfect to customize.",
    "category": "outerwear",
    "style_tags": [
      "denim",
      "vintage",
      "classic",
      "streetwear"
    ],
    "size": "S",
    "condition": "excellent",
    "price": 42.0,
    "colors": [
      "light blue"
    ],
    "brand": "Wrangler",
    "platform": "poshmark"
  },
  "wardrobe": {
    "items": []
  },
  "outfit_suggestion": "**Outfit 1: Off-Duty Monochrome**\n- Black ribbed tank top\n- High-waisted black wide-leg trousers\n- Black leather platform loafers\n- Silver hoop earrings\n*Vibe:* Effortless streetwear with a sharp, balanced contrast.\n\n**Outfit 2: Retro Contrast**\n- White graphic baby tee\n- Dark-wash straight-leg jeans\n- Retro canvas low-top sneakers\n- Tortoiseshell oval sunglasses\n*Vibe:* A nod to classic '90s casual with a modern, cropped silhouette.",
  "fit_card": "Scored this cropped light wash denim jacket on Poshmark for $42 and honestly haven't taken it off since. Loving how it pops against my black ribbed tank, high-waisted wide-leg trousers, and platform loafers for that effortless streetwear contrast. It’s giving major '90s casual when I throw it over a white graphic baby tee and dark-wash straight legs.",
  "error": null,
  "notice": null
}
--- empty wardrobe checks ---
wardrobe items: 0
outfit is non-empty str: True
fit card made: True
error: None | notice: None
(.venv) PS C:\Users\Owner\OneDrive\Desktop\CodePath!\AI201\ai201-project2-fitfindr-starter-v2026> 
(.venv) PS C:\Users\Owner\OneDrive\Desktop\CodePath!\AI201\ai201-project2-fitfindr-starter-v2026> python app.py ask "vintage graphic tee under 30, size M"
>> 

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1**
* Y2K Baby Tee — Butterfly Print
* Baggy straight-leg jeans, dark wash
* Brown leather belt
* Chunky white sneakers
* Black crossbody bag

*Vibe:* This balances the Y2K fitted crop top with relaxed denim for an effortless, nostalgic off-duty model look.

**Outfit 2**
* Y2K Baby Tee — Butterfly Print
* Wide-leg khaki trousers
* Vintage black denim jacket
* Chunky white sneakers
* Black crossbody bag

*Vibe:* A playful mix of earthy minimalism and early 2000s whimsy that feels fresh and street-style ready.

  Fit card: Found this little butterfly print baby tee on Depop for $18 and haven't taken it off since. Paired it with baggy dark wash straight-leg jeans, a brown leather belt, and chunky white sneakers for that effortless, nostalgic off-duty model look. Seriously living in this vibe right now.

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good','price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```
$ python -c "from tools import suggest_outfit; ..."

```
NORMAL VERSION: 
ITEM: lst_002 Y2K Baby Tee — Butterfly Print
str 777
**Outfit 1: Y2K Streetwear Contrast**
Pair the Y2K Baby Tee — Butterfly Print with the Baggy straight-leg jeans, dark wash. Cinch the waist with the Brown leather belt, and finish the look with the Chunky white sneakers and Black crossbody bag. 
*Vibe: This outfit balances the fitted, feminine butterfly graphic with ultra-relaxed denim for an effortless off-duty pop star aesthetic.*

**Outfit 2: Edgy Grunge Layering**
Wear the Y2K Baby Tee — Butterfly Print layered under the Vintage black denim jacket, paired with the Wide-leg khaki trousers. Ground the look with the Black combat boots and accessorize with the Black crossbody bag. 
*Vibe: The juxtaposition of a sweet, pastel baby tee with tough outerwear and earthy trousers creates the ultimate high-low vintage mix.*

EMPTY WARDROBE VERSION: 
**Outfit 1:**
- Mid-rise baggy cargo pants in olive green
- Chunky platform sneakers
- Pastel beaded shoulder bag

**Outfit 2:**
- Distressed light-wash denim skirt 
- Knee-high white boots
- Silver chain-link belt

**Vibe Check:** 
This look blends nostalgic Y2K pop-star energy with effortless everyday streetwear.

```
$ python -c "from tools import create_fit_card; ..."

```
NORMAL VERSION: 

ITEM: Y2K Baby Tee — Butterfly Print | 18.0 | depop | S/M
Scored this butterfly baby tee on Depop for just 18 bucks and I'm obsessed. Paired it with baggy dark-wash jeans and chunky white sneakers to balance out the tiny top energy. It's giving low-key 2000s streetwear without trying too hard.

EMPTY WARDROBE VERSION: 

Scored this butterfly print baby tee on Depop for just $18 and I am fully channeling my inner 2000s pop star today. Paired it with low-rise baggy cargo pants, chunky platform slides, and tinted wire-rims for that ultimate nostalgic streetwear energy.
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
     + When evaluating the rules I created for the branch loop, I asked Claude to test and see if it can understand the original branch loop I wrote. For the original branch loop, I intended for the first function to inform the user that their prompt was insufficient before proceeding with the rest of the function.
- *What came back:*
     + Claude was able to act as a partner programmer and tell me that if they were asked to write code based on my branch loop rule, it would not understand it; Claude then recommended a rule to help me better understand how to write branch loops.
- *What I changed:*
     + Claude was able to help refine my query, building on my understanding of how branch loops work, but one thing I changed that different from claude is what we raise if a query is vague and doesn't match the list descriptions. Claude initially proposed raising a session['error']. Instead I decided it would be best to return a statement that would allow the user to retry their query so the session can proceed onto the next tool. Claude refined this idea and decided to add another type of raised "error", session['notice'].

**Moment 2**

- *What I asked for:*
     + While working on the first Tool, search_listings(), I asked claude to go through the To Do list and write lines of code that align with the criteria I've established before programming (returning everything at or below max price if given and sizes that are at or +/- 1 in size away from the given size). I continued tailoring the logistics for the program, such as how the program should rank best options based on parsed key works and given price/size. 
- *What came back:*
     + Claude gave me exactly what I needed, I tested the code, and it fit the criteria I wrote. I tested the entire session with a query after Claude and I finished Tools 2 and 3, and I managed to get the best results I wanted using both a happy path and an empty path.
- *What I changed:*
     + Initially, I decided to include some lines of code to original function Claude returned, essentially reducing the list size of listing dicts from search_tools(). I believed this would make the list more concise and easier for users to choose items. However, when I asked Claude to test this, I quickly realized that this system won't work especially with more specific queries, and I decided not to shorten the returned listing dict.

- UNIT 4 UPDATE: 
     + When testing this program, Claude was useful in helping me understand how the program runs with an empty wardrobe. After Claude gave me a break down of what was outputted from Tool 2 and Tool 3, I asked Claude to fix run_agent() to identify and remind the user that these outputted strings and captions do not reference a wardrobe. Claude gave me a summary of what additional features I wanted to include, and I approved of the integration, including the additional idea Claude had about adding an extra branch that flags an empty wardrobe. After evaluating the code to confirm the changes, I ran the tests, and all test cases were met due to a fix on handling an empty wardrobe.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools  | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Input in one tool should equal output of previous tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5)|
| 4. Acceptable fit card answer and length | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Handling an empty wardrobe | 5 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
Criterion 1 Example Output: 

matching query completes  (example wardrobe)
  query: vintage graphic tee under $30
[1] [{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'],'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'VintageGraphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_003', 'title': 'Oversized Flannel Shirt — Plaid Red/Black', 'description': 'Classic oversized flannel. Great layering piece. A few tiny pulls in the fabric but nothing visible when worn.', 'category': 'tops', 'style_tags': ['grunge', 'vintage', 'flannel', 'streetwear', 'layering'], 'size': 'XL (oversized)', 'condition': 'good', 'price': 22.0, 'colors': ['red', 'black'], 'brand': 'Woolrich', 'platform': 'thredUp'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_013', 'title': '90s Silk Slip Dress — Floral,Midi Length', 'description': 'Delicate 90s slip dress in a muted floral print. Midi length, adjustable straps. Light snag on the side seam— not visible when worn.', 'category': 'bottoms', 'style_tags': ['90s', 'vintage', 'feminine', 'floral', 'cottagecore'], 'size': 'M', 'condition': 'good', 'price': 30.0, 'colors': ['ivory', 'dusty pink', 'green'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_014', 'title':'Leather Belt — Brown, Braided', 'description': 'Genuine leather braided belt. Adjustable, multiple holes. Classic Western buckle. Can be dressed up or down.', 'category': 'accessories', 'style_tags': ['vintage', 'western', 'classic', 'earth tones'], 'size': 'One Size (adjustable)', 'condition': 'excellent', 'price': 12.0, 'colors': ['brown'], 'brand': None, 'platform': 'thredUp'}]
      in:  ('vintage graphic tee', None, 30.0)
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] **Outfit 1**
- Y2K Baby Tee — Butterfly Print
- Baggy straight-leg jeans, dark wash
- Chunky white sneakers
- Black crossbody bag

*Vibe:* A quintessential Y2K street style look that balances the fitted, feminine butterfly tee with the relaxed, cool-girl energy of darkindigo denim.

**Outfit 2**
- Y2K Baby Tee — Butterfly Print
- Wide-leg khaki trousers
- Vintage black denim jacket
- Chunky white sneakers
- Brown leather belt

*Vibe:* An effortless mix of retro Y2K sweetness and structured earth-tone minimalism for a balanced weekend fit.
      in:  ({'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee …
      out: **Outfit 1** - Y2K Baby Tee — Butterfly Print - Baggy straight-leg jeans, dark wash - Chunky white sneakers - …
[3] Found this little butterfly print baby tee on Depop for $18 and haven’t taken it off since. Paired it with dark wash baggy straight-leg jeans and chunky white sneakers for that ultimate Y2K street style energy. Finished the whole fit off with my trusty black crossbody bag.
      in:  ('**Outfit 1**\n- Y2K Baby Tee — Butterfly Print\n- Baggy straight-leg jeans, dark wash\n- Chunky white sneake…
      out: Found this little butterfly print baby tee on Depop for $18 and haven’t taken it off since. Paired it with dar…
  try 1: completed — fit card 273 chars

FILE: agent.py 
FUNCTION: run_agent(query, wardrobe)

```
Criterion 2 Example Output

query: designer ballgown size XXS under $5
[1] []
      in:  ('designer ballgown', 'XXS', 5.0)
      out: [] (empty)
  try 1: stopped early (empty search) — No listings matched "designer ballgown". Let's try something...

FILE: agent.py 
FUNCTION: run_agent(query, wardrobe)

```
Criterion 3 Example Output

input in one tool equals output of second tool  (example wardrobe)
  query: denim jacket under $50
[1] in:  ('denim jacket', None, 50.0)
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 m...
     
[2] in:  ({'id': 'lst_007', 'title': 'Denim Jacket — Light Wash, Cropped', 'description': 'Cropped denim jacket in a line...})
      out: **Outfit 1** - Denim Jacket — Light Wash, Cropped - White ribbed tank top - Baggy straight-leg jeans, dark was…

FILE: agent.py 
FUNCTION: run_agent(query, wardrobe)
```
Criterion 4

[3] Scored these low-rise khaki cargo pants on Poshmark for $27 and honestly they were so worth it. Paired them with a white ribbed tank, black cropped zip hoodie, and chunky sneakers for the ultimate Y2K streetwear moment. Swapping the top for an oversized grey crewneck and combat boots gives it that perfect cozy, grunge-leaning 2000s street style.

FILE: tools.py 
FUNCTION: create_fit_card(outfit, new_item)
```
Criterion 5

[3] Scored these Off-White canvas sneakers on Poshmark for just $20 and the naturally yellowed soles give them the exact vintage look I wanted. Wearing them today with dark straight-leg jeans and an oversized heather grey crewneck for running errands. Later I swapped into olive green utility trousers and a black cropped boxy tee because they just go with everything.

FILE: tools.py 
FUNCTION: create_fit_card(outfit, new_item)
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4/5 | MET | Successfully ran through all three tools and returned the desired output 5 out of 5 times, exceeding initial expectations. The query was valid, and there was a wardrobe file the program was able to reference, returning a well-written fit card. |
| 2 | An impossible query stops before the second tool | 5/5 | MET | For every run under the second scenario, the program was able to identify if a query doesn't match any listings, returning a message informing the user of a query mismatch and requesting they try a different query. |
| 3 | Input in one tool should equal output of previous tool | 5/5 | MET | 5 out of 5 times, the program always takes the first listing from the outputted listing dict of search_listings() and inputs it as an argument for suggest_outfits(). |
| 4 | Acceptable fit card answer and length | 4/5 | MET | 5 out of 5 times, the program returns descriptions between 2-4 sentences (mostly 3 sentences in length) while also included detailed descriptions about the price and unique features of that outfit. |
| 5 | Handling an empty wardrobe | 5/5 | MISSED| The program does return a description related to the query, however, the description never includes a blurb about inputting a wardrobe for a more detailed description about the outfit. In fact, the program runs through all three tools instead of stopping the run and automatically returning a message recommedning the user inputs a wardrobe for more detailed advice. |

**Diagnoses**

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->
"""

**Happy path**

```
[1] [{'id': 'lst_003', 'title': 'Oversized Flannel Shirt — Plaid Red/Black', 'description': 'Classic oversized flannel. Great layering piece. A few tiny pulls inthe fabric but nothing visible when worn.', 'category': 'tops', 'style_tags': ['grunge', 'vintage', 'flannel', 'streetwear', 'layering'], 'size': 'XL (oversized)', 'condition': 'good', 'price': 22.0, 'colors': ['red', 'black'], 'brand': 'Woolrich', 'platform': 'thredUp'}, {'id': 'lst_024', 'title': 'Vintage Polo Shirt — Forest Green', 'description': 'Classic polo in forest green. Short sleeve, ribbed collar. Slightly boxy. The kind of piece that goes with everything.', 'category':'tops', 'style_tags': ['vintage', 'preppy', 'classic', 'earth tones'], 'size': 'M', 'condition': 'good', 'price': 18.0, 'colors': ['green', 'forest green'], 'brand': 'Ralph Lauren', 'platform': 'thredUp'}]
          in:  ('shirts', None, 30.0)
          out: 2 items: Oversized Flannel Shirt — Plaid Red/Black, Vintage Polo Shirt — Forest Green
     [2] **Outfit 1: 90s Grunge Layering**
     Wear the White ribbed tank top as a base, add the Oversized Flannel Shirt left unbuttoned, and pair with the Baggy straight-leg jeans, dark wash secured with theBrown leather belt. Finish with the Black combat boots and Black crossbody bag. 
     *Vibe:* Effortless 90s alternative rock nostalgia with a tough, edgy finish.

     **Outfit 2: Streetwear Contrast**
     Layer the Black cropped zip hoodie underneath the Oversized Flannel Shirt (worn buttoned halfway), paired with the Wide-leg khaki trousers and Chunky white sneakers. Complete the look with the Black crossbody bag.
     *Vibe:* A cozy, textured clash of streetwear and earthy minimalism that leans into skater culture.
          in:  ({'id': 'lst_003', 'title': 'Oversized Flannel Shirt — Plaid Red/Black', 'description': 'Classic oversized fla…
          out: **Outfit 1: 90s Grunge Layering** Wear the White ribbed tank top as a base, add the Oversized Flannel Shirt le…
     [3] Got this red and black flannel off thredUp for $22 and it’s basically my new uniform. Wore it open over a ribbed tank with baggy jeans and combat boots for some heavy 90s alt-rock energy. Later swapped it over a cropped hoodie and wide-leg khakis for that effortless skate-culture look.
          in:  ('**Outfit 1: 90s Grunge Layering**\nWear the White ribbed tank top as a base, add the Oversized Flannel Shirt…
          out: Got this red and black flannel off thredUp for $22 and it’s basically my new uniform. Wore it open over a ribb…

     Found:    Oversized Flannel Shirt — Plaid Red/Black — $22.0 on thredUp

     Outfit:   **Outfit 1: 90s Grunge Layering**
     Wear the White ribbed tank top as a base, add the Oversized Flannel Shirt left unbuttoned, and pair with the Baggy straight-leg jeans, dark wash secured with theBrown leather belt. Finish with the Black combat boots and Black crossbody bag. 
     *Vibe:* Effortless 90s alternative rock nostalgia with a tough, edgy finish.

     **Outfit 2: Streetwear Contrast**
     Layer the Black cropped zip hoodie underneath the Oversized Flannel Shirt (worn buttoned halfway), paired with the Wide-leg khaki trousers and Chunky white sneakers. Complete the look with the Black crossbody bag.
     *Vibe:* A cozy, textured clash of streetwear and earthy minimalism that leans into skater culture.

     Fit card: Got this red and black flannel off thredUp for $22 and it’s basically my new uniform. Wore it open over a ribbed tank with baggy jeans and combat boots for some heavy 90s alt-rock energy. Later swapped it over a cropped hoodie and wide-leg khakis for that effortless skate-culture look.

     2 model calls this session, 698 prompt + 233 output tokens
```

**Empty search**

```
[1] []
      in:  ('designer ballgown', 'XXS', 5.0)
      out: [] (empty)

  No listings matched "designer ballgown". Let's try something like 'leather boots', or refine your description, size, or price and searchagain.
```

**On the MCP move:** <!-- what changed in your code, and whether anything behaved differently afterwards. If the rewire didn't work, say exactly where it broke — the error text and the last thing that worked. That earns the point in full. -->

The rewire worked successfully. Every criteria I've established in the program was met including criterion 5, which didn't perform the way I wanted it to perform initially. What changed in my run_agent() code in agent.py is adding an extra branch called session["wardrobe empty"], which basically calls for generalized styling advice in the suggest_outfits() tool.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

In the function run_agent(query, wardrobe), I worked with Claude to integrate an additional branch that identifies an empty wardrobe and returns a general styling advice statement, followed by a disclaimer in parentheses that inform the user that this statement was generated with no wardrobe to reference. That disclaimer also reminds the user to input a wardrobe if they want advice that directly ties to their existing list of clothing items.

**Which failure it was meant to fix:**

Criterion 5 before the fix returned a string from tool 2 that doesn't remind the user that the description was generated without referencing a wardrobe. With this fix, the program will return a string along with the disclaimer.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 3. Input in one tool should equal output of previous tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 4. Acceptable fit card answer and length | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 5. Handling an empty wardrobe | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->

This fix definetely helped. It especially helped when the disclaimer was given as an output for both the Tool 2 string and the Tool 3 generated caption. This fix helped refine the program completely and performed exactly what I needed it to perform.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

NOTE: All tests have been passed, and cases that failed during the initial run have been fixed; these fixes ran successfully and met all my criteria.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [*] criteria.md has five numbered criteria, each with a target
       [*] Each criterion has a reason underneath it
       [*] All five unit 3 sections above have real content
       [*] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [*] Planning Loop names the branch rule and agent.py::run_agent
       [*] Sample Run: one full query plus the three per-tool tests, as text
       [*] At least four new commits
       [*] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [*] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [*] Run Log — Before, five criteria, five tries each
       [*] Real output pasted underneath, naming file and function
       [*] A verdict on every criterion
       [*] A diagnosis for every miss, naming a place AND a mechanism
       [*] Loop Trace, with the MCP call visible in it
       [*] All three failure modes triggered and handled
       [*] One improvement, with Run Log — After in the same format
       [*] What's Still Broken
       [*] At least four new commits
       [*] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
