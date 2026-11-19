# NOTES: Basilica Holiday Home demo

## 1. Photos picked (from images/raw, all property-published)

The photo that sets the mood is **agoda-92fc44ac3c**: the two-storey stone villas at dusk, white circle-lattice breeze-block panels lit from inside, a red-purple sky over the tiled roofs. It shows what nobody else in Raiwood has: the facade itself. Its colours (wet basalt green from the garden, laterite red from the roofs and the pool deck, slate from the sky) became the palette, and the **circle lattice** became the site's single motif.

Supporting photos:
- The valley balcony with two drinks over monsoon-green forest (exp-516fc429). This sells "weekend from Mumbai".
- The oval pool against the wooded slope (wmg-Pool).
- The Lawn at night with rows of chairs under the palms (wmg-0F1A8625), and the floral ring stage in smoke (wmg-0F1A8626).
- The Lawn by day with round tables (wmg-2022 44pm), the Basilica hall set for a banquet (wmg-2022 38pm), an indoor stage with a red carpet (wmg-2022 52pm), and the terrace mandap (wmg-2022 45pm).
- Rooms: the deluxe room with towel swans (agoda-59742dd), the room opening onto a balcony (ta-18-34), and the yellow-curtained room (agoda-9d163f5638). Bungalow rooms (agoda-bung-*).
- The glass-walled restaurant facing the garden (exp-83b4c743), the lobby with the compass-rose marble floor (exp-51a83220), and the courtyard roundabout (exp-a7656ae3).

All are converted to AVIF and WebP at 480/800/1280 (and 1600 for the two big ones) by `site/make_images.py`.
Caveat: some WedMeGood photos carry a faint "WedMeGood" watermark in the corner. Ask the owner for the originals before launch.

## 2. What the best sites in this niche do (hill-station holiday homes and resorts near Mumbai/Pune)

1. **Dates and a "from" price in the first screen, with a reason to book direct.** Della Resorts, Fariyas and Rhythm Lonavala open with a booking bar. Smaller independents that rely on OYO, MakeMyTrip and Goibibo lose 15–25% per booking to commission. → The hero carries a booking card (check-in, check-out, guests, rooms) and the line "Rooms from ₹2,500 a night. Book direct and skip the app fees." A sticky bar keeps "Check dates", WhatsApp and Call one tap away.
2. **Room types sized for the group, each with a photo, who it sleeps and a price.** Lonavala weekends are families and friend groups from Mumbai and Pune. Sites that convert show villas and bungalows next to rooms, with headcount up front. → Rooms run from the deluxe garden-view room (sleeps 3) to the 4-bedroom bungalow (sleeps 15), each with "sleeps N" and a "from" price or a clear "rate on request".
3. **A separate events funnel with capacities and per-plate prices.** Resorts like Della and Lagoona earn a large share from weddings and offsites. Their sites list each space with seated/floating capacity and send planners to a date-and-headcount enquiry, not the room booker. → A dark "evening" section for the Lawn and the three halls with real capacities, ₹400 veg / ₹550 non-veg per plate, the catering, decor and DJ policies, and an enquiry form (date, guests, event type, space).

Also: WhatsApp first; drive times from Mumbai and Pune; nearby places with walk or drive times; house rules (check-in noon, check-out 10 am, no pets, ₹700 extra bed) written plainly.

## 3. Design directions (Stitch)

Stitch project: "Basilica Holiday Home Lonavala – homepage directions" (id 12220466598368974227, private, in Soham's Stitch account).

**Direction A: "Monsoon Ghats".** Light, rain-washed: plaster white, wet-basalt green #183324, laterite red #9E382A, slate mist #64748B. Newsreader for headings and Public Sans for text, 4–8 px radii, no shadows, and a **circle-lattice breeze-block strip** taken from the facade. Hero: the valley/dusk photo with the booking card on the first screen, then rooms → pool and restaurant → a dark weddings band → nearby. Stitch generated the full design system for it; it is exported to `design/tokens.json`.

**Direction B: "Lamps on at the Lawn".** A dark plum dusk page with a marigold accent and a fairy-light dot motif. The hero has two tabs, "Book a room" and "Plan an event", followed by big numbers.

_Stitch caveat:_ every generate call timed out on the client side, and `list_screens` returns nothing (the same as on the Voyage project). The Stitch web app isn't signed in inside the browser pane, so the screens can only be seen by opening the project in Soham's Stitch account. The project thumbnail Stitch saved (`design/stitch-B-ai-generated-thumbnail.png`) is from Direction B. It is an **AI-generated wedding scene with invented guests and mountains that aren't Lonavala**, not the property's lawn.

### Pick: A, "Monsoon Ghats"

1. **It comes from the place.** The palette and the lattice motif are taken from the building and its setting. B's dusk-and-fairy-lights look could belong to any wedding venue in India.
2. **Rooms are the everyday money, events are the big tickets.** A keeps room booking in the first screen and gives events a strong section of their own. B's "Book / Plan" tabs split attention in the hero, and dark pages make room photos look gloomy.
3. **B drifted.** Stitch filled it with an invented AI photo, which breaks the "real photos only" rule.

What A borrows from B: the **evening** feeling for the events section only. The events section switches to dark basalt green with the night-lawn photo, so the page "goes from day to evening" as you scroll. That is the one memorable idea: the stay by day, the celebration by night.

### Refinements made while building A
- The one orchestrated motion: the lattice circles in the hero's breeze-block strip "light up" one after another on load, like the facade windows at dusk. It is off under `prefers-reduced-motion`.
- Laterite red is used only for the primary booking action and prices. Basalt green is for structure. Slate is too light for small text on white, so a darker slate (#475569) is used for secondary text to meet AA.
- No all-caps labels and no pill buttons, as the Stitch system requires.

## 4. Checks (19 Nov 2026)

- Lighthouse mobile, served with the production `_headers` and gzip: **Performance 97, Accessibility 100, Best Practices 100, SEO 69**. LCP 2.6 s, CLS 0, TBT 0 ms.
  - SEO is 69 only because of the `noindex` meta, `X-Robots-Tag` and `robots.txt Disallow` that the demo rules require. With those removed, as they will be at launch, SEO is **100** (checked on a separate launch copy).
- No console errors, no failed requests and no broken images. No horizontal overflow at 390 px or 1440 px.
- The booking card ("Check dates" button and the "Rooms from ₹2,500 a night. Book direct and skip the app fees." line) is fully inside the first 390×844 screen, above the sticky WhatsApp / Call / Check dates bar.
- Keyboard: every control is reachable and has a visible focus ring (a laterite outline, or a green border and ring on fields). The demo dialog uses the native `<dialog>`, so Escape closes it and focus returns.
- Interactions tested: the weekend quick-dates, the night count, room-card "Check dates" (pre-selects the stay type and bungalow), the booking and enquiry demo dialogs, the headcount-to-space hint, and the click-to-load map (no Google requests until you ask).
- WedMeGood watermarks were cropped out of the pool, lawn, ring-stage and Basilica-hall images.
- Screenshots are in `screenshots/` (fold and full page, 390 px and 1440 px).
- Self-check: swap the logo and the page would still show Basilica's own lattice facade, its compass-rose lobby, the Lawn's real capacities and Raiwood distances. Without them it wouldn't work for another business.

## 5. Placeholders the owner must fill

Each shows on the site as a dashed "owner to add/confirm" tag.
1. Direct room rates for each type. Only "from ₹2,500" (WedMeGood) is shown now, and it is tagged.
2. The direct-booking offer (for example free breakfast or a set discount).
3. Which photo shows which room type (the Cottage and 1-bedroom-with-terrace photos are best guesses).
4. Check-out time: 10 am (Expedia, Agoda) or 11 am (Google, OYO).
5. Event packages: names, full veg / non-veg menus, and hall rental or minimum guarantee.
6. Photos of the Tulip and Orchid halls (they show a lattice placeholder now).
7. Restaurant name, timings and a short menu.
8. Email address.
9. Payment methods (is cash accepted?).
10. Room count (45 or 50) and the pool rules (adults-only or family).
11. Original photos without WedMeGood watermarks, plus anything better from the Facebook page.
12. At launch: the real domain in the canonical, og:image and schema URLs, and remove noindex.
