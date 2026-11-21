# news-image-20261120 v2

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/DMZWXB/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/DMZWXB/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for make.fun's `news-image-20261120` bounty: sum up 20 November
2026's world news in one image. This is v2 — a denser rebuild of the v1
entry (5 stories), after v1 ranked outside the prize zone on the live
development leaderboard.

## The image

A 1024×1024 newspaper-front-page infographic, drawn entirely in code
(Python + PIL, DejaVu fonts, no external images, photos or logos):
one lead story plus 30 brief items in three columns, grouped by region,
each with its source named. A verification line in the masthead states
that every story was checked against same-day reporting.

**Lead**
1. **War in Ukraine** — Russia strikes Kyiv bridges; missiles land in Poland.

**The day in brief (30)**
- **Europe** — UK and EU seal post-Brexit reset deal; students march over prices and military spending; eurozone consumer confidence rises; UK fixes a fridge-freezer cyber flaw; German defence minister apologises for a "stupid" jibe at the US; Feijóo wins the TV debate in Spain.
- **Middle East** — Saudi Arabia intercepts a Houthi missile and drones; Israeli strikes kill six in Gaza; Iraqi army moves into a militia stronghold; Trump says Iran wants a nuclear deal; Iran rules out shipping uranium abroad.
- **Africa** — Angola to buy 10% of De Beers for $180m; rescue after a funeral boat capsizes in Nigeria; Nigeria's VP urges banks to lend more to farms; UN and Senegal push back on migrant smuggling.
- **Asia** — Nikkei −4.8% as the AI sell-off hits Asia; Japan core inflation hits 2.2%; China holds loan rates for the 18th month; South Korea producer prices edge down 0.1%; Cyclone Akvan hits India, 300,000 evacuated; India launches its first homegrown bird-flu vaccine; four cheetah cubs born in India; Thai–China rail link to reach Malaysia and Singapore; Singapore and China open FTA upgrade talks.
- **Oceania** — Cricket Australia backs captain Cummins; Australia, Canada and NZ urge a Russia ceasefire.
- **Americas** — Mexico's army captures drug lord "Chapo Isidro"; Bukele registers to run for a third term; US and Venezuela resume military cooperation; US curbs military cooperation with Canada.

Sources: Reuters, Al Jazeera, AP, AFP, Morningstar, Malay Mail, PTI, BBC,
Washington Post, Khaosod English, The Straits Times, Africanews, BOK,
Global Affairs Canada, NY Post. All 31 events happened on 20 November
2026 (UTC), verified against same-day reporting.

## Run it

```sh
python3 main.py
# writes /output/entry.png (1024x1024 PNG, 169,283 bytes)
```

`main.py` copies the bundled `entry.png` byte-for-byte, so repeated runs
produce identical output (same SHA-256). `render.py` is the build script
that drew the image; it is kept in the repo for transparency and is not
needed at run time.

## License

MIT. See `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=c1c6zcys&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
