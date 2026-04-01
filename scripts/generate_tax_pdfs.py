"""
Generates comprehensive, detailed tax PDF documents for all supported countries.
Covers income tax rates, corporate tax, GST/VAT, deduction limits, land tax,
industry-specific rules, non-resident tax policies, tax cuts, and more.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "PDF")

COUNTRIES = {
    "US": {
        "folder": "US",
        "title": "United States (USA) Comprehensive Tax Guide 2024",
        "sections": [
            ("Income Tax Rates (Federal)", [
                "Individual Income Tax brackets (2024):",
                "- 10%: $0 - $11,600 (Single); $0 - $23,200 (Married Filing Jointly)",
                "- 12%: $11,601 - $47,150 (Single); $23,201 - $94,300 (MFJ)",
                "- 22%: $47,151 - $100,525 (Single); $94,301 - $201,050 (MFJ)",
                "- 24%: $100,526 - $191,950 (Single); $201,051 - $383,900 (MFJ)",
                "- 32%: $191,951 - $243,725 (Single); $383,901 - $487,450 (MFJ)",
                "- 35%: $243,726 - $609,350 (Single); $487,451 - $731,200 (MFJ)",
                "- 37%: Over $609,350 (Single); Over $731,200 (MFJ)",
                "Standard Deduction: $14,600 (Single), $29,200 (MFJ), $21,900 (Head of Household)",
            ]),
            ("Corporate Tax Rates", [
                "Federal Corporate Income Tax: Flat 21% rate (since Tax Cuts and Jobs Act 2017).",
                "Small Business (Pass-through entities): 20% deduction under Sec. 199A.",
                "Alternative Minimum Tax (AMT): 15% corporate AMT for companies earning over $1 billion.",
                "State Corporate Tax Rates: Range from 0% (Wyoming, SD) to 11.5% (New Jersey).",
            ]),
            ("Sales Tax / GST / VAT", [
                "No federal GST or VAT system exists in the USA.",
                "State Sales Tax Rates:",
                "- California: 7.25% base; up to 10.75% with local additions",
                "- Texas: 6.25% state + up to 2% local = 8.25% max",
                "- New York: 4% state + 4.5% NYC local = 8.875%",
                "- Florida: 6% with local surtax typically 0.5-1.5%",
                "- 5 states have no sales tax: Alaska, Delaware, Montana, New Hampshire, Oregon",
            ]),
            ("Deduction Limits & Tax Incentives", [
                "Form 2106 Business Expense Deduction limit: $10,000 (SALT deduction cap).",
                "401(k) contribution limit: $23,000 (under 50); $30,500 (50 and over) for 2024.",
                "IRA (Traditional/Roth) limit: $7,000; $8,000 if age 50+.",
                "HSA contribution limit: $4,150 (individual); $8,300 (family).",
                "Child Tax Credit: $2,000 per qualifying child.",
                "Earned Income Tax Credit (EITC): Up to $7,830 for 3+ children.",
                "Mortgage interest deduction: Up to $750,000 in mortgage debt.",
                "Charitable deduction: Up to 60% of AGI for cash donations.",
            ]),
            ("Capital Gains Tax", [
                "Short-term capital gains: Taxed as ordinary income (up to 37%).",
                "Long-term capital gains (held 1+ year) rates:",
                "- 0% for income up to $47,025 (Single) or $94,050 (MFJ)",
                "- 15% for income $47,026 - $518,900 (Single) or $94,051 - $583,750 (MFJ)",
                "- 20% for income above those thresholds.",
                "Net Investment Income Tax: 3.8% surcharge on investment income above $200k (Single)/$250k (MFJ).",
            ]),
            ("Industry-Specific Tax Rules", [
                "Real Estate / Land Tax: Varies by state and county. Typical rate: 0.3% - 2.5% of assessed value.",
                "   - New Jersey: 2.16% average (highest in USA)",
                "   - Hawaii: 0.28% average (lowest in USA)",
                "Oil & Gas Companies: Percentage depletion allowance (15% of gross income).",
                "Agriculture: Special exclusions for farm income and land.",
                "Technology/R&D: R&D Tax Credit (Section 41) worth 20% of eligible expenses.",
                "Non-profit Entities: Exempt from federal income tax (501(c)(3) status).",
            ]),
            ("Non-Resident Tax Policies", [
                "Non-resident aliens (NRA) are taxed only on US-source income.",
                "FDAP Income (Fixed, Determinable, Annual, Periodical): 30% withholding tax (or lower per treaty).",
                "ECI (Effectively Connected Income): Taxed at standard graduated rates.",
                "FIRPTA: 15% withholding on sale of US real property by foreign persons.",
                "Foreign tax treaties reduce withholding to 0-15% depending on country.",
            ]),
            ("Tax Filing Deadlines", [
                "Individual tax return (Form 1040): April 15.",
                "Extension available: October 15 (Form 4868 by April 15).",
                "Corporate tax return (Form 1120): April 15 (or 2.5 months after fiscal year end).",
                "Estimated quarterly taxes: April 15, June 17, Sept 16, Jan 15.",
                "FBAR (Foreign Bank Account Report): April 15 (auto-extension to Oct 15).",
            ]),
            ("Recent Tax Changes & Cuts", [
                "Tax Cuts and Jobs Act 2017: Reduced corporate rate from 35% to 21%.",
                "Inflation Reduction Act 2022: 15% corporate minimum tax; 1% excise tax on stock buybacks.",
                "SECURE 2.0 Act: Enhanced retirement savings provisions.",
                "Proposed 2024 Biden Budget: 28% corporate tax rate (not enacted).",
            ]),
        ]
    },
    "UK": {
        "folder": "UK",
        "title": "United Kingdom Comprehensive Tax Guide 2024-25",
        "sections": [
            ("Income Tax Rates", [
                "Personal Allowance (tax-free): £12,570 per year.",
                "Basic Rate: 20% on income from £12,571 to £50,270.",
                "Higher Rate: 40% on income from £50,271 to £125,140.",
                "Additional Rate: 45% on income above £125,140.",
                "Scottish Income Tax rates differ slightly (19%, 20%, 21%, 42%, 47%).",
                "Dividend Tax Rate: 8.75% (basic), 33.75% (higher), 39.35% (additional).",
            ]),
            ("Corporate Tax Rates", [
                "Main Rate (profits over £250,000): 25%.",
                "Small Profits Rate (profits up to £50,000): 19%.",
                "Marginal Relief: Applies for profits between £50,000 - £250,000.",
                "Research and Development Relief: Enhanced 186% deduction for qualifying SMEs.",
                "Patent Box: 10% rate for profits from patented inventions.",
            ]),
            ("VAT (Value Added Tax)", [
                "Standard Rate: 20% on most goods and services.",
                "Reduced Rate: 5% (domestic fuel/power, some construction, children's car seats).",
                "Zero Rate: 0% (food, books, children's clothing, exports).",
                "VAT Registration Threshold: £90,000 annual turnover.",
                "VAT Return: Quarterly or annually via Making Tax Digital.",
            ]),
            ("Deduction Limits & Allowances", [
                "£1,000 Trading Allowance: Tax-free for self-employed sole traders.",
                "£1,000 Property Allowance: Tax-free for rental income.",
                "Marriage Allowance: Transfer £1,260 of personal allowance to spouse.",
                "Annual ISA Allowance: £20,000 tax-free savings per year.",
                "Pension Annual Allowance: £60,000 or 100% of earnings (whichever is lower).",
                "Capital Gains Annual Exempt Amount: £3,000 (2024-25).",
            ]),
            ("Land & Property Tax", [
                "Stamp Duty Land Tax (SDLT) in England & N. Ireland:",
                "- 0% up to £250,000 (residential); £425,000 first-time buyers",
                "- 5% from £250,001 to £925,000",
                "- 10% from £925,001 to £1.5 million",
                "- 12% above £1.5 million",
                "- Additional 3% surcharge for second homes/buy-to-let",
                "Council Tax: Based on property band (A to H) set by local authority.",
                "Land & Buildings Transaction Tax (Scotland): Different thresholds apply.",
            ]),
            ("Non-Resident Tax Policies", [
                "Non-resident individuals pay UK tax only on UK-source income.",
                "Non-resident landlord scheme: 20% withholding on rent unless approved otherwise.",
                "Non-dom Tax: Remittance basis available (charge after 7 years UK residence).",
                "Statutory Residence Test determines UK tax residency.",
                "Double tax treaties exist with 130+ countries.",
                "Withholding tax on dividends to non-residents: 0% (no withholding on UK dividends).",
                "Withholding on interest to non-residents: 20% (unless treaty relief).",
            ]),
            ("Industry-Specific Tax Rules", [
                "Financial Services: Ring-fence around retail banking activities.",
                "Oil & Gas: Ring Fence Corporation Tax at 30%; Supplementary Charge 10%.",
                "Charities: Exempt from corporation tax on charitable income.",
                "Property developers: Different rules on land remediation relief.",
                "Creative Industries: Film Tax Relief (34%), Animation (39%), Video Games (34%).",
            ]),
            ("Capital Gains Tax (CGT)", [
                "Basic rate taxpayers: 10% (18% for residential property).",
                "Higher/Additional rate taxpayers: 20% (24% for residential property).",
                "Business Asset Disposal Relief (BADR): 10% rate on first £1 million lifetime gains.",
                "Private Residence Relief: No CGT on your main home.",
            ]),
            ("Tax Filing Deadlines", [
                "Self Assessment paper return: October 31 (following tax year ending April 5).",
                "Self Assessment online return: January 31.",
                "Corporation Tax payment: 9 months and 1 day after accounting period ends.",
                "VAT returns: 1 month and 7 days after the end of VAT accounting period.",
            ]),
        ]
    },
    "AUSTRALIA": {
        "folder": "AUSTRALIA",
        "title": "Australia Comprehensive Tax Guide 2024-25",
        "sections": [
            ("Income Tax Rates (Individual)", [
                "Resident tax rates 2024-25:",
                "- 0%: $0 - $18,200 (tax-free threshold)",
                "- 19%: $18,201 - $45,000",
                "- 32.5%: $45,001 - $135,000",
                "- 37%: $135,001 - $190,000",
                "- 45%: Over $190,000",
                "Medicare Levy: 2% on most taxable income (income above threshold).",
                "Low Income Tax Offset (LITO): Up to $700 for income under $37,500.",
                "Stage 3 Tax Cuts (effective 1 July 2024): Reduced 19% tax bracket ceiling to $45,000 and merged 32.5%/37% bracket.",
            ]),
            ("Corporate Tax Rates", [
                "General corporate tax rate: 30%.",
                "Small business entity tax rate: 25% (annual turnover under $50 million).",
                "Base rate entities eligible for 25% rate if passive income is less than 80% of total income.",
                "Research & Development (R&D) Tax Incentive:",
                "- 43.5% refundable offset for companies with turnover < $20 million",
                "- 38.5% non-refundable offset for larger companies",
            ]),
            ("GST (Goods and Services Tax)", [
                "Standard GST rate: 10% on most goods and services.",
                "GST-free supplies: Fresh food, medical services, education, exports, international travel.",
                "Input-taxed supplies: Financial services, residential rental (no GST charged, no credit claimed).",
                "GST registration required if annual turnover exceeds $75,000.",
                "GST return: Monthly, quarterly, or annual (depending on turnover).",
            ]),
            ("PAYG Withholding (Pay As You Go)", [
                "PAYG withholding rate: 1.5% - 20% depending on income level.",
                "Employers withhold PAYG from employee wages and remit to ATO.",
                "PAYG instalments: Quarterly prepayment of expected tax for businesses.",
            ]),
            ("Fringe Benefits Tax (FBT)", [
                "FBT rate: 47% (gross-up rate applied to employer-provided benefits).",
                "FBT year: 1 April to 31 March.",
                "Examples of FBT items: Company cars, private health insurance, entertainment.",
                "Salary packaging arrangements used to minimise FBT.",
            ]),
            ("Capital Gains Tax (CGT)", [
                "50% CGT discount for assets held longer than 12 months (individuals).",
                "33.3% discount for compliant superannuation funds.",
                "No discount for companies (full gain is taxable).",
                "Main residence exemption: Full or partial CGT exemption on primary home.",
                "Small business CGT concessions: Up to 100% exemption under conditions.",
            ]),
            ("Land Tax", [
                "Land tax in Australia is levied by state/territory governments, not federally.",
                "New South Wales (NSW): 1.6% on value above $1,075,000; 2% above $6,571,000.",
                "Victoria (VIC): 0.2% - 2.25% depending on land value (0% below $300,000 threshold).",
                "Queensland (QLD): 1.6% on value above $600,000 for individuals.",
                "South Australia (SA): 0.5% - 2.4% on value above $723,000.",
                "Western Australia (WA): 0.6% - 2.67% on value above $300,000.",
                "Tax Cuts: South Australia abolished land tax for primary production in 2023.",
                "National Residential Property Tax: Under review (government consultation 2024).",
            ]),
            ("Deduction Limits", [
                "$300 (Work-Related Expenses): Claim without receipts if under $300 total.",
                "Home Office Deduction: Fixed rate 67 cents per hour (2024).",
                "Superannuation Concessional Contributions: $27,500 per year.",
                "Superannuation Non-Concessional Contributions: $110,000 per year cap.",
                "Car expense deduction: 85 cents per km method (up to 5,000 km), or logbook method.",
                "Rental Property Deductions: Interest, maintenance, depreciation, rates, insurance.",
                "Negative Gearing: Loss on rental property deductible against all income.",
            ]),
            ("Non-Resident Tax Policies", [
                "Non-residents taxed only on Australian-source income.",
                "Non-resident individual tax rates:",
                "- 32.5% on income $0 - $135,000",
                "- 37% on $135,001 - $190,000",
                "- 45% on over $190,000",
                "No tax-free threshold for non-residents.",
                "Foreign residents pay 12.5% withholding tax on property sale proceeds.",
                "Dividend withholding tax for non-residents: 30% (reduced by treaty to 5-15%).",
                "Interest withholding tax: 10% (reduced by treaties).",
                "Royalties withholding tax: 30% (reduced by treaties).",
            ]),
            ("Industry-Specific Tax Rules", [
                "Mining/Resources: Petroleum Resource Rent Tax (PRRT) on gas projects; 40% rate.",
                "Agriculture: Primary Production concessions; farm management deposits scheme.",
                "Film Industry: Producer Offset tax rebate of 40% for Australian films.",
                "Startups: Employee Share Scheme (ESS) concessions; startup tax concession.",
                "Financial Services: Managed Investment Trusts (MITs) - special tax rules.",
            ]),
            ("Tax Filing Deadlines", [
                "Individual tax return: October 31 (or May 15 if using a tax agent).",
                "Company income tax return: 28 February (or later with tax agent).",
                "BAS (Business Activity Statement): 28 days after the end of each quarter.",
                "FBT annual return: 21 May.",
                "PAYG withholding summary: Due 14 August.",
            ]),
        ]
    },
    "INDIA": {
        "folder": "INDIA",
        "title": "India Comprehensive Tax Guide FY 2024-25 (AY 2025-26)",
        "sections": [
            ("Income Tax Rates - New Tax Regime (Default)", [
                "- 0%: Up to ₹3,00,000",
                "- 5%: ₹3,00,001 - ₹7,00,000",
                "- 10%: ₹7,00,001 - ₹10,00,000",
                "- 15%: ₹10,00,001 - ₹12,00,000",
                "- 20%: ₹12,00,001 - ₹15,00,000",
                "- 30%: Above ₹15,00,000",
                "Rebate u/s 87A: Full tax rebate for income up to ₹7,00,000 in new regime.",
                "Standard Deduction: ₹75,000 (new regime from FY 2024-25).",
            ]),
            ("Income Tax Rates - Old Tax Regime", [
                "- 0%: Up to ₹2,50,000 (₹3,00,000 for senior citizens; ₹5,00,000 super senior)",
                "- 5%: ₹2,50,001 - ₹5,00,000",
                "- 20%: ₹5,00,001 - ₹10,00,000",
                "- 30%: Above ₹10,00,000",
                "Surcharge: 10% (₹50L-₹1Cr); 15% (₹1Cr-₹2Cr); 25% (₹2Cr-₹5Cr); 37% (above ₹5Cr - old regime only).",
                "Health and Education Cess: 4% on income tax + surcharge.",
            ]),
            ("Corporate Tax Rates", [
                "Domestic companies (General): 30% + surcharge + cess.",
                "Domestic companies (New Sec 115BAB - Manufacturing from 2023): 15% + 10% surcharge + 4% cess = effective 17.01%.",
                "Domestic companies (Sec 115BAA - no exemptions): 22% base = effective 25.17%.",
                "Foreign companies: 40% base rate.",
                "Minimum Alternate Tax (MAT): 15% of book profit.",
                "Dividend Distribution Tax: Abolished; dividends now taxable in shareholder hands.",
            ]),
            ("GST (Goods and Services Tax)", [
                "GST is a multi-stage, value-added tax replacing multiple State and Central taxes.",
                "GST Rates:",
                "- 0%: Essential items (grains, fresh vegetables, milk, eggs, books, newspapers)",
                "- 5%: Packed food items, packaged water, medicines, apparels up to ₹1000",
                "- 12%: Butter, cheese, agarbatti, mobile phones",
                "- 18%: Most services, TV, computers, soaps, toothpaste, CCTV",
                "- 28%: Luxury goods, tobacco, automobiles, cement, ACs, DTH service",
                "Special Rates: 0.25% (diamonds/gemstones); 3% (gold/silver).",
                "GST Registration: Mandatory if turnover exceeds ₹20 lakh (₹10 lakh in North-east/hill states).",
            ]),
            ("Deduction Limits (Old Regime)", [
                "Section 80C: Up to ₹1,50,000. Eligible investments include: Equity Linked Savings Scheme (ELSS) mutual funds with 3-year lock-in, Public Provident Fund (PPF) with 15-year maturity, Employees' Provident Fund (EPF), National Savings Certificate (NSC) with 5-year lock-in, Life Insurance premium payments, Repayment of principal amount on a home loan, Tuition fees paid for up to two children, 5-year fixed deposits with banks or post offices, and Senior Citizens Savings Scheme (SCSS).",
                "Section 80CCC: Deduction for payments towards pension funds, sub-limit under the overall ₹1.5 lakh 80C umbrella.",
                "Section 80CCD(1): Deduction for contribution to National Pension System (NPS), up to 10% of salary (or 20% of gross total income for self-employed), within the ₹1.5 lakh 80C limit.",
                "Section 80CCD(1B): Additional deduction of ₹50,000 for NPS contribution, above the 80C limit (bringing total potential to ₹2,00,000 for NPS savers).",
                "Section 80D: Deduction for health insurance premiums. Limits are ₹25,000 for self/spouse/children and an additional ₹25,000 for parents. If parents are senior citizens, the limit is ₹50,000. Total maximum deduction can be ₹75,000 or ₹1,00,000 depending on age of taxpayer and parents. Also covers ₹5,000 for preventive health check-up within the overall limit.",
                "Section 80E: Full deduction on interest paid on education loan for higher studies. Available for a maximum of 8 consecutive years.",
                "Section 80EEA: Additional deduction of up to ₹1,50,000 for interest on housing loan for first-time homebuyers if stamp duty value of house is ≤ ₹45 lakh.",
                "Section 80G: 50% or 100% deduction on donations to approved charitable funds or institutions (e.g., PM CARES, Chief Minister Relief Fund). Limit applies based on adjusted gross total income in some cases.",
                "Section 80TTA: Up to ₹10,000 deduction on savings bank interest for individuals and HUF (excluding senior citizens).",
                "Section 80TTB: Up to ₹50,000 deduction on interest income (from savings, FDs, RDs) for senior citizens.",
                "HRA Exemption: Minimum of (actual HRA received; 50% of salary for metro cities or 40% for non-metros; excess of rent paid over 10% of salary).",
                "LTA Exemption: Leave Travel Allowance for actual domestic travel expenses (twice in a block of 4 years).",
            ]),
            ("Capital Gains Tax", [
                "Short-Term Capital Gains (STCG):",
                "- Listed securities (STT paid): 20% (Budget 2024 revision from 15%).",
                "- Others: As per income tax slab.",
                "Long-Term Capital Gains (LTCG):",
                "- Listed equity/units: 12.5% over ₹1,25,000 annual exemption (Budget 2024: raised from 10%, exemption from ₹1L).",
                "- Real property, unlisted shares: 12.5% without indexation (Budget 2024 change).",
                "- Debt mutual funds: As per slab rate (indexation removed from 2023).",
            ]),
            ("Land & Property Tax", [
                "Property tax is levied by local municipal bodies (not central government).",
                "Rates vary widely by state and city.",
                "Stamp Duty on Property Purchase:",
                "- Maharashtra: 5-6%",
                "- Delhi: 4% (women), 6% (men)",
                "- Karnataka: 3-5%",
                "- Tamil Nadu: 7%",
                "Registration charges: 1% of property value in most states.",
                "TDS on Property: 1% TDS if property value exceeds ₹50 lakh.",
            ]),
            ("Non-Resident Tax Policies (NRI)", [
                "NRI taxed only on India-sourced income.",
                "Rental income: Taxable; tenant must deduct 30% TDS.",
                "Interest income:",
                "- NRE Account: Tax-exempt in India.",
                "- NRO Account: Taxable; 30% TDS.",
                "- FCNR Account: Tax-exempt.",
                "STCG on equity: 20%; LTCG on equity: 12.5% above ₹1.25 lakh.",
                "Dividend Withholding Tax: 20% (can be reduced by DTAA).",
                "India has DTAAs with 90+ countries for reduced withholding rates.",
            ]),
            ("Industry-Specific Tax Rules", [
                "SEZ Units: 100% tax exemption for 5 years; 50% for next 5 years.",
                "Startups: 100% profit deduction for 3 consecutive years out of 10 (Sec 80-IAC).",
                "IFSC (Gift City): 10% corporate tax; no GST on IFSC services.",
                "Cooperative Societies: Special slabs; 22% for new cooperatives (Sec 115BAD).",
                "Real Estate Investment Trusts (REITs): Pass-through taxation.",
                "Shipping Companies: Tonnage Tax scheme.",
            ]),
            ("Tax Filing Deadlines", [
                "Individuals (non-audit): July 31.",
                "Businesses (audit required): October 31.",
                "Transfer pricing audit cases: November 30.",
                "Belated return: December 31 (with late fee).",
                "Advance Tax installments: June 15 (15%), September 15 (45%), December 15 (75%), March 15 (100%).",
            ]),
        ]
    },
    "CANADA": {
        "folder": "CANADA",
        "title": "Canada Comprehensive Tax Guide 2024",
        "sections": [
            ("Federal Income Tax Rates", [
                "- 15%: First $55,867",
                "- 20.5%: $55,868 - $111,733",
                "- 26%: $111,734 - $154,906",
                "- 29%: $154,907 - $220,000",
                "- 33%: Over $220,000",
                "Basic Personal Amount: $15,705 (tax-free credit reducing taxes by $2,356).",
                "Provincial Tax: Additional 5.05% - 25.75% depending on province.",
                "Combined top marginal rate (federal + provincial): 53.53% in Nova Scotia.",
            ]),
            ("Corporate Tax Rates", [
                "Federal Corporate Tax: 15% base rate (after general rate reduction of 13%).",
                "Small Business Deduction (SBD): 9% net federal tax on first $500,000 active income.",
                "Provincial corporate tax: 0% (AB) to 16% (PEI); average ~11-12%.",
                "Combined effective rate for small biz: ~9-12% approx.",
                "Scientific Research and Experimental Development (SR&ED): 15-35% tax credit.",
                "Accelerated Investment Incentive: Enhanced first-year depreciation for capital purchases.",
            ]),
            ("GST / HST / PST", [
                "Federal GST rate: 5%.",
                "Harmonized Sales Tax (HST) in participating provinces:",
                "- Ontario: 13% (5% federal + 8% provincial)",
                "- Nova Scotia: 15%",
                "- New Brunswick: 15%",
                "- Prince Edward Island: 15%",
                "- Newfoundland & Labrador: 15%",
                "Provinces with GST + separate PST:",
                "- British Columbia: 5% GST + 7% PST = 12%",
                "- Saskatchewan: 5% GST + 6% PST = 11%",
                "- Manitoba: 5% GST + 7% RST = 12%",
                "- Quebec: 5% GST + 9.975% QST = ~14.975%",
                "GST/HST registration required if annual revenue exceeds $30,000.",
            ]),
            ("Deduction Limits", [
                "Line 22900 Other Employment Expenses: $1,000 flat deduction (T2200 required for more).",
                "RRSP (Registered Retirement Savings Plan): 18% of previous year earned income, max $31,560 (2024).",
                "TFSA (Tax-Free Savings Account): $7,000 annual contribution room (2024); lifetime ~$95,000.",
                "RESP (Education): $2,500/year to get Canada Education Savings Grant of 20% ($500/year).",
                "Work-From-Home Deduction: $2/day flat rate (up to $500) or detailed method with T2200.",
                "Child Care Expenses: Up to $8,000 (under 7), $5,000 (7-16).",
                "Capital Cost Allowance (CCA): Depreciation on business assets by class.",
            ]),
            ("Land & Property Tax", [
                "Property tax (municipal): Varies widely by municipality, average 0.5% to 2.5% of assessed value.",
                "Land Transfer Tax in Ontario: 0.5% to 2.5% depending on value; extra 1% for Toronto.",
                "BC Property Transfer Tax: 1% up to $200k; 2% up to $2M; 3% up to $3M; 5% above $3M.",
                "Federal GST/HST applies to new home purchases (rebates available for homes under $450,000).",
                "Non-Resident Speculation Tax (NRST): 25% in Ontario; 20% in BC.",
            ]),
            ("Non-Resident Tax Policies", [
                "Non-residents taxed on Canadian-source income only.",
                "Rental income: 25% withholding tax (can elect to file NR6 for net income).",
                "Employment income from Canadian source: Full graduated rates apply.",
                "Dividends paid to non-residents: 25% withholding (reduced by treaty - e.g., 15% US/Can treaty).",
                "Interest paid to non-residents: 25% withholding (reduced under most treaties to 0-10%).",
                "Capital gains on Canadian taxable property: Regular capital gains rules apply; T2062 required.",
                "Canada has tax treaties with over 90 countries.",
            ]),
            ("Capital Gains Tax", [
                "50% of capital gains included in taxable income (inclusion rate for individuals).",
                "For corporations/trusts and individual gains exceeding $250,000: 2/3 (66.7%) inclusion rate (2024 Budget).",
                "Principal Residence Exemption: No tax on sale of your primary home.",
                "Lifetime Capital Gains Exemption (LCGE): $1,016,602 for qualified small business shares (2024).",
                "$1 million lifetime exemption for qualified farm property.",
            ]),
            ("Tax Filing Deadlines", [
                "Individual (T1): April 30.",
                "Self-employed individuals: June 15 (balance owing still due April 30).",
                "Corporate (T2): 6 months after fiscal year end.",
                "GST/HST returns: Quarterly (28 days after quarter end) or monthly.",
                "T4 slips (employer): February 28.",
            ]),
        ]
    },
    "GERMANY": {
        "folder": "GERMANY",
        "title": "Germany Comprehensive Tax Guide 2024",
        "sections": [
            ("Income Tax Rates (Einkommensteuer)", [
                "- 0%: Up to €11,604 (basic tax-free allowance / Grundfreibetrag)",
                "- 14% to 42%: Progressive rates from €11,605 to €277,825 (linear progression)",
                "- 42% top rate: €66,761 to €277,825",
                "- 45% (Reichensteuer): Above €277,826",
                "Solidarity Surcharge (Solidaritätszuschlag): 5.5% of income tax (for high earners only).",
                "Church Tax (Kirchensteuer): 8-9% of income tax (optional, only for church members).",
            ]),
            ("Corporate Tax Rates (Körperschaftsteuer)", [
                "Corporate Income Tax: 15% flat rate.",
                "Solidarity Surcharge: 5.5% of corporate tax = 15.825% effective federal rate.",
                "Trade Tax (Gewerbesteuer): 7% base rate × municipal multiplier (around 3.5x average) = ~14-17%.",
                "Total effective combined rate: Typically 30-33%.",
                "Participation Exemption: 95% of dividends and capital gains from subsidiaries tax-exempt.",
                "Loss Carryforward: Unlimited in time but limited to €1 million + 60% of excess per year.",
            ]),
            ("VAT (Umsatzsteuer)", [
                "Standard VAT rate: 19%.",
                "Reduced rate: 7% (food, books, public transport, cultural events, hotels).",
                "Zero rated: Intra-EU and export transactions.",
                "VAT registration threshold: €22,000 (2024 turnover; new threshold from 2025: €25,000).",
                "VAT returns: Monthly or quarterly advance returns; annual return required.",
            ]),
            ("Deduction Limits (Werbungskosten / Betriebsausgaben)", [
                "Employee Standard Deduction (Arbeitnehmer-Pauschbetrag): €1,230 per year.",
                "Home Office Deduction: €6 per day, capped at €1,260 per year (without specific room).",
                "Commuting Deduction: €0.30/km for first 20km; €0.38/km beyond 20km.",
                "Special Expenses (Sonderausgaben): Church tax, alimony, donations (20% of income cap).",
                "Extraordinary Burdens (Außergewöhnliche Belastungen): Medical expenses over reasonable burden.",
                "Pension/Retirement contributions: Up to €27,566 deductible (2024).",
                "Child Allowance (Kinderfreibetrag): €6,612 per child (or child benefit €250/month).",
            ]),
            ("Land & Property Tax (Grundsteuer)", [
                "Property Tax Reform 2025: New calculation based on property value, area, and age.",
                "Current rate: Assessed unit value × property tax assessment rate × municipal multiplier.",
                "Average effective rates: 0.3% - 1.2% of property value per year.",
                "Berlin: ~0.8%; Munich: ~0.35%; Hamburg: ~0.7%.",
                "Real Estate Transfer Tax (RETT / Grunderwerbsteuer): 3.5% - 6.5% depending on state:",
                "- Bavaria & Saxony: 3.5%",
                "- North Rhine-Westphalia & Thuringia: 6.5%",
                "- Berlin: 6%",
            ]),
            ("Non-Resident Tax Policies", [
                "Limited tax liability: Non-residents taxed only on German-source income.",
                "Withholding tax on dividends: 25% + solidarity surcharge = 26.375%.",
                "Withholding tax on interest: 25% + solidarity surcharge (bank interest).",
                "Royalties to non-residents: 15% withholding.",
                "Reduced rates under tax treaties (e.g., 5-15% for EU parent companies).",
                "EU Parent-Subsidiary Directive: 0% withholding on qualifying EU dividends.",
                "Germany has 100+ tax treaties worldwide.",
            ]),
            ("Industry-Specific Tax Rules", [
                "R&D Tax Credit: 25% credit on eligible R&D wages/salaries (max €25M per year).",
                "Investment Grants (Investitionszulagengesetz): Former East Germany subsidies.",
                "Real Estate/Construction: VAT applicable on construction but options exist.",
                "Financial Sector: Specific regulatory tax for banks; flat-rate capital gains scheme.",
                "Agriculture/Forestry: Special average-rate taxation option (9%).",
            ]),
            ("Capital Gains Tax", [
                "Capital gains on investments (Abgeltungsteuer): 25% flat rate + solidarity surcharge = ~26.375%.",
                "Annual exemption (Sparerpauschbetrag): €1,000 per person (€2,000 for couples).",
                "Real property held over 10 years: Tax-exempt.",
                "Private real estate sold within 10 years: Taxed as ordinary income.",
                "Business asset gains: Taxable at normal income rates.",
            ]),
            ("Tax Filing Deadlines", [
                "Individual income tax return (Einkommensteuererklärung): July 31.",
                "With tax advisor: Up to February 28/29 of the following year.",
                "Corporate tax / trade tax: July 31 (with extension via tax advisor to February 28).",
                "VAT advance return: 10th of the following month (monthly or quarterly).",
                "Annual VAT return: July 31 with extension options.",
            ]),
        ]
    },
    "CHINA": {
        "folder": "CHINA",
        "title": "China Comprehensive Tax Guide 2024",
        "sections": [
            ("Individual Income Tax (IIT) Rates", [
                "Comprehensive income (wages/salaries, remuneration, royalties, manuscripts) - Annual rates:",
                "- 3%: Up to ¥36,000",
                "- 10%: ¥36,001 - ¥144,000",
                "- 20%: ¥144,001 - ¥300,000",
                "- 25%: ¥300,001 - ¥420,000",
                "- 30%: ¥420,001 - ¥660,000",
                "- 35%: ¥660,001 - ¥960,000",
                "- 45%: Over ¥960,000",
                "Basic Standard Deduction: ¥60,000 per year (¥5,000/month) for residents.",
                "Special Additional Deductions: Child education, continuing education, medical expenses, housing loan interest, housing rent, eldercare.",
            ]),
            ("Individual Income Tax - Specific Incomes", [
                "Business income: 5-35% progressive rates (5 brackets).",
                "Interest/dividends/stock gains: 20% flat rate.",
                "Rental income: 20% (after 20% expense deduction for property costs).",
                "Property transfer: 20% on gain (sale price minus original cost minus deductions).",
                "Temporary income (prizes, lottery): 20% flat rate.",
            ]),
            ("Corporate Income Tax (Enterprise Income Tax - EIT)", [
                "Standard EIT rate: 25%.",
                "High-Tech Enterprise (HTE) preferential rate: 15%.",
                "Small Low-Profit Enterprise: 20% on taxable income up to ¥3 million.",
                "Western Region Development incentive: 15% in designated areas.",
                "Advanced Technology Service Enterprises: 15%.",
                "Encouraged industries in China-ASEAN Free Trade zones: 15%.",
            ]),
            ("VAT (Value Added Tax)", [
                "Standard VAT rate: 13% (goods, most services).",
                "Reduced rate: 9% (agricultural products, utilities, real estate, transportation).",
                "6% rate: Financial services, modern services, postal services, consumer services.",
                "0%: Exports, cross-border services.",
                "Small-scale taxpayers: 3% (simplified collection; suspended to 1% until end 2027).",
                "VAT invoice system (fapiao) is mandatory in China for all business transactions.",
            ]),
            ("Land & Property Tax", [
                "Land Use Tax (Chengzhen Tudi Shiyong Shui): Annual tax on land use rights.",
                "- Annual rate: ¥0.6 - ¥30 per square meter (varies by city tier).",
                "- Beijing/Shanghai tier 1 cities: Up to ¥30/sqm.",
                "Land Appreciation Tax (LAT): Tax on real estate transfers.",
                "- 30%: Appreciation rate 0-50%",
                "- 40%: Appreciation rate 50-100%",
                "- 50%: Appreciation rate 100-200%",
                "- 60%: Appreciation rate over 200%",
                "Property Tax for Enterprises: 1.2% of original value (deduct 10-30%) or 12% of rental income.",
                "Property Tax Reform: China piloting residential property tax in Shanghai and Chongqing.",
                "Shanghai Pilot: 0.6-1.2% of taxable value (for second homes); many exemptions.",
                "Stamp Tax on property transactions: 0.05% to 3%.",
            ]),
            ("Deduction Limits", [
                "Basic Monthly Deduction (IIT): ¥5,000 per month.",
                "Special Additional Deductions (Annual caps):",
                "- Child Education: ¥2,000 per month per child (¥24,000/year)",
                "- Continued Education: ¥400/month during certificate study period (max ¥4,800/year)",
                "- Major Medical: Out-of-pocket medical expenses 5,000-90,000 per year at 80%",
                "- Housing Loan Interest: ¥1,000/month (¥12,000/year) for first home mortgage",
                "- Housing Rent: ¥1,500/month (direct cities); ¥1,100/month (others); ¥800/month (under 100k)",
                "- Eldercare: ¥3,000/month (only child); ¥1,500/month (with siblings)",
                "Individual Annual Deduction Limit: ¥20,000 (specific investment-related deductions).",
            ]),
            ("Non-Resident Tax Policies", [
                "Non-residents (stay in China <183 days/year): Taxed only on China-source income.",
                "No days in China: Only taxed on income paid by/through Chinese entities.",
                "China-source employment income: Full Chinese IIT applies.",
                "Withholding tax on dividends: 10% (reduced by treaty).",
                "Withholding tax on interest: 10% (reduced by treaty to 5-7% with key partners).",
                "Withholding tax on royalties: 10% (reduced by treaty).",
                "China has 115+ double taxation agreements.",
                "Non-resident enterprises: 10% withholding on passive income from China (EIT).",
            ]),
            ("Industry-Specific Tax Rules", [
                "Software Companies: 10% EIT rate (qualified); VAT refund on portion above 3%.",
                "Integrated Circuit (semiconductor) manufacturers: 0-10% EIT for 5-10 years.",
                "Free Trade Zones (FTZ): 15% EIT in Hainan Free Trade Port.",
                "Hainan FTP: 0% personal income tax for qualified high-income talent.",
                "Agriculture: Exempt from EIT; special VAT rules.",
                "Finance/Banking: 6% VAT on financial services income.",
                "Real Estate Development: LAT pre-levy of 2-4%; complex EIT treatment for presales.",
            ]),
            ("Tax Filing Deadlines", [
                "Individual IIT (Annual Reconciliation): March 1 - June 30 of following year.",
                "Monthly/quarterly IIT withholding by employers: 15th of following month.",
                "Enterprise Income Tax (EIT) annual return: May 31.",
                "EIT quarterly prepayment: 15th of following month after quarter end.",
                "VAT returns: Monthly or quarterly; due on the 15th of the following period.",
                "Land Appreciation Tax: Pre-levy at time of property sales; annual settlement.",
            ]),
        ]
    },
}

def styles():
    s = getSampleStyleSheet()
    title_style = ParagraphStyle('T', parent=s['Heading1'], fontSize=18, spaceAfter=12, textColor=colors.HexColor("#1a237e"))
    section_style = ParagraphStyle('H', parent=s['Heading2'], fontSize=13, spaceAfter=8, textColor=colors.HexColor("#1565c0"), spaceBefore=14)
    body_style = ParagraphStyle('B', parent=s['Normal'], fontSize=10, spaceAfter=4, leading=15)
    return title_style, section_style, body_style

def create_pdf(folder_name, data):
    folder = os.path.join(BASE, folder_name)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{folder_name}_Tax_Comprehensive.pdf")
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
    title_s, section_s, body_s = styles()
    flow = [Paragraph(data["title"], title_s), HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a237e")), Spacer(1, 10)]
    
    universal_calc_section = ("General Tax Calculation Formula & Principles", [
        "If a user asks a generic question like 'what is the amount tax I want to payable' or 'how much tax do I pay':",
        "1. Determine their tax residency status and applicable country tax brackets.",
        "2. Calculate Gross Income from all sources.",
        "3. Subtract any standard allowances (like the US Standard Deduction, UK Personal Allowance, or Indian Standard Deduction) to find the Taxable Income.",
        "4. Apply the progressive income tax brackets/slabs step-by-step to the Taxable Income.",
        "5. Add any mandatory surcharges, cesses, or state/provincial taxes.",
        "6. Subtract any eligible tax credits or rebates to determine the final Net Tax Payable.",
        "If exact income is NOT provided by the user, explicitly list the above steps and provide the country's tax slabs so they can calculate it themselves."
    ])
    
    for section_title, lines in data["sections"] + [universal_calc_section]:
        flow.append(Paragraph(section_title, section_s))
        for line in lines:
            flow.append(Paragraph(line, body_s))
        flow.append(Spacer(1, 6))
    doc.build(flow)
    print(f"✅ Generated: {path}")

if __name__ == "__main__":
    print("📄 Generating comprehensive tax PDFs...")
    for country_code, data in COUNTRIES.items():
        create_pdf(data["folder"], data)
    print("🎉 All PDFs generated successfully!")
