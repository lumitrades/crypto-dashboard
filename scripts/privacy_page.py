"""/privacy/ (one per language): the privacy policy. Called from site_pages.build().
(Not to be confused with scripts/privacy.py, which scrubs paper-trade results from data files.)

Facts only, and every statement here mirrors the code. Keep it in sync when any of these change:
- newsletter: Kit list (no signup form on the site since Oct 25, 2026; existing subscribers only), email only
- analytics: Cloudflare Web Analytics beacon (build_pages.CF_BEACON), cookieless
- hosting: GitHub Pages (CNAME); no accounts, logins or comment forms
- third parties loaded by pages: Google Fonts, jsDelivr (Chart.js on /classic/), browser-side market data from Coinbase Exchange,
  (none since Oct 25, 2026: the market pages, live prices and referral links were retired)
- browser storage: localStorage lumi_lang + lumi_lang_hint (assets/i18n.js)
- agent API (lumi-api repo): src/traffic.ts (path, status, UA, referrer host, country, daily keyed IP hash, 90 days),
  src/sales.ts (payer wallet, amount, network, tx), src/trial.ts (wallet + daily IP hash), monitor/feed signups
  (migrations/0011: wallet, endpoints, optional webhook URL / email), tips and replies (src/trust)
- Lumi Check (lumi-api packages/scanner-kit = npm lumi-check, src/trust/contributors.ts, outcomes.ts, migrations 0016-0022):
  tier 1 off until yes (asked once after the first check), tier 2 receipts = chain + tx hash only, badge-only rewards
Never name a person. Contact: hello@lumitrades.io."""
import datetime as dt

import seo

UPDATED = dt.date(2026, 11, 19)   # bump when the policy text changes (shown on the page and in dateModified)
CONTACT = "hello@lumitrades.io"

LEDE = ("Lumi Trades runs this website (lumitrades.io) and the agent API (api.lumitrades.io). We collect as little as we can. "
        "This page lists what is collected, by whom and why. We do not sell personal data and we do not use advertising trackers.")
SECTIONS = [
    ("newsletter", "Newsletter", [
        "If you subscribed to the newsletter, the email address you entered is sent to Kit (ConvertKit), the email service "
        "that stores the subscriber list and sends the emails. It is used only to send "
        "the newsletter.",
        "Kit asks you to confirm the subscription by email, and every newsletter has an unsubscribe link: you can unsubscribe at any time. "
        "Like most email services, Kit may record delivery details such as whether an email was opened. Kit handles this data under its own privacy policy.",
    ]),
    ("analytics", "Analytics", [
        "The site counts visits with Cloudflare Web Analytics. It does not use cookies and does not follow you across websites. "
        "We only see aggregate numbers, such as page views, referring sites, countries and browser types.",
    ]),
    ("hosting", "Hosting", [
        "The website is a set of static pages hosted on GitHub Pages. GitHub may log visitors' IP addresses and request details to run "
        "and secure its service, under GitHub's privacy statement. The site has no accounts, logins or comment forms.",
    ]),
    ("third-parties", "Third-party content and links", [
        "Pages load fonts from Google Fonts. The vendor trust pages fetch the latest test results from Lumi's own API "
        "(api.lumitrades.io); like any web request, this sends your IP address and browser details to that service. "
        "Nothing from X, YouTube or TikTok is embedded; they are plain links. "
        "Once you follow a link to another site, that site's privacy policy applies.",
    ]),
    ("browser", "Stored in your browser", [
        "This site sets no cookies. Your browser keeps your language choice and whether you dismissed the language suggestion (local storage). "
        "You can clear them in your browser settings.",
    ]),
    ("api", "The agent API (api.lumitrades.io)", [
        "The API runs on Cloudflare Workers. To operate it, it keeps a private traffic log: for each request, the path (without the query string), "
        "the status code, the user agent, the referring site, the country and a keyed hash of the IP address that changes every day. "
        "Raw IP addresses are not stored, and traffic records are deleted after 90 days.",
        "Payments are made on public blockchains. For each paid call the API records the payer's wallet address, the amount, the network and the "
        "transaction ID, which are public on the ledger anyway. Free trial calls record the wallet that signed in and a daily IP hash, to enforce the limits.",
        "If you sign up for seller monitoring or the data feed, the API stores what you submit: your wallet address, your endpoints and, "
        "if you add them, a webhook URL or an email address for alerts. That email address is used only for those alerts and is never shown publicly. "
        "Reports, seller replies and tips sent to the API are stored as submitted (reports and tips with a hashed IP address, to limit abuse); tips are never published.",
    ]),
    ("sharing", "No selling of data", [
        "We do not sell, rent or trade personal data. We share it only with the service providers named on this page, as far as they need it "
        "to run the site, the newsletter and the API, or when the law requires it.",
    ]),
    ("choices", "Your choices and contact", [
        "To unsubscribe from the newsletter, use the link in any email. To ask what we hold about you, or to have it corrected or deleted, "
        "email <a href=\"mailto:{mail}\">{mail}</a>. Payments recorded on a public blockchain cannot be changed or deleted by anyone.",
        "The site is not aimed at children. If this policy changes, this page is updated and the date at the top changes.",
    ]),
]
# Lumi Check section (after "api"). Trusted, hand-written HTML (<strong>, <code>, mailto links), so it is not escaped.
# Kept in English on every language page for now (marked lang="en", with a translated note) so the policy wording is exact;
# translate it into the i18n catalogs and move it into SECTIONS when ready.
LUMI_CHECK_ID, LUMI_CHECK_HEAD = "lumi-check", "Lumi Check"
LUMI_CHECK_NOTE = "This section is in English only for now."
LUMI_CHECK = [
    "Lumi Check is a free check an agent can run before it pays an x402 seller. It answers allow, warn or block, shown as one label (Delivered in recent checks, Check first, Recent checks failed or Not enough data), with reasons, the seller's score and a link to the live report. The answer is signed by Lumi so the agent can verify it.",
    "<strong>Checks.</strong> When you run a check, the kit sends only the seller URL's origin and path (any query string is removed before it leaves your machine), or the seller's pay-to address, plus the price if you give one. We don't store who checked what. A checked seller that shows a warning signal may be queued for a test-buy. Short-lived counters (for rate limits) are kept in memory and are not stored.",
    '<strong>What the kit shares. Tier 1, off until you say yes:</strong> nothing is sent before you agree. Right after your first check, the kit asks once: &ldquo;Share your results to help improve Lumi\'s public trust list? [Y/n]&rdquo;. Your answer is saved only on your computer, and the question is not shown again. Where the kit cannot ask (no terminal, CI, the MCP server or code), sharing stays off. If you say yes, after a paid call the kit sends one anonymous delivery outcome: the seller\'s host name or Lumi endpoint ID, whether the data was delivered (yes or no) and optionally a coarse status class (for example 2xx, 5xx or timeout). Each report carries a new random token that is used once to drop duplicates and cannot be linked to you or to your other reports. It never includes your wallet, the amount, the transaction hash, the query string, the response, or any stable ID. Tier 1 reports are counted only; they never change a seller\'s score. To change your answer at any time, run <code>lumi-scan telemetry on</code> or <code>lumi-scan telemetry off</code>, set <code>LUMI_CHECK_TELEMETRY=on</code> or <code>off</code>, or set <code>"telemetry": true</code> or <code>false</code> in the kit\'s config file.',
    "<strong>Tier 2, off by default:</strong> sharing full signed receipts. Nothing is sent unless you turn it on (<code>lumi-scan sharing on</code> or <code>LUMI_SHARE_RECEIPTS=1</code>). Each shared receipt includes the payment's transaction ID. A transaction ID is public on its blockchain: anyone who has it can look it up and link it to the wallet that paid and the amount. If you take part, the API stores what you register and submit: a label you choose, your contributor public key, the wallet addresses you pay from, any domains you tell us you own, and the wallet that first funded each registered wallet (read from the public ledger, used to tell independent contributors apart). Your contributor private key and wallet secrets stay on your machine and are never sent to us.",
    "For each receipt you share we store the receipt and the test data in it: the seller endpoint (origin and path only) and the seller's pay-to address, the payment's network and transaction ID, HTTP status, outcome, timing, response size, a hash and a schema fingerprint of the response (field names and types, not the content), data freshness, facilitator and settlement time. Receipts contain no amount, price or wallet field, and we refuse receipts that do. Response bodies are never uploaded. We check each receipt against the public ledger before it counts: that the wallet that signed it paid the seller. We do not store the amount. We keep the paying wallet's address (read from the ledger) with the submission only to run the anti-abuse checks below; it is never published or shown by any public page or API.",
    "<strong>Rewards.</strong> Contributors get a public, pseudonymous contributor badge, optionally with a count of verified contributions (at most one per seller per day). That is the only reward: there are no credits, money, perks, rankings or rate-limit changes, and sharing never changes how any score is computed. The 'Tested by Lumi' badge can only be earned. It can never be bought, and it is removed automatically when the seller's score drops below the threshold. Paying Lumi never changes a score, tier, ranking or 'Tested by Lumi' result. The paid 'Monitored by Lumi' badge is separate and labelled as paid.",
    "We use this data to score sellers, to prevent self-testing and abuse (for example, limits per key, per endpoint and per funding source), and to show your badge. Findings can appear in Lumi's seller observations and badges in combined form; your key id and wallets are not shown with them. Demand statistics are off by default; if you opt in, your purchases are counted only in aggregate, at domain level, with at least two contributors per row and no key ids or wallets.",
    '<strong>How long we keep it.</strong> We keep raw data for 90 days and then delete it. This covers tier 1 outcome counters and contributor submissions, including the stored receipt copy. A raw tier 1 day is deleted only after it has been summarised. The summaries are kept long-term: one row per seller per day, holding the number of delivered and failed purchases and coarse status classes. They contain no wallet address, amount, transaction ID, URL query, payload or anything that identifies you. Your contributor account (key ID, public key and registered wallets) is kept while it is active, meaning you submitted a verified receipt in the last 12 months, and is not deleted at 90 days. You can see your own submissions and your badge at any time through the contributor API. You do not get, and we do not share, the raw pooled database. To ask about your contributor data, email <a href="mailto:hello@lumitrades.io">hello@lumitrades.io</a>.',
    '<strong>Deleting your contributor account.</strong> You can delete it yourself at any time with <code>lumi-scan account delete</code> (it asks you to type your key ID first), or email <a href="mailto:hello@lumitrades.io">hello@lumitrades.io</a> and we delete it the same way. Deletion is immediate and cannot be undone. <em>Deleted:</em> your key (it can never be used again), label, public key, registered wallets and the funding wallet recorded for each, any domains you told us you own, your demand opt-in, your last-activity date, your badge, and every receipt you shared, including the stored copy, unless we have already cited it in a published, dated test result. <em>Kept, with no link to you:</em> receipts already cited in a published, dated test result, with your wallet signature, paying-wallet address, kit details and key ID removed (the transaction ID, seller and delivery result stay because the published result cites them, and they are still deleted after 90 days like other raw data); the anonymous per-seller daily summaries and tier 1 counters, which never had a link to you; and a record that the deleted key ID existed, so it cannot be reused. Transactions on a public blockchain cannot be deleted by anyone, including us.',
]
# Seller payment analysis (legal review 2026-10-25, M9, section 7.5 text verbatim). English on every page like the Lumi Check section.
SELLER_PAY_ID, SELLER_PAY_HEAD = "seller-payments", "Seller payment analysis"
SELLER_PAY = [
    "To describe x402 sellers and to spot self-payment, Lumi reads public blockchain payments to sellers' listed pay-to addresses. We group payer wallets by funding source and publish only ranges and flags for sellers, never payer wallets or dollar amounts. Raw wallet-level data is kept up to 90 days and then deleted; aggregates are kept. We don't try to identify payers. If you think a payer wallet is yours and want us to stop processing it, email <a href=\"mailto:hello@lumitrades.io\">hello@lumitrades.io</a> and we will exclude it (you can object at any time). Legal basis (EU/UK): legitimate interests in reporting on and preventing manipulation of a public payment market.",
]
# Payments you make to Lumi (privacy review 2026-11-19, section 2, published with the fleet-guard launch on 2026-11-19 with the
# owner's yes). English on every page like the Lumi Check section. Trusted, hand-written HTML; a "<ul" item is not wrapped in <p>.
PAYMENTS_ID, PAYMENTS_HEAD = "payments-to-lumi", "Payments you make to Lumi"
PAYMENTS = [
    "This section is about you as a customer of Lumi: someone who pays Lumi for an API call, a data-feed plan or credits, seller monitoring, or a pack, or who opens a feed key by proving a wallet. It is not about the third-party payers we observe on public ledgers when we describe other sellers (that is “Seller payment analysis” and, when launched, the wallet pattern check).",
    "When you pay us, or when you prove a wallet to create a feed key, we store:",
    "<ul><li>your wallet address, in raw form;</li><li>the payment’s transaction hash (transaction ID), amount, asset, network, and time;</li><li>the route or product you bought;</li><li>for a feed key: a SHA-256 hash of the secret key (we show the secret once and do not store it), the key’s plan and credits, and the wallet bound to that key.</li></ul>",
    "We collect this to perform the contract (to confirm the payment, bind and look up your key, account for credits, and, where a refund is owed, pay it back to the same wallet) — legal basis (EU/UK): contract, GDPR Article 6(1)(b); to keep accounting records of amounts received — legal basis: legal obligation, Article 6(1)(c); and to prevent abuse (for example, tagging Lumi’s own test wallets, enforcing one free feed key per wallet, and enforcing free-trial limits) — legal basis: legitimate interests, Article 6(1)(f).",
    "<strong>How long we keep it today.</strong> In the live system as of 19 November 2026, these customer records are <strong>not</strong> automatically deleted. The tables that hold them (<code>sales</code>, <code>feed_keys</code>, <code>feed_payments</code>, and similar records for monitoring plans, refused pack payments, and free-trial sign-ins) have no 90-day purge in the running production code. A feed key can keep its bound wallet for as long as the key exists (a free key has no expiry). We are rolling out a recurring cleanup so that raw customer wallet addresses are kept only as long as they are needed for payment, refunds, or key matching, with a target of 90 days after the key expires or after the last payment, whichever is later, unless a longer accounting period applies. For accounting we aim to keep the transaction hash, amount, asset, date, and route, and to drop the raw address link where we can. A transaction hash remains public on the blockchain and can still be used to look up the paying address. Until that cleanup is in production, assume we still hold the raw address. We will date this page when the cleanup is actually running, rather than describe a deletion that is not yet live.",
    "Separately, once the wallet pattern check is deployed, a nightly job in that product will delete <em>that product’s</em> sales-ledger rows after 90 days, and will delete prepaid-key rows (including the payment transaction hash stored with the key) 30 days after the key expires. That job does not change retention for feed keys, feed payments, monitoring plans, or other sales routes.",
    "<strong>Who sees it.</strong> Lumi’s operator can see these records on private owner-only API routes used to run the service (for example, to review sales or refunds). A private sale-alert email to the operator names the route, amount, and transaction hash; it does not include the wallet in the email text. If a sale-alert webhook is configured, that webhook currently receives the full sales row, including the wallet. Cloudflare, which hosts the API and its database, may process the same records to run the service. Workers Logs may include the payer address and transaction hash on a settled-payment log line. The payment facilitator sees the payment at the time it settles. We do not publish your wallet on the public website or in the public data feed.",
    "If you want a copy of what we hold about your payments, or want us to delete or correct it, email <a href=\"mailto:hello@lumitrades.io\">hello@lumitrades.io</a> and include the wallet you paid from. We aim to acknowledge the request within 5 business days and to resolve it within 30 days (sooner if the law requires). We may keep a limited accounting record (transaction hash, amount, date, route) where the law requires it. We cannot delete the payment from the public blockchain."
]
# Wallet pattern check (fleet guard), same review, verbatim except the plan price is left out (not offered, so not in public docs).
FLEET_ID, FLEET_HEAD = "wallet-pattern-check", "Wallet pattern check (fleet guard)"
FLEET = [
    "Lumi offers a wallet pattern check (also called fleet guard) at <code>api.lumitrades.io</code>. A caller submits a wallet address, a seller domain, or a seller URL, and we return a dated label saying whether that identifier, in our method, matches a known automated payment-pattern cluster on public ledgers. We also use the same public-ledger clustering, in aggregate, to keep seller activity views honest (ranges and flags, not a list of payers).",
    "This is a statistical pattern observation. It is not a finding of intent or wrongdoing, and it is not a fraud, identity, or sanctions determination. We do not try to attach a person’s civil name or off-chain identity to a wallet.",
    "We use only public-ledger payment data and identifiers the caller submits. We do not buy marketing lists for this product. Legal basis (EU/UK): legitimate interests (GDPR Article 6(1)(f)) in reporting dated payment-pattern observations from public ledgers and in limiting misleading use of public payment counts. You can object at any time (Article 21) by emailing <a href=\"mailto:hello@lumitrades.io\">hello@lumitrades.io</a>.",
    "The label is one of three values only. There is no confidence score. A match is exactly: “Pattern match: automated cluster, as of [date], method [URL]”. The date in that sentence is the UTC day we last loaded or reconfirmed the membership, and the URL is <a href=\"https://api.lumitrades.io/v1/fleet/methodology\">https://api.lumitrades.io/v1/fleet/methodology</a> (also returned as <code>method_url</code>). The other two labels are exactly “No match” and “Insufficient data.” A match may also include a role (payer or seller). We do not return a cluster id, member counts, a first-seen date, or a list of other addresses in the cluster. Absence of a match is not a clearance. The response also has an <code>as_of</code> time for the check and a <code>valid_until</code> time (one hour later); do not treat the result as current after that. A “No match” or “Insufficient data” answer may be cached for up to an hour. A match is re-read on every call, so a correction takes effect on the next check.",
    "This product is not OFAC, sanctions, AML, or KYC screening, and it is not a substitute for those. It is not a “consumer report,” and Lumi is not a consumer reporting agency (15 U.S.C. §1681 et seq.). Callers must not use the label as a factor in deciding a person’s eligibility for credit, insurance, employment, housing, a government benefit, or any other purpose listed in 15 U.S.C. §1681b, and must not tell others they may do so.",
    "<strong>What we store.</strong> We do not store the submitted (subject) address in raw form in the fleet-guard database. We store an HMAC-SHA256 keyed hash of the normalised identifier, under a secret key only Lumi holds. During a key rotation we may also keep the previous secret, so we can still find an older hash for a lookup, a dispute, or a deletion; new hashes are written only with the current secret. A keyed hash can be joined back to the address by anyone who has the address and the key, or by us if you give us the address so we can recompute the hash. Under GDPR Recital 26, this is <strong>pseudonymous personal data, not anonymous data</strong>. We do not claim that hashed addresses are anonymous.",
    "We also store the transaction hash of a payment made to Lumi for a paid check or a prepaid pack, together with a keyed hash of the paying wallet, the amount, the network, and the route. Transaction hashes are public on the relevant blockchain and can be used to look up the paying address. That record is also <strong>pseudonymous, not anonymous</strong>. On Lumi’s other paid routes, customer wallets are still stored in raw form, as described under “Payments you make to Lumi,” until the cleanup there is in production.",
    "Prepaid pack and plan keys are shown once to the buyer. Lumi stores only a SHA-256 of the key, not the key itself. A 30-day plan exists in the code but is not offered unless we turn that plan on; it is not listed in the public docs while it is off.",
    "<strong>What we do not store raw in this product.</strong> Other members of a cluster are stored only as keyed hashes, never as a published list, and we do not return a cluster id in the check response. The paying wallet on a fleet-guard payment is stored as a keyed hash, not in raw form, in Lumi’s fleet-guard and sales records. Lumi’s private API traffic log stores the request path without the query string, a daily-rotating keyed hash of the IP address, and no raw IP; those traffic records are deleted after 90 days. Rate-limit counters use keyed hashes of the IP (and, on the free path, of an optional wallet header) and last only for the cap window (a minute or a day). In-memory cache entries are keyed by the subject hash, hold only non-match answers, and expire after one hour.",
    "<strong>Retention.</strong> A nightly job (the existing 03:00 UTC cron tick) applies these periods, including while the product is switched off, once the fleet-guard tables exist:",
    "<ul><li>Raw subject addresses: not stored in the fleet-guard database. (You still send the address in the request URL; see “Logs and request URLs” below.)</li><li>Keyed hashes of cluster membership: 90 days from the last load or reconfirmation, then deleted. A successful dispute removes or overrides that hash sooner. Empty clusters are removed when they have no remaining members. A hashed record of a correction or exclusion (an override) is kept so the correction continues to apply.</li><li>Settled payment records for this product in <code>fleet_guard_settles</code> (raw transaction hash, route, hashed payer, time): 90 days, then deleted.</li><li>Sales-ledger rows for this product only: 90 days, then deleted.</li><li>Prepaid keys, including the <code>paid_tx</code> transaction hash on the key row: until 30 days after the key expires, then the whole key row is deleted. A pack is valid for 365 days, so that transaction hash can remain with the key for up to 395 days. A monthly plan, if offered, is valid for 30 days and does not auto-renew.</li><li>Idempotent payment retries: 24 hours, without the payer address.</li><li>Traffic logs: 90 days, as in “The agent API” above.</li><li>Application logs on this path may include a transaction hash and a short prefix of a payer hash for security (replay and underpayment alerts). Address-shaped strings in those events are redacted, except transaction hashes. Log shipping, if any, should follow the same 90-day maximum unless a longer legal hold is required.</li></ul>",
    "<strong>Logs and request URLs.</strong> The check is called with the subject in the query string of the caller’s request. Lumi’s traffic log stores the path without that query string. Payment invoice and resource URLs for this product always carry a keyed hash of the query (<code>n</code> and <code>qh=</code>), never the raw address. We do not put raw subject or payer addresses in fleet-guard application logs. Other infrastructure (for example a hosted log stream) might still see a request URL a caller sent. We do not use those URLs to build a public list of addresses.",
    "<strong>Paid checks and “sale” of personal information.</strong> We do not sell, rent, or trade lists of wallets, cluster memberships, or other personal data. We do not give a caller the other members of a cluster. A paid check (and the capped free check) returns only a dated label for the identifier the caller submits. Whether that paid, per-call disclosure is a “sale” or “share” of personal information under the California CPRA is a legal question; if you want us not to return a label on an address that is yours, email <a href=\"mailto:hello@lumitrades.io\">hello@lumitrades.io</a> and ask us to exclude it. We will hash the address you give us, suppress future labels for that hash, and confirm when it is done. We will not discriminate against you for making that request.",
    "<strong>Disputes, correction, and your rights.</strong> If you believe a label about an address is wrong, or you want us to stop processing an address, email <a href=\"mailto:hello@lumitrades.io\">hello@lumitrades.io</a> (legal notices may also go to <a href=\"mailto:legal@lumitrades.io\">legal@lumitrades.io</a>, as described in our Terms). Tell us the address, the network if you know it, and what you want (correction, deletion, exclusion, or a copy of what we hold). If the request is about a keyed hash, we can only find it if you give us the address so we can recompute the hash.",
    "We aim to acknowledge the request within 5 business days and to resolve it within 30 days (sooner if the law requires). If a dispute succeeds, we will correct or remove the label in our own check results. That change is applied in our systems when we record it, and the next check will show it (matches are not served from cache). We do not currently publish a public corrections list for this product, and there is no automatic notice to licensees. If we later add a public corrections feed, we will describe it here. Until then, anyone displaying a label should not treat a result as current after its <code>valid_until</code> time, and should obtain a fresh check if they need an updated label.",
    "You may also ask us for access, correction, or deletion, or object to processing (GDPR Articles 15–17 and 21, and equivalent rights where they apply, including California rights to know, delete, and correct). On a valid request, and after we recompute the hash from the address you provide (including, during a rotation, the previous secret if we still hold it), we will say whether a membership record exists, show you the current label, and delete or suppress the hashed record as requested, except where we must keep a limited record of the request itself, a payment legally required to be kept, or a transaction that remains on a public blockchain (which we cannot delete). Payments you made to Lumi stay visible on the ledger even after we delete our copy of the payment record.",
    "The method is described at <a href=\"https://api.lumitrades.io/v1/fleet/methodology\">https://api.lumitrades.io/v1/fleet/methodology</a>. Questions: <a href=\"mailto:hello@lumitrades.io\">hello@lumitrades.io</a>."
]
TITLE = "Privacy Policy | Lumi Trades"
DESC = ("What Lumi Trades collects and why: newsletter email via Kit, cookieless Cloudflare Web Analytics, GitHub Pages hosting and the "
        "agent API logs. We do not sell data.")


def build_page(h, tp, nav_items, V, gen_date, page):
    E, _t = h.E, h._
    title = _t(TITLE)
    desc = _t(DESC)
    url = h.SITE + h.L.prefix + "privacy/"
    ld = [seo.organization(_t),
          {"@context": "https://schema.org", "@type": "WebPage", "name": _t("Privacy Policy"), "url": url, "description": desc,
           "inLanguage": h.L.code, "isPartOf": {"@id": seo.SITE_ID}, "publisher": {"@id": seo.ORG_ID},
           "dateModified": UPDATED.isoformat()},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Lumi Trades", "item": h.SITE + h.L.prefix},
              {"@type": "ListItem", "position": 2, "name": _t("Privacy Policy"), "item": url}]}]
    upd = h.L.date(dt.datetime(UPDATED.year, UPDATED.month, UPDATED.day), with_time=False)
    secs = "".join(
        f'<section class="card cp-sec" id="{sid}"><h2>{E(_t(head))}</h2>\n'
        + "".join(f"<p>{_t(p, mail=CONTACT) if '{mail}' in p else E(_t(p))}</p>" for p in paras) + "</section>\n"
        for sid, head, paras in SECTIONS)
    note = "" if h.L.en else f'<p class="meta" lang="{h.L.code}">{E(_t(LUMI_CHECK_NOTE))}</p>\n'
    lang_attr = "" if h.L.en else ' lang="en"'
    lumi = (f'<section class="card cp-sec" id="{LUMI_CHECK_ID}"{lang_attr}><h2>{E(LUMI_CHECK_HEAD)}</h2>\n'
            + note + "".join(f"<p>{p}</p>" for p in LUMI_CHECK) + "</section>\n")
    sellers = (f'<section class="card cp-sec" id="{SELLER_PAY_ID}"{lang_attr}><h2>{E(SELLER_PAY_HEAD)}</h2>\n'
               + note + "".join(f"<p>{p}</p>" for p in SELLER_PAY) + "</section>\n")
    wrap = lambda p: p if p.startswith("<ul") else f"<p>{p}</p>"
    payments = (f'<section class="card cp-sec" id="{PAYMENTS_ID}"{lang_attr}><h2>{E(PAYMENTS_HEAD)}</h2>\n'
                + note + "".join(wrap(p) for p in PAYMENTS) + "</section>\n")
    fleet = (f'<section class="card cp-sec" id="{FLEET_ID}"{lang_attr}><h2>{E(FLEET_HEAD)}</h2>\n'
             + note + "".join(wrap(p) for p in FLEET) + "</section>\n")
    cut = secs.index('<section class="card cp-sec" id="sharing">')
    secs = secs[:cut] + lumi + sellers + payments + fleet + secs[cut:]
    body = f"""<main class="wrap cp-main">
<p class="cp-crumb"><a href="../">Lumi Trades</a> › {E(_t("Privacy Policy"))}</p>
<h1>{E(_t("Privacy Policy"))}</h1>
<p class="meta">{E(_t("Last updated: {date}", date=upd))}</p>
<p class="cp-lede">{E(_t(LEDE))}</p>
{secs}</main>
"""
    return page(h, tp, "privacy/", title, desc, ld, body, V, gen_date, nav_items, "privacy", keywords=None)
