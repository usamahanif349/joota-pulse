# Joota Pulse

**Your customers are asking to buy. Nobody is answering.**
Joota Pulse finds the shoppers Pakistani footwear brands leave unanswered on YouTube, every week, and hands the marketing team the reply, the customer group and the next campaign.

**Live site:** https://usamahanif349.github.io/joota-pulse/ · **Free brand audit:** [Borjan](https://usamahanif349.github.io/joota-pulse/audit.html?brand=Borjan), [Servis](https://usamahanif349.github.io/joota-pulse/audit.html?brand=Servis), [Ndure](https://usamahanif349.github.io/joota-pulse/audit.html?brand=Ndure) and 5 more

![Joota Pulse](preview.jpg)

## What a brand gets

- **Missed sales:** buyers who asked about price, stock or delivery and never got a reply (an estimate you can adjust)
- **Leads inbox:** every waiting buyer, with a ready reply in Roman Urdu or English
- **Brand health score:** 0–100, ranked against 7 competitors every week
- **Alerts and a Monday digest:** new buyers, complaints and creator leads
- **Customer groups, campaign ideas and creators:** who is asking, what to post and who already sells for you
- **Client report and personal audit page:** one page per brand, downloadable as PDF

Covers Borjan, Servis, Ndure, Stylo, Metro, Hush Puppies, Insignia and ECS.

## How it stays live

A GitHub Action ([`refresh.yml`](.github/workflows/refresh.yml)) runs every Monday:

1. collects fresh public comments with the official YouTube Data API
2. re-runs the analysis engine and exports `data.json`
3. retakes the screenshots on the home page and republishes the site

`state/` remembers known videos, when each comment was first seen (so "new" means posted since the last update) and the weekly history. If YouTube collection ever fails, the site keeps last week's data.

**Accuracy rules:** a city, group or campaign figure is only shown when at least 5 comments back it; missed sales is labelled as an estimate; commenter names are never stored.

## Built with

HTML, CSS and JavaScript (no framework), Chart.js, GitHub Pages and GitHub Actions, Playwright for screenshots. The analysis (multilingual embeddings, clustering, anomaly detection, Spark benchmark) lives in **[pk-footwear-audience-engine](https://github.com/usamahanif349/pk-footwear-audience-engine)**.

Built by **Usama Hanif** · [LinkedIn](https://www.linkedin.com/in/usama-hanif-ai/) · Project 3 of the [Big Data Analytics course](https://github.com/usamahanif349/big-data-analytics-course), UMT.
Independent analysis of public YouTube comments; not affiliated with any brand shown.
