# Service Knowledge Framework

Guide for AI classification of password entries by service type. This is a framework for reasoning, not an exhaustive database.

## Classification Approach

For each unmatched entry, consider:
1. **URL/domain** — What is this service? What category does it fall into?
2. **Title** — Service name when URL is missing or unclear
3. **Username** — Even if it didn't match a known email, does it suggest personal vs. business?
4. **Context** — What other entries exist for this service? Multiple accounts suggest personal + business split.

## Service Categories

### Almost Always Personal
- **Entertainment**: Netflix, Hulu, Disney+, HBO Max, Paramount+, Peacock, Apple TV+, Spotify, Apple Music, YouTube Premium, Twitch, Crunchyroll
- **Gaming**: Steam, PlayStation, Xbox, Nintendo, Epic Games, GOG, Battle.net, EA, Ubisoft
- **Social Media**: Facebook, Instagram, TikTok, Snapchat, Reddit, Pinterest, Tumblr, Discord (personal servers)
- **Personal Finance**: Venmo, Cash App, Zelle, Robinhood, Mint, YNAB, Credit Karma, personal bank accounts
- **Personal Shopping**: Amazon (flag as shared if business purchasing possible), eBay, Etsy, Target, Walmart, Best Buy, Costco
- **Health & Fitness**: MyFitnessPal, Strava, Peloton, health insurance portals, pharmacy accounts
- **Travel (personal)**: Airline loyalty programs, hotel rewards, Airbnb (personal), Uber/Lyft (personal)
- **Dating**: Tinder, Bumble, Hinge, etc.

### Almost Always Business
- **Cloud/Infrastructure**: AWS, GCP, Azure, DigitalOcean, Heroku, Vercel, Netlify, Railway, Fly.io, Cloudflare
- **Developer Tools**: GitHub, GitLab, Bitbucket, Docker Hub, npm, PyPI, Homebrew
- **Business SaaS**: Slack, Notion, Linear, Jira, Confluence, Asana, Monday.com, Basecamp, ClickUp
- **Design**: Figma, Sketch, Adobe Creative Cloud, Canva (business), InVision, Framer
- **Business Finance**: QuickBooks, Xero, FreshBooks, Stripe, Square, Brex, Mercury, Wave
- **Marketing**: Google Ads, Meta Ads, Mailchimp, ConvertKit, HubSpot, Sendgrid, Twilio
- **Analytics**: Google Analytics, Mixpanel, Amplitude, Hotjar, Datadog, Sentry
- **AI/ML Tools**: OpenAI, Anthropic, Replicate, Hugging Face (if business use)
- **Domain/Hosting**: GoDaddy, Namecheap, Google Domains, Squarespace, WordPress (business sites)
- **HR/Legal**: Gusto, Rippling, Zenefits, DocuSign, registered agent services, state filing portals

### Shared / Ambiguous (Flag These)
- **Google** — Personal Gmail vs. Google Workspace (check the email used)
- **Microsoft** — Personal Outlook vs. Microsoft 365 (check the email used)
- **Apple** — Personal Apple ID vs. Apple Developer account (check URL: developer.apple.com = business)
- **Amazon** — Personal shopping vs. AWS vs. business purchasing (check URL: aws.amazon.com = business)
- **LinkedIn** — Personal networking vs. LinkedIn Premium for business
- **Dropbox** — Personal vs. Dropbox Business
- **Zoom** — Personal vs. business account
- **PayPal** — Personal vs. PayPal Business
- **GitHub** — Could be personal projects vs. work (check the email)

### Client Indicators
- URL contains a client's domain
- Username is a client-provided email
- Title includes a client's company name
- Service is a client's internal tool (e.g., their Jira, their Slack workspace)

## Disambiguation Tips

- **Check the email first** — Even for shared services, the email used often reveals intent
- **developer.* or admin.* subdomains** — Usually business
- **Multiple accounts for same service** — One is likely personal, one business
- **If truly uncertain** — Flag it. Better to ask than guess wrong.
- **Title contains "work" or "business"** — Business vault
- **Title contains "personal" or "home"** — Personal vault
