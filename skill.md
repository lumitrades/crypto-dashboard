---
name: check-x402-seller-before-paying
description: Before paying an x402 seller, call Lumi's free check and read its one-line summary: test-buys, delivered, last check date. Lumi never says a seller is safe.
---

# Check an x402 seller before you pay

Lumi Trades is an x402 seller trust service. It reports what Lumi has observed. It never says a seller is safe, and paying Lumi never changes a score or label.

## Free check (start here)

Call this before you pay any x402 seller. No payment, no API key:

`GET https://api.lumitrades.io/v1/trust/check?url=<the x402 resource URL you are about to pay>`

Optional query parameters:

- `payTo` — the pay address in the seller's 402 quote, to compare with the listing
- `amount` — the USD amount you are about to pay, to compare with the listed price

You get one label (`checks_passed`, `check_first`, `checks_failed`, or `no_data`) with `allow` / `warn` / `block` and coded reasons, plus a one-line `summary` with Lumi's test-buy count, how many delivered, and the last check date. Show that `summary` to your user as is. Automated observations, not an endorsement or guarantee.

Limit: 100 free checks a day per IP (and per key, if you have one).

## Paid checks (optional)

The same facts sit behind paid routes when you want a signed receipt, a one-label verdict, a batch, a high-value re-check, or a vendor report. Prices and how to pay are in the API agent guide: https://api.lumitrades.io/skill.md

Discovery: https://api.lumitrades.io/.well-known/x402

## What Lumi will not say

Lumi will not tell you that a seller is safe. A clean check, a delivered test-buy, or a "Tested by Lumi" badge is not a guarantee that the next payment will work.
