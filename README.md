# Letterboxd Friend-Discovery Prototype

## The Problem
Letterboxd (30M+ users as of July 2026) offers only two ways to find friends on the platform: syncing an X/Twitter or Facebook account, or searching an exact username. There is no contact sync, QR code, or algorithmic "people you may know" suggestion system — unlike comparable platforms such as Instagram or Spotify. This is confirmed directly in [Letterboxd's own FAQ](https://letterboxd.com/about/faq/), and echoed in user complaints:

> "I find Letterboxd pretty boring because I can't find any of my friends on there. They only offer integration with X which I don't use."

## The Prototype
This repo contains a Python prototype simulating a **multi-signal "people you may know" algorithm**, combining three real-world signals into one weighted match score:

1. **Taste similarity** — Jaccard similarity on shared highly-rated films
2. **Location proximity** — same-city matching
3. **Mutual connections** — overlap in who users already follow

This mirrors how real recommendation systems (e.g. LinkedIn, Instagram) blend multiple signals rather than relying on a single one — and produces noticeably better suggestions than taste alone. In testing, adding location and mutual-connection signals surfaced two additional strong matches for a sample user that a taste-only version missed entirely.

## Files
- `friend_match.py` — v1: taste-based matching only (Jaccard similarity)
- `friend_match_v2.py` — v2: multi-signal matching (taste + location + mutual connections)

## Example Output
```
'People You May Know' suggestions for: new_user_lily
(currently follows: cinephile_casey)

1. arthouse_avery — match score: 71%
   Taste: you both liked Moonlight, Portrait of a Lady on Fire
   Location: both in Gainesville, FL
   Mutual: you both follow cinephile_casey
```

## Status
This is an active, ongoing project. Next steps: UX wireframes in Figma, competitive analysis write-up, and a process map comparing the current vs. proposed friend-adding flow.

## Author
Lily Gast — Information Systems, University of Florida
