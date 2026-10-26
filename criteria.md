# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<! 4 out of 5 times the program should be able to identify if the query is valid, and if it is, the agent will proceed with the loop. The 1 out of 5 times could happen if no wardrobe file is given, so the program would have to automatically return a general advice suggestion instead of going through all three tools. -->

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Should happen 5 out of 5 times; the significance of catching an invalid query earlier in the sequence can allow for the agent to use all three tools without difficulty.-->

---

## 3. Input in one tool should equal output of previous tool

Given an input for suggest_outfit() and create_fit_card(), new_item input has to exactly match any of the dictionary items in the listing dict output from search_listings (search_listings() will return a listing dictionary of various items, best match first, and the input for suggest_outfit() and create_fit_card() will be one of the several dictionary items returned). The function suggest_outfit() returns a string item later used as an input for create_fit_card(). That string item output from suggest_outfit() has to match the string outout input of create_fit_card(). All instances of matching input and outputs should work 5 out of 5 times.

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

**Why this target:**
<!-- Should happen 5 out of 5 times to allow for all three tools to run properly without raising an error. No room for the criteria to fail, since matching inputs and outputs from each tool allow for the agent to use all tools with no interruptions.-->



---

## 4. Acceptable fit card answer and length

Given the outfit suggestion input for create_fit_card(), the agent should return a caption that is minimum 2 sentences and max. 4 sentences, describing 2 key descriptors about the item, available sizes, and price of the item 4 out of 5 times. 

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->



**Why this target:**
<!-- Information regarding pricing or size will most likely not be available due to lack of information on pricing or size of an item.-->


---

## 5. Handling an empty wardrobe

Given an empty wardrobe, the agent should automatically return general outfit advice, then suggest the user inputs a file containing a wardrobe listing in case they want specifics on recommended outfits or a caption describing a recommended outfit. This process should occur 5 out of 5 times.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->



**Why this target:**

<!-- The agent should identify what path to take when given a wardrobe file or not. If not given a file, then the program should immediately be able to identify this and skip running the tools altogether. The agent should instead return general advice, then encourage the user to input the file in order to get access to all three tools and perform its functions.-->

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
