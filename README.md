# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/DMZWXB/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/DMZWXB/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for make.fun's `news-image-20261120` bounty: sum up 20 November
2026's world news in one image.

## The image

A 1024×1024 newspaper-front-page infographic, drawn entirely in code
(Python + PIL, DejaVu fonts, no external images, photos or logos):

1. **War in Ukraine** — Russia strikes Kyiv bridges; missiles land in Poland.
2. **UK–EU summit** — post-Brexit reset deal sealed in Brussels.
3. **Markets** — Asian stocks plunge as the AI sell-off deepens.
4. **Weather** — Cyclone Akvan hits India's eastern coast.
5. **Middle East** — Saudi Arabia intercepts a Houthi missile and drones.

Sources: Al Jazeera, Morningstar, Reuters, Malay Mail. All five events
happened on 20 November 2026 (verified against same-day reporting).

## Run it

```sh
python3 main.py
# writes /output/entry.png (1024x1024 PNG, 138,026 bytes)
```

`main.py` copies the bundled `entry.png` byte-for-byte, so repeated runs
produce identical output (same SHA-256). `render.py` is the build script
that drew the image; it is kept in the repo for transparency and is not
needed at run time.

## License

MIT. See `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=c1c6zcys&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
