# -*- coding: utf-8 -*-
"""
THE SERVICE LIST — the single place where services, prices and durations live.

tools/build.py renders this into three places, so they can never drift apart:
  · the full list on the services page
  · the picker on the booking page
  · the drop-down on the booking and contact forms

TO CHANGE A PRICE OR DURATION, edit it here and run  python3 tools/build.py

Each entry is:  (name, duration, price, description)
  duration / price = None  means it still has to be supplied, and shows up on
  the site as a marked [[DURATION]] / [[PRICE]] placeholder.

Prices marked below were taken from the Roots of Care Setmore page.
"""

GROUPS = [
    ("locs", "Locks", None, [
        ("Loc consultation", None, None,
         "A sit-down to look at your hair and scalp and plan the right route — whether you are starting, switching loctician, or repairing."),
        ("Loc starting", None, None,
         "Comb coils, two-strand twists or interlocks, chosen for your texture and the loc size you want. Includes a full aftercare plan."),
        ("Retwist &amp; maintenance", None, None,
         "Root maintenance with light tension and a clean, even part. The regular appointment most clients book."),
        ("Retwist, wash &amp; deep condition", None, None,
         "The full maintenance visit: clarifying wash, deep conditioning, root maintenance and a proper dry."),
        ("Retwist + style", None, None,
         "Maintenance finished with a set style — barrel rolls, pipe cleaner curls, an updo or two-strand twists."),
        ("Interlocking maintenance", None, None,
         "Root maintenance by interlocking rather than palm rolling, for looser textures or very active lifestyles."),
        ("Loc repair", None, None,
         "Thinning roots, weak spots, married locs, breakage or loose ends. Assessed loc by loc and quoted before work starts."),
        ("No Retwist Styles", "30 min", "$25",
         "Styling in between retwists. Options include, but are not limited to, two-strand twists, three-strand twists, barrel twists and loc braids. "
         "<strong>An additional fee applies for more than 100 locs.</strong>"),
    ]),

    ("braids", "Braids &amp; twists", None, [
        ("Small Men&rsquo;s Twists on Natural Hair", "5 h", "$95",
         "Small twists on natural hair — 80 twists or more."),
        ("Medium Men&rsquo;s Twists on Natural Hair", "3 h 30 min", "$65",
         "Medium-sized twists on natural hair — roughly 50 to 65 twists."),
        ("Knotless braids", None, None,
         "Feed-in knotless braids installed with light tension at the root. Hair extensions not included unless arranged."),
        ("Box braids", None, None,
         "Classic box braids in the length and size of your choice."),
        ("Two-strand twists", None, None,
         "Twists on natural hair, with or without added length."),
        ("Cornrows", None, None,
         "Straight-back, feed-in or patterned cornrows, with or without extensions."),
        ("Children&rsquo;s braids", None, None,
         "Shorter, gentler sessions for children. Please mention the child&rsquo;s age when booking."),
    ]),

    ("henna", "Henna &amp; body art",
     "Henna and jagua prices may change with the complexity of the design — you will be told before any work starts. "
     "<strong>Do not book a jagua service if you have an allergy or sensitivity to berries, eucalyptus or lavender.</strong>",
     [
        ("Henna Paste — One Hand Design", "15 min", "$15",
         "A design on one hand, drawn freehand with natural henna paste."),
        ("Henna Paste — One Arm Sleeve", "35 min", "$45",
         "A full sleeve design on one arm, drawn freehand with natural henna paste."),
        ("Jagua Temporary Tattoo — One Hand", "15 min", "$20",
         "A one-sided hand design in jagua, which stains a deep blue-black rather than henna&rsquo;s reddish-brown."),
        ("Jagua Gel Temporary Tattoo — One Arm Sleeve", "35 min", "$60",
         "A full sleeve design on one arm in jagua gel, for a blue-black finish."),
        ("Henna — feet &amp; ankles", None, None,
         "Anklets, foot panels and toe detail. Feet hold the deepest stain."),
        ("Bridal henna", None, None,
         "A dedicated session for hands, arms and feet. Book two to three months ahead in peak season."),
        ("Events &amp; groups", None, None,
         "Parties, showers, festivals, Eid and Diwali gatherings, corporate events. Priced by the hour or per guest."),
        ("Hair henna treatment", None, None,
         "Henna as a natural conditioning treatment and colour for hair. A strand test is done first."),
    ]),

    ("care", "Treatments", None, [
        ("Clarifying detox wash", None, None,
         "A deep cleanse that lifts product build-up, mineral residue and lint from locs and natural hair."),
        ("Deep conditioning treatment", None, None,
         "A moisture treatment for dry, brittle or over-worked hair. Can be added to any appointment."),
        ("Scalp treatment", None, None,
         "A targeted treatment for dryness, flaking, tightness or tenderness after a previous style."),
        ("Wash &amp; dry", None, None,
         "A gentle wash and a full, proper dry — no retwist, no style. Useful between maintenance visits."),
    ]),
]

# Label shown on the category filter buttons
FILTERS = [("all", "All")] + [(cat, title) for cat, title, _note, _svcs in GROUPS]
