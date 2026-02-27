# Tax Prep Agent - YouTube Demo Script

**Filer**: Alex Rivera | Rivera Digital Consulting LLC
**Video Target Length**: ~25-30 minutes
**Tone**: Conversational, enthusiastic but professional. You are showing a developer audience how an AI agent handles real-world tax complexity.

---

## Table of Contents

1. [Pre-Video Setup](#pre-video-setup)
2. [Phase 1: Initialize](#phase-1-initialize-2-minutes)
3. [Phase 2: Drop Documents](#phase-2-drop-documents-2-minutes)
4. [Phase 3: Intake Interview](#phase-3-intake-interview-8-10-minutes)
5. [Phase 4: Extract](#phase-4-extract-3-minutes)
6. [Phase 5: Review](#phase-5-review-8-10-minutes)
7. [Phase 6: Package](#phase-6-package-2-minutes)
8. [Wrap-Up](#wrap-up-2-minutes)

---

## Pre-Video Setup

Before hitting record, make sure the following are ready:

### Terminal
- Clean terminal window, dark theme, large font (16pt+)
- Working directory set to the project root
- Claude Code CLI installed and authenticated
- No sensitive personal data visible anywhere on screen

### Documents to Have Ready (in a staging folder)
Prepare these files in a folder like `~/Desktop/alex-tax-docs/`:

- `chase-business-checking-2025.csv` -- Full year bank statement export from Chase
- `wellsfargo-personal-checking-2025.csv` -- Full year statement from Wells Fargo
- `marcus-savings-2025.csv` -- Marcus savings account statement
- `1099-NEC-techstart.pdf` -- 1099-NEC from TechStart Inc. ($114,000)
- `1099-NEC-greenleaf.pdf` -- 1099-NEC from GreenLeaf Co. ($28,000)
- `1099-INT-marcus.pdf` -- 1099-INT from Marcus (interest income)
- `health-insurance-1095A.pdf` -- BCBS Form 1095-A
- `roth-ira-5498-vanguard.pdf` -- Form 5498 from Vanguard
- `denver-lease-agreement.pdf` -- Lease showing 1,100 sq ft, $2,800/mo
- `portland-lease-agreement.pdf` -- Lease showing 1,350 sq ft, $3,100/mo
- `estimated-tax-confirmations/` -- Folder with IRS and state payment confirmations

### Screen Layout
- Terminal taking up ~70% of screen
- File explorer or Finder visible on the side (to show drag-and-drop of documents)
- Browser tab with the project README open (optional, for reference)

### Recording Software
- OBS or ScreenFlow configured
- Microphone levels tested
- Resolution: 1920x1080 minimum

---

## Phase 1: Initialize (~2 minutes)

### Opening

[NARRATOR/VOICEOVER]
"Today I'm going to show you something I've been building -- a tax prep agent that runs entirely inside Claude Code. It handles the full workflow that a freelancer goes through every year: gathering documents, answering interview questions, reviewing transactions, and packaging everything up for your CPA. Let's walk through a complete tax prep session for a fictional freelancer named Alex Rivera."

[NARRATOR/VOICEOVER]
"Alex runs Rivera Digital Consulting, a single-member LLC doing freelance web development and digital marketing out of Denver and Portland. Made about 142K this year. Let's get started."

### Run the Initialize Command

[YOU SAY]
"First, we initialize a new tax year. This sets up the entire folder structure."

[YOU TYPE]
```
/cpa-tax-prep:initialize 2025
```

[AGENT SAYS]
The agent will create the folder structure and output something like:

```
Tax Prep initialized for tax year 2025.

Created folder structure:
  tax-prep/2025/
    documents/
      income/
      expenses/
      bank-statements/
      retirement/
      insurance/
      property/
      other/
    workpapers/
    output/

Ready for Phase 2: Drop your documents into the appropriate folders.
```

[NARRATOR/VOICEOVER]
"So it's created a clean folder structure organized by document type. Income documents like 1099s go in one folder, bank statements in another, insurance docs in another. This is how a real CPA's office organizes things -- the agent follows the same conventions."

[YOU SAY]
"Let me quickly show you the folder structure it created."

[YOU TYPE]
```
ls -la tax-prep/2025/documents/
```

[NARRATOR/VOICEOVER]
"Each of these folders maps to a category the agent understands. When we drop documents in, it knows what to look for based on where you put them. Let's do that now."

---

## Phase 2: Drop Documents (~2 minutes)

[NARRATOR/VOICEOVER]
"Phase 2 is simple -- we just drop our tax documents into the right folders. In a real scenario, you'd download these from your bank, your clients' payroll providers, and your brokerage."

[YOU SAY]
"I've got Alex's documents ready in a staging folder. Let me move them into the right places."

[YOU TYPE]
```
cp ~/Desktop/alex-tax-docs/1099-NEC-techstart.pdf tax-prep/2025/documents/income/
cp ~/Desktop/alex-tax-docs/1099-NEC-greenleaf.pdf tax-prep/2025/documents/income/
cp ~/Desktop/alex-tax-docs/1099-INT-marcus.pdf tax-prep/2025/documents/income/
cp ~/Desktop/alex-tax-docs/chase-business-checking-2025.csv tax-prep/2025/documents/bank-statements/
cp ~/Desktop/alex-tax-docs/wellsfargo-personal-checking-2025.csv tax-prep/2025/documents/bank-statements/
cp ~/Desktop/alex-tax-docs/marcus-savings-2025.csv tax-prep/2025/documents/bank-statements/
cp ~/Desktop/alex-tax-docs/health-insurance-1095A.pdf tax-prep/2025/documents/insurance/
cp ~/Desktop/alex-tax-docs/roth-ira-5498-vanguard.pdf tax-prep/2025/documents/retirement/
cp ~/Desktop/alex-tax-docs/denver-lease-agreement.pdf tax-prep/2025/documents/property/
cp ~/Desktop/alex-tax-docs/portland-lease-agreement.pdf tax-prep/2025/documents/property/
cp -r ~/Desktop/alex-tax-docs/estimated-tax-confirmations/ tax-prep/2025/documents/other/
```

[NARRATOR/VOICEOVER]
"We've got 1099s from both clients and the savings account, all three bank statements, the health insurance form, the Roth IRA contribution form, both lease agreements -- Alex moved mid-year which adds complexity -- and the estimated tax payment confirmations. That's everything. Now we move to the intake interview."

[YOU SAY]
"Documents are in. Let's start the intake."

---

## Phase 3: Intake Interview (~8-10 minutes)

[YOU TYPE]
```
/cpa-tax-prep:intake 2025
```

[NARRATOR/VOICEOVER]
"The intake interview is where the agent collects all the contextual information it can't get from documents alone -- your filing status, your business structure, things like that. It goes through nine sections. Let me walk through each one."

---

### Section 1: Personal Information

[AGENT SAYS]
"Let's start with your basic information. What is your full legal name?"

[YOU SAY]
"Alex Rivera."

[AGENT SAYS]
"And your date of birth?"

[YOU SAY]
"March 12, 1991."

[AGENT SAYS]
"What's your current mailing address?"

[YOU SAY]
"742 NW Everett Street, Apartment 4B, Portland, Oregon 97209."

[AGENT SAYS]
"Phone number?"

[YOU SAY]
"303-555-0147."

[AGENT SAYS]
"Email address?"

[YOU SAY]
"alex@riveradigital.co."

[AGENT SAYS]
"What is your filing status? Single, Married Filing Jointly, Married Filing Separately, Head of Household, or Qualifying Surviving Spouse?"

[YOU SAY]
"Single."

[AGENT SAYS]
"Do you have any dependents?"

[YOU SAY]
"No dependents."

[NARRATOR/VOICEOVER]
"Pretty straightforward so far. The agent is building out the filer profile that'll be used throughout the rest of the process."

---

### Section 2: State Residency

[AGENT SAYS]
"Now let's talk about state residency. Did you live in the same state for all of 2025?"

[YOU SAY]
"No, I moved mid-year. I was in Denver, Colorado from January through August, then I moved to Portland, Oregon in September. So I lived in Oregon from September through December."

[AGENT SAYS]
"Got it -- part-year resident of both Colorado and Oregon. To confirm: Colorado from January 1 through August 31, and Oregon from September 1 through December 31, 2025. Is that correct?"

[YOU SAY]
"Yes, that's right."

[AGENT SAYS]
"Did you earn income in any other states besides Colorado and Oregon?"

[YOU SAY]
"No, just those two. All my work is remote."

[NARRATOR/VOICEOVER]
"This is a detail that a lot of DIY tax filers miss. When you move states mid-year, you're a part-year resident of both states, and you typically need to file returns in both. The agent picks up on this immediately and will factor it into the final package."

---

### Section 3: Business Information

[AGENT SAYS]
"Let's get your business details. What is your business name and entity type?"

[YOU SAY]
"Rivera Digital Consulting LLC. It's a single-member LLC."

[AGENT SAYS]
"What does your business do?"

[YOU SAY]
"Freelance web development and digital marketing consulting."

[AGENT SAYS]
"What is your EIN or do you use your SSN for the business?"

[YOU SAY]
"I have an EIN -- it's 84-1234567."

[AGENT SAYS]
"When did you start this business?"

[YOU SAY]
"January 2021."

[AGENT SAYS]
"What accounting method do you use -- cash or accrual?"

[YOU SAY]
"Cash basis."

[AGENT SAYS]
"Do you have any employees or contractors working for you?"

[YOU SAY]
"No, just me. Solo operation."

[NARRATOR/VOICEOVER]
"Single-member LLC on cash basis -- that means the business income flows through to Alex's personal return on Schedule C. The agent knows this and will structure everything accordingly."

---

### Section 4: Income Sources

[AGENT SAYS]
"Let's go through your income sources for 2025. Tell me about your clients and how you were paid."

[YOU SAY]
"I have two main clients. My primary client is TechStart Inc. -- they pay me a $9,500 per month retainer, processed through Gusto. That ran all 12 months, so $114,000 total. My second client is GreenLeaf Co. -- project-based work, they paid me about $28,000 total across 3 or 4 invoices throughout the year. Then I had a few smaller one-off projects that added up to about $5,000."

[AGENT SAYS]
"So approximately $147,000 in total business income. Did you receive 1099-NEC forms from TechStart and GreenLeaf?"

[YOU SAY]
"Yes, I got 1099s from both of them. The smaller projects were under the 1099 threshold."

[AGENT SAYS]
"Any other income sources? W-2 employment, investment income, rental income, cryptocurrency, anything else?"

[YOU SAY]
"I earned some interest on my Marcus savings account -- I think it was around $1,200 for the year. That's it."

[NARRATOR/VOICEOVER]
"The agent is cross-referencing what Alex says with the documents we dropped in. It'll flag any discrepancies later during the review phase."

---

### Section 5: Bank Accounts

[AGENT SAYS]
"Let's identify your bank accounts. Tell me about each account you used in 2025."

[YOU SAY]
"I have three accounts. First is my business checking at Chase -- that's where all my business income comes in and most business expenses go out. Second is a personal checking account at Wells Fargo -- that's mostly personal, but I do pay rent, internet, and utilities from it. Third is a high-yield savings account at Marcus by Goldman Sachs -- that's just savings, nothing business-related."

[AGENT SAYS]
"So to confirm: Chase business checking is primary business, Wells Fargo personal checking has some mixed-use expenses like rent and internet that may have a business component through home office deduction, and Marcus savings is purely personal. Is that right?"

[YOU SAY]
"Exactly."

[NARRATOR/VOICEOVER]
"The agent is flagging the Wells Fargo account as 'mixed use' because of the home office situation. It knows that rent paid from a personal account can still have a business deduction component. Smart."

---

### Section 6: Business Expenses

[AGENT SAYS]
"Let's talk about your business expenses. I'll pull the details from your bank statements, but give me a high-level overview of your major expense categories."

[YOU SAY]
"Sure. I have a bunch of software subscriptions -- Claude, GitHub, Vercel, Figma, AWS, Google Workspace, Notion, Linear -- those run between $10 and $50 a month each. I bought a new MacBook Pro in March for $2,499. A 4K monitor for $649 and a standing desk for $445 -- both for my home office. I went to ReactConf, the ticket was $799. I flew to Miami in June to meet with the GreenLeaf team -- the flight was $487.50, hotel was $312 a night for two nights, plus Uber rides and business meals during the trip. I also pay for professional services -- my accountant and a registered agent for the LLC."

[AGENT SAYS]
"Got it. For the MacBook Pro at $2,499, will you be deducting it in full this year under Section 179, or depreciating it over time?"

[YOU SAY]
"Full deduction this year under Section 179."

[AGENT SAYS]
"And for the monitor and standing desk -- same approach?"

[YOU SAY]
"Yes, Section 179 for both."

[AGENT SAYS]
"Do you use any of this equipment for personal purposes, or is it 100% business use?"

[YOU SAY]
"100% business. I have a separate personal laptop."

[NARRATOR/VOICEOVER]
"Notice the agent is already asking the right follow-up questions -- Section 179 election, business use percentage. These are the exact questions a CPA would ask. The agent will reconcile all of this against the actual bank statement charges during extraction."

---

### Section 7: Home Office

[AGENT SAYS]
"You mentioned working from home. Let's calculate your home office deduction. Since you moved mid-year, we'll need to do this for both locations. Let's start with Denver. What was the total square footage of your Denver apartment?"

[YOU SAY]
"1,100 square feet total."

[AGENT SAYS]
"And how large was the dedicated office space?"

[YOU SAY]
"120 square feet. It was a dedicated room I used exclusively for work."

[AGENT SAYS]
"What was your monthly rent?"

[YOU SAY]
"$2,800 per month."

[AGENT SAYS]
"And you were there January through August, so 8 months. That gives us 120 divided by 1,100, which is 10.91% business use. Applied to $2,800, that's $305.45 per month, times 8 months, for a total of $2,443.64 in home office deduction for the Denver location. Does that sound right?"

[YOU SAY]
"Yes, that's correct."

[AGENT SAYS]
"Now let's do Portland. Total square footage?"

[YOU SAY]
"1,350 square feet."

[AGENT SAYS]
"Dedicated office space?"

[YOU SAY]
"140 square feet. Also a dedicated room."

[AGENT SAYS]
"Monthly rent?"

[YOU SAY]
"$3,100 per month."

[AGENT SAYS]
"September through December is 4 months. So 140 divided by 1,350 is 10.37% business use. Applied to $3,100, that's $321.48 per month, times 4 months, for a total of $1,285.93. Combined with Denver, your total home office rent deduction is $3,729.57. We'll also apply the same percentages to your internet and utilities."

[YOU SAY]
"That looks right. Internet is $89 a month all year, and utilities average about $120 a month."

[NARRATOR/VOICEOVER]
"This is one of the most common areas where freelancers leave money on the table. The agent handles the mid-year move seamlessly, calculating two separate home office percentages and applying them to the right months. It even extends the deduction to internet and utilities without being asked -- because it knows those qualify too."

---

### Section 8: Health Insurance & Retirement

[AGENT SAYS]
"Do you have health insurance? As a self-employed individual, your premiums may be deductible."

[YOU SAY]
"Yes. Blue Cross Blue Shield -- I had coverage in Colorado for the first eight months, then transferred to an Oregon plan for the last four months. Same carrier though. My premium is $485 per month, all 12 months."

[AGENT SAYS]
"So $5,820 total for the year. Did you receive any premium tax credits or subsidies through the marketplace?"

[YOU SAY]
"No, I pay full price. I buy directly from BCBS, not through the marketplace."

[AGENT SAYS]
"Got it -- we'll take the full self-employed health insurance deduction. Now, did you make any retirement contributions in 2025?"

[YOU SAY]
"Yes, I contributed $7,000 to my Roth IRA at Vanguard. Made the full contribution on March 15, 2025."

[AGENT SAYS]
"That's the maximum Roth IRA contribution for 2025. Since it's a Roth, it's not deductible on your return, but we'll note it for your records and confirm it with the 5498 form. Do you have a SEP-IRA or Solo 401(k)?"

[YOU SAY]
"No, just the Roth IRA."

[NARRATOR/VOICEOVER]
"The agent correctly identifies that the Roth IRA contribution isn't deductible but still documents it. It also probes for SEP-IRA or Solo 401(k) -- which, honestly, might be something Alex should consider for next year given the income level. A good CPA might mention that."

---

### Section 9: Estimated Tax Payments

[AGENT SAYS]
"Did you make estimated tax payments during 2025?"

[YOU SAY]
"Yes, quarterly. To the IRS, I paid $4,200 each quarter -- so $16,800 total for the year. For state taxes, I paid Colorado $1,800 for Q1 and Q2, then switched to Oregon and paid $2,100 for Q3 and Q4."

[AGENT SAYS]
"Let me confirm the dates and amounts:
- Q1 (April 15): IRS $4,200 + Colorado $1,800
- Q2 (June 16): IRS $4,200 + Colorado $1,800
- Q3 (September 15): IRS $4,200 + Oregon $2,100
- Q4 (January 15, 2026): IRS $4,200 + Oregon $2,100

Total federal: $16,800. Total Colorado: $3,600. Total Oregon: $4,200. Does that match your records?"

[YOU SAY]
"Yes, that's exactly right."

[AGENT SAYS]
"Great. That wraps up the intake interview. I have everything I need. Let me summarize what we've captured."

[NARRATOR/VOICEOVER]
"The agent will now output a summary of the entire intake. This is your chance to catch any errors before it moves on to extraction."

[AGENT SAYS]
The agent will display a complete intake summary covering all nine sections. Review it on screen and confirm.

[YOU SAY]
"That all looks correct. Let's move on."

---

## Phase 4: Extract (~3 minutes)

[YOU TYPE]
```
/cpa-tax-prep:extract 2025
```

[NARRATOR/VOICEOVER]
"Now the agent does the heavy lifting. It's going to read through every document we dropped in -- the bank statements, the 1099s, the lease agreements -- and extract structured data from all of them. It runs these extractions in parallel, so it processes multiple documents at the same time."

[AGENT SAYS]
The agent will show progress output as it processes each document:

```
Extracting data from documents...

[1/11] Processing: 1099-NEC-techstart.pdf
  -> Extracted: $114,000.00 non-employee compensation from TechStart Inc.

[2/11] Processing: 1099-NEC-greenleaf.pdf
  -> Extracted: $28,000.00 non-employee compensation from GreenLeaf Co.

[3/11] Processing: 1099-INT-marcus.pdf
  -> Extracted: $1,247.83 interest income from Marcus by Goldman Sachs

[4/11] Processing: chase-business-checking-2025.csv
  -> Extracted: 847 transactions, $189,432.17 total debits, $148,291.50 total credits
  -> Categorized: 312 business expenses, 23 transfers, 512 other

[5/11] Processing: wellsfargo-personal-checking-2025.csv
  -> Extracted: 634 transactions
  -> Flagged: 12 potentially business-related (rent, internet, utilities)

[6/11] Processing: marcus-savings-2025.csv
  -> Extracted: 14 transactions (transfers and interest)

[7/11] Processing: health-insurance-1095A.pdf
  -> Extracted: 12 months coverage, $485.00/month premium

[8/11] Processing: roth-ira-5498-vanguard.pdf
  -> Extracted: $7,000.00 Roth IRA contribution, 3/15/2025

[9/11] Processing: denver-lease-agreement.pdf
  -> Extracted: 1,100 sq ft, $2,800/month, lease dates confirmed

[10/11] Processing: portland-lease-agreement.pdf
  -> Extracted: 1,350 sq ft, $3,100/month, lease dates confirmed

[11/11] Processing: estimated-tax-confirmations/
  -> Extracted: 8 payment confirmations matching intake data

Extraction complete. 10 items flagged for review.
```

[NARRATOR/VOICEOVER]
"A couple things to notice here. First, the interest income from Marcus came back as $1,247.83 -- Alex estimated $1,200 during the intake. This is why we cross-reference documents against verbal answers. The actual 1099 is what matters. Second, the agent found 10 transactions it wants to ask about -- charges that are ambiguous or don't clearly fall into business or personal categories. This is where the review phase gets really interesting."

[YOU SAY]
"Extraction is done. Let's review."

---

## Phase 5: Review (~8-10 minutes)

**This is the main event of the demo. The review phase is where the agent demonstrates its real value.**

[YOU TYPE]
```
/cpa-tax-prep:review 2025
```

[NARRATOR/VOICEOVER]
"The review phase is where this agent really shines. It's going to walk through every category of the tax return, confirm the numbers, and then ask about specific transactions it flagged as unclear. This is exactly what a CPA does in a review meeting -- except it's happening in your terminal."

---

### Income Review

[AGENT SAYS]
"Let's start the review. First, income. I've reconciled your 1099s against your bank deposits. Here's what I found:

**Business Income (Schedule C):**
- TechStart Inc. (1099-NEC): $114,000.00
- GreenLeaf Co. (1099-NEC): $28,000.00
- Other business income (no 1099): $4,850.00
- **Total business income: $146,850.00**

**Other Income:**
- Interest income (1099-INT, Marcus): $1,247.83

**Total gross income: $148,097.83**

The other business income of $4,850 comes from deposits I couldn't match to a 1099. These appear to be the smaller one-off projects you mentioned. Does this look correct?"

[YOU SAY]
"Yes, that's right. The $4,850 is from a couple small projects that were under the 1099 threshold. Total income looks correct."

[NARRATOR/VOICEOVER]
"Notice it caught those small deposits that don't have 1099s attached. A lot of freelancers forget to report income that doesn't come with a 1099 -- but the IRS still expects you to report it. The agent found it in the bank statements."

---

### Business Expenses Review

[AGENT SAYS]
"Next, let's review business expenses. I've categorized your Chase business checking transactions into the following:

**Software & Subscriptions:** $4,128.00
  - Claude Pro: $20/mo x 12 = $240
  - GitHub Team: $25/mo x 12 = $300
  - Vercel Pro: $20/mo x 12 = $240
  - Figma Professional: $15/mo x 12 = $180
  - AWS: varies, total $1,847
  - Google Workspace: $14.40/mo x 12 = $172.80
  - Notion Plus: $10/mo x 12 = $120
  - Linear: $8/mo x 12 = $96
  - Other software: $932.20

**Equipment (Section 179):**
  - MacBook Pro: $2,499.00
  - 4K Monitor + USB-C dock: $1,247.83 (flagged -- will discuss)
  - Standing desk: $445.00
  - **Equipment subtotal: $4,191.83**

**Travel:**
  - Southwest Airlines flight: $487.50 (flagged -- will discuss)
  - Hotel (Miami, 2 nights): $624.00
  - Uber rides (business): $312.00
  - **Travel subtotal: $1,423.50**

**Conferences:**
  - ReactConf ticket: $799.00

**Meals (business, 50% deductible):**
  - Various business meals: $1,247.00

**Professional Services:**
  - TaxPro Services: $2,400.00 (flagged -- will discuss)
  - Registered agent: $149.00
  - **Professional services subtotal: $2,549.00**

**Other/Flagged:**
  - Several transactions flagged for your review

**Total identified business expenses: ~$14,338.33** (before flagged item decisions)

Does the overall picture look right before we go through the flagged items?"

[YOU SAY]
"Yeah, that looks about right. The software subscriptions are all legit -- those are my daily work tools. Equipment looks right too, though let's talk about that Best Buy charge when we get to the flagged items. Let's go through them."

---

### Home Office Review

[AGENT SAYS]
"Before the flagged items, let me confirm the home office deduction. I calculated two separate deductions based on your mid-year move:

**Denver (Jan-Aug, 8 months):**
- Office: 120 sq ft / 1,100 sq ft = 10.91%
- Rent: $2,800/mo x 10.91% = $305.45/mo x 8 = $2,443.64
- Internet: $89/mo x 10.91% = $9.71/mo x 8 = $77.67
- Utilities: $120/mo x 10.91% = $13.09/mo x 8 = $104.73
- **Denver subtotal: $2,626.04**

**Portland (Sep-Dec, 4 months):**
- Office: 140 sq ft / 1,350 sq ft = 10.37%
- Rent: $3,100/mo x 10.37% = $321.48/mo x 4 = $1,285.93
- Internet: $89/mo x 10.37% = $9.23/mo x 4 = $36.92
- Utilities: $120/mo x 10.37% = $12.44/mo x 4 = $49.78
- **Portland subtotal: $1,372.63**

**Total home office deduction: $3,998.67**

Does this look accurate?"

[YOU SAY]
"Yes, the square footage and rent numbers are all correct. That matches my lease agreements."

[NARRATOR/VOICEOVER]
"This is a calculation that trips up so many people who move mid-year. The agent handles it cleanly -- two separate calculations with prorated months, and it even applies the home office percentages to internet and utilities automatically."

---

### Flagged Items Review

[NARRATOR/VOICEOVER]
"Now we get to the best part. The agent found 10 transactions in the bank statements that it couldn't confidently categorize on its own. Rather than guessing, it asks about each one. This is exactly what a good accountant does -- they don't assume."

---

#### Flagged Item 1: Namecheap Domain Renewal

[AGENT SAYS]
"I found a $299.99 charge on 3/14 to NMCHEAP*RENEWAL. Is this a business expense?"

[YOU SAY]
"Yes, that's Namecheap -- I renewed my business domain and a couple of client project domains. All business."

[AGENT SAYS]
"Got it. I'll categorize that as a business expense under 'Internet & Web Services.' $299.99."

[NARRATOR/VOICEOVER]
"The charge showed up as 'NMCHEAP*RENEWAL' on the statement -- not exactly obvious. The agent recognized it might be Namecheap but wanted confirmation before categorizing it."

---

#### Flagged Item 2: Southwest Airlines Flight

[AGENT SAYS]
"There's a $487.50 charge to Southwest Airlines on 6/3. Was this a business trip?"

[YOU SAY]
"Yes, that was my flight to Miami to meet with the GreenLeaf team for a project kickoff."

[AGENT SAYS]
"I'll add that to business travel expenses. I also see the hotel charges from that same trip -- two nights at $312 each. I'll group these together as the GreenLeaf Miami trip."

[NARRATOR/VOICEOVER]
"Notice the agent is connecting the dots. It sees the flight on June 3rd and links it to the hotel charges from the same period. It's building a coherent narrative of the business trip, which is important if the IRS ever asks questions."

---

#### Flagged Item 3: Best Buy Purchase

[AGENT SAYS]
"I see a $1,247.83 charge to Best Buy on 2/18. What was this for?"

[YOU SAY]
"That was a 4K monitor and a USB-C dock for my home office setup. Both 100% business use."

[AGENT SAYS]
"Got it. I'll categorize that as office equipment under Section 179. I already had this in the equipment category -- just wanted to confirm the business use percentage. 100% business, noted."

---

#### Flagged Item 4: Headspace Subscription

[AGENT SAYS]
"There's a recurring $49.99 monthly charge to Headspace. Is this business-related?"

[YOU SAY]
"No, that's personal. Exclude it."

[AGENT SAYS]
"Understood. I'll exclude Headspace from business expenses. That's $49.99 times 12 months, $599.88 total, marked as personal."

[NARRATOR/VOICEOVER]
"This is a great example. A meditation app -- you could try to argue it's for work productivity, but that's a stretch. The agent doesn't make that judgment call. It asks, and Alex correctly says it's personal. Excluded."

---

#### Flagged Item 5: STK Steakhouse

[AGENT SAYS]
"There's a $312.00 charge at STK Steakhouse on 6/5. Was this a business meal?"

[YOU SAY]
"Yes -- that was a dinner with the GreenLeaf Co. team during the Miami trip. There were 4 of us."

[AGENT SAYS]
"I'll categorize that as a business meal. For 2025, business meals are 50% deductible, so $156.00 will be the deductible amount. I'll note it was associated with the GreenLeaf Miami trip, 4 attendees."

[NARRATOR/VOICEOVER]
"The agent correctly applies the 50% meal deduction limit and documents the number of attendees. If you're ever audited, having that level of detail is invaluable."

---

#### Flagged Item 6: Venmo Payment

[AGENT SAYS]
"There's an $89.00 Venmo payment to J. Martinez on 4/22. Can you tell me what this was for?"

[YOU SAY]
"That was splitting a business lunch with my colleague -- we were discussing a potential partnership project. Business expense."

[AGENT SAYS]
"I'll categorize that as a business meal. Same 50% deduction rule applies -- $44.50 deductible. I'll note the business purpose as 'partnership discussion with J. Martinez.'"

[NARRATOR/VOICEOVER]
"Venmo payments are notoriously hard to categorize from a bank statement. There's no description beyond the recipient's name. The agent rightly flags this -- it could be anything. Turns out it was a legitimate business meal."

---

#### Flagged Item 7: TaxPro Services

[AGENT SAYS]
"I see a $2,400 charge to TaxPro Services on 2/5. Is this your accountant?"

[YOU SAY]
"Yes, that's my CPA's fee for preparing last year's taxes. Professional services, 100% business."

[AGENT SAYS]
"I'll categorize that under Professional Services -- tax preparation. This is a fully deductible business expense on Schedule C."

---

#### Flagged Item 8: Creative Market

[AGENT SAYS]
"There's a $175.00 charge to Creative Market on 8/12. Is this business-related?"

[YOU SAY]
"Yes -- I buy design templates and assets there for client projects. All business."

[AGENT SAYS]
"Got it. I'll categorize that as 'Supplies -- Digital Assets' under business expenses."

---

#### Flagged Item 9: Uber to Airport

[AGENT SAYS]
"There's a $65.00 Uber ride on 6/3. Was this business travel?"

[YOU SAY]
"Yes, that was my Uber to Denver International Airport for the Miami trip."

[AGENT SAYS]
"I'll add that to the GreenLeaf Miami trip expenses under ground transportation. That brings the total trip cost to: flight $487.50, hotel $624.00, Uber $65.00, dinner $312.00 -- total $1,488.50, with $156.00 of the dinner subject to the 50% meal limit."

[NARRATOR/VOICEOVER]
"The agent just rolled up the entire Miami trip into a single expense group with correct deduction treatment for each component. That's genuinely useful for record-keeping."

---

#### Flagged Item 10: WeWork Charges

[AGENT SAYS]
"I found two charges to WeWork -- $270 on 10/1 and $270 on 11/1. Is this coworking space?"

[YOU SAY]
"Yes, I used a WeWork hot desk in Portland for a couple months while my home office was being set up after the move. Business expense."

[AGENT SAYS]
"I'll categorize both as 'Rent -- Coworking Space' under business expenses. $540 total. Note: since you're also claiming a home office deduction for those months, I want to flag that you can claim both -- the home office deduction is based on your lease, and the coworking space is a separate business expense. There's no conflict."

[NARRATOR/VOICEOVER]
"That last note is important. Some people worry that using a coworking space invalidates their home office deduction. It doesn't -- they're separate expenses. The agent proactively clarifies that, which is exactly the kind of guidance you'd want from a CPA."

---

### Estimated Taxes Confirmation

[AGENT SAYS]
"Let me confirm your estimated tax payments against the confirmation documents you provided:

- Q1 (4/15/2025): IRS $4,200 -- confirmed. Colorado $1,800 -- confirmed.
- Q2 (6/16/2025): IRS $4,200 -- confirmed. Colorado $1,800 -- confirmed.
- Q3 (9/15/2025): IRS $4,200 -- confirmed. Oregon $2,100 -- confirmed.
- Q4 (1/15/2026): IRS $4,200 -- confirmed. Oregon $2,100 -- confirmed.

Total federal: $16,800. Total Colorado: $3,600. Total Oregon: $4,200. All payments verified against confirmation documents."

[YOU SAY]
"Perfect, that's all correct."

---

### Health Insurance Confirmation

[AGENT SAYS]
"Health insurance: I've confirmed $485.00 per month for 12 months with Blue Cross Blue Shield, totaling $5,820.00. This matches your 1095-A form. The full amount qualifies for the self-employed health insurance deduction on line 17 of Schedule 1."

[YOU SAY]
"Correct."

---

### Retirement Confirmation

[AGENT SAYS]
"Retirement contributions: Roth IRA at Vanguard, $7,000.00 contributed on March 15, 2025. Confirmed against your 5498 form. As a Roth contribution, this is not deductible but will be noted in your records.

That completes the review. Would you like me to generate the final package?"

[YOU SAY]
"Yes, let's package it up."

[NARRATOR/VOICEOVER]
"The review phase is done. Every ambiguous transaction has been resolved, every number has been confirmed. The agent now has a complete, verified picture of Alex's finances for 2025. Let's generate the final output."

---

## Phase 6: Package (~2 minutes)

[YOU TYPE]
```
/cpa-tax-prep:package 2025
```

[NARRATOR/VOICEOVER]
"The package command generates all the final output files that Alex's CPA needs to prepare the actual tax return."

[AGENT SAYS]
```
Generating final tax package for Alex Rivera, TY 2025...

Creating workpapers...
  -> Income summary workpaper
  -> Business expense detail (Schedule C)
  -> Home office calculation (Form 8829)
  -> Estimated tax payment log
  -> Flagged items resolution log

Creating CPA deliverables...
  -> Tax organizer spreadsheet (xlsx)
  -> CPA summary memo
  -> Document index

Package complete. Files saved to tax-prep/2025/output/

Output files:
  tax-prep/2025/output/rivera-2025-tax-organizer.xlsx
  tax-prep/2025/output/rivera-2025-cpa-summary.md
  tax-prep/2025/output/rivera-2025-document-index.md
  tax-prep/2025/workpapers/income-summary.md
  tax-prep/2025/workpapers/schedule-c-expenses.md
  tax-prep/2025/workpapers/home-office-8829.md
  tax-prep/2025/workpapers/estimated-taxes.md
  tax-prep/2025/workpapers/flagged-items-resolution.md
```

[NARRATOR/VOICEOVER]
"Let's look at what it generated."

[YOU SAY]
"Let me open the CPA summary first."

[YOU TYPE]
```
cat tax-prep/2025/output/rivera-2025-cpa-summary.md
```

[NARRATOR/VOICEOVER]
"The CPA summary is a one-page memo that gives the accountant a complete overview. It covers the filing situation -- single filer, single-member LLC, part-year resident of two states. It lists all income sources with amounts, summarizes deductions, notes the mid-year move and dual home office situation, confirms estimated tax payments, and calls out anything unusual the CPA should be aware of."

[YOU SAY]
"Now let's look at the spreadsheet."

[YOU TYPE]
```
open tax-prep/2025/output/rivera-2025-tax-organizer.xlsx
```

[NARRATOR/VOICEOVER]
"The tax organizer is an Excel file with multiple tabs -- income, expenses broken down by Schedule C category, home office calculations, estimated payments, and the flagged item resolutions with notes. This is the document that makes your CPA's life dramatically easier. Instead of handing them a shoebox of receipts, you're handing them a clean, organized, verified spreadsheet."

---

## Wrap-Up (~2 minutes)

[NARRATOR/VOICEOVER]
"Let's recap what just happened. In about 25 minutes, we took a fairly complex tax situation -- freelancer, single-member LLC, mid-year state move, multiple clients, mixed-use bank accounts, equipment purchases, a business trip, and coworking expenses -- and turned it into a CPA-ready package."

[YOU SAY]
"Let me show you the final folder structure."

[YOU TYPE]
```
tree tax-prep/2025/
```

[NARRATOR/VOICEOVER]
"Everything is organized. Original documents are preserved in the documents folder. The workpapers show the agent's calculations and categorizations. And the output folder has the final deliverables for the CPA."

[YOU SAY]
"A few things I want to highlight about what the agent did well here."

[NARRATOR/VOICEOVER]
"First -- the flagged items. The agent didn't guess on ambiguous transactions. It asked. That Namecheap renewal, the Venmo payment, the WeWork charges -- those are exactly the kinds of things that get miscategorized when you do this yourself. Having the agent surface them and ask is a huge win.

Second -- the mid-year move. Handling part-year residency in two states, with two separate home office calculations, two sets of state estimated tax payments -- that's genuinely complex. The agent handled it correctly.

Third -- the trip grouping. It automatically connected the Southwest flight, the Miami hotel, the Uber to the airport, and the steakhouse dinner into a single business trip. That's the kind of organization that matters in an audit.

And finally -- the output. The CPA summary and the spreadsheet are exactly what an accountant wants to receive. It saves them time, which saves you money on their bill."

[YOU SAY]
"That's the Tax Prep Agent. If you're a freelancer or small business owner, this is what tax prep should feel like -- structured, thorough, and painless. Thanks for watching."

---

## Timing Summary

| Phase | Estimated Duration |
|---|---|
| Opening + Initialize | ~2 min |
| Drop Documents | ~2 min |
| Intake Interview (9 sections) | ~8-10 min |
| Extraction | ~3 min |
| Review (income, expenses, home office, 10 flagged items, confirmations) | ~8-10 min |
| Package + Output Tour | ~2 min |
| Wrap-Up | ~2 min |
| **Total** | **~27-31 min** |

---

## Tips for Recording

1. **Pace yourself during the intake.** Don't rush through the answers. Let each response breathe -- the viewer needs time to read the agent's output.

2. **Pause on the flagged items.** This is the demo's showcase moment. After each flagged item, give a brief beat before moving to the next one. The Headspace exclusion and the WeWork clarification are particularly good moments to linger on.

3. **Show the output files.** Don't skip the package phase. Scroll through the CPA summary and at least one tab of the spreadsheet. This is the payoff.

4. **Keep your terminal clean.** Clear between phases if needed. The viewer should always be able to read the current output.

5. **If something goes wrong, keep rolling.** Errors and retries are authentic. If the agent asks an unexpected follow-up question, answer it naturally. It makes the demo feel real.

6. **Consider B-roll.** For the extraction phase (which may take 30-60 seconds of processing), consider a brief voiceover explaining what's happening under the hood rather than watching a loading spinner.

7. **End on the spreadsheet.** The final visual should be the polished xlsx open in a spreadsheet app. That's the tangible deliverable -- it's satisfying to see.
