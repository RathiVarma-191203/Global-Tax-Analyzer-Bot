"""
Generates highly detailed tax PDFs covering all commonly queried sections,
deductions, rates, and policies. Designed to eliminate "data not found" responses.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "PDF")

def get_styles():
    s = getSampleStyleSheet()
    title = ParagraphStyle('T', parent=s['Heading1'], fontSize=17, spaceAfter=10, textColor=colors.HexColor("#1a237e"))
    h2 = ParagraphStyle('H2', parent=s['Heading2'], fontSize=13, spaceAfter=6, textColor=colors.HexColor("#1565c0"), spaceBefore=12)
    h3 = ParagraphStyle('H3', parent=s['Heading3'], fontSize=11, spaceAfter=4, textColor=colors.HexColor("#0277bd"), spaceBefore=8)
    body = ParagraphStyle('B', parent=s['Normal'], fontSize=9.5, spaceAfter=3, leading=14)
    return title, h2, h3, body

def build_pdf(path, title_text, sections):
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=1.8*cm, rightMargin=1.8*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)
    title_s, h2_s, h3_s, body_s = get_styles()
    flow = [
        Paragraph(title_text, title_s),
        HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a237e")),
        Spacer(1, 8)
    ]
    for item in sections:
        if item[0] == 'h2':
            flow.append(Paragraph(item[1], h2_s))
        elif item[0] == 'h3':
            flow.append(Paragraph(item[1], h3_s))
        elif item[0] == 'p':
            flow.append(Paragraph(item[1], body_s))
        elif item[0] == 'sp':
            flow.append(Spacer(1, item[1]))
    doc.build(flow)
    print(f"✅  {path}")

# ─────────────────────────────────────────────────────────────────────────────
# INDIA – Sections & Deductions (dedicated file)
# ─────────────────────────────────────────────────────────────────────────────
INDIA_DEDUCTIONS = [
    ('h2', 'Chapter VI-A Deductions: Overview'),
    ('p', 'Chapter VI-A of the Income Tax Act 1961 provides various deductions from Gross Total Income (GTI). These deductions reduce the taxable income, thereby reducing the tax liability. Deductions are only available under the OLD tax regime; the new regime (Section 115BAC) does not allow most Chapter VI-A deductions.'),
    
    ('h2', 'Section 80C – Most Popular Deduction (Limit: ₹1,50,000)'),
    ('p', 'Section 80C allows a total deduction of up to ₹1,50,000 (₹1.5 lakh) per financial year.'),
    ('p', 'Eligible investments and expenses under Section 80C:'),
    ('p', '1. Employee Provident Fund (EPF) – mandatory contribution by salaried employees'),
    ('p', '2. Public Provident Fund (PPF) – minimum ₹500, maximum ₹1,50,000 per year; 15-year lock-in'),
    ('p', '3. ELSS (Equity Linked Savings Scheme) Mutual Funds – 3-year lock-in; best returns among 80C options'),
    ('p', '4. Life Insurance Premium (LIC or any insurer) – for self, spouse, children'),
    ('p', '5. National Savings Certificate (NSC) – 5-year fixed income instrument by Post Office'),
    ('p', '6. 5-Year Tax-Saving Fixed Deposit (FD) – with scheduled banks or post offices'),
    ('p', '7. Sukanya Samriddhi Yojana (SSY) – for girl child; tax-free interest'),
    ('p', '8. Senior Citizens Savings Scheme (SCSS) – for individuals 60+'),
    ('p', '9. Principal repayment of Home Loan – under Section 80C'),
    ('p', '10. Tuition Fees – for up to 2 children (full-time education in India)'),
    ('p', '11. Stamp Duty and Registration charges for house property'),
    ('p', '12. NABARD Rural Bonds – notified bonds issued by NABARD'),
    ('p', 'Note: Sections 80CCC (pension plan), 80CCD(1) (NPS) are part of the aggregate ₹1.5 lakh limit under 80CCE. The total of 80C + 80CCC + 80CCD(1) cannot exceed ₹1,50,000.'),
    
    ('h2', 'Section 80CCD – National Pension System (NPS) Deductions'),
    ('h3', 'Section 80CCD(1) – Employee / Self-employed NPS Contribution'),
    ('p', 'Deduction up to 10% of salary (Basic + DA) for salaried; 20% of gross income for self-employed. Subject to ₹1.5 lakh overall 80CCE cap.'),
    ('h3', 'Section 80CCD(1B) – Additional NPS Contribution (Extra ₹50,000)'),
    ('p', 'An ADDITIONAL deduction of up to ₹50,000 over and above the ₹1.5 lakh limit under Section 80CCE. This brings total potential deduction to ₹2,00,000 using 80C + 80CCD(1B).'),
    ('h3', 'Section 80CCD(2) – Employer NPS Contribution'),
    ('p', 'Employer contribution to NPS is deductible: up to 10% of salary for private sector; 14% for central government employees. No monetary cap. This is not subject to 80CCE limit.'),
    
    ('h2', 'Section 80D – Health Insurance Premium Deduction'),
    ('p', 'Deduction for health insurance premiums and preventive health check-up expenses:'),
    ('p', '• Self, spouse, dependent children: ₹25,000 per year (₹50,000 if any insured person is a senior citizen 60+)'),
    ('p', '• Parents (non-senior citizen): additional ₹25,000'),
    ('p', '• Parents (senior citizen 60+): additional ₹50,000'),
    ('p', '• Maximum combined 80D deduction: ₹1,00,000 (if both self-family and parents are senior citizens)'),
    ('p', '• Preventive Health Check-up: ₹5,000 (within the overall 80D limit); cash payments allowed'),
    ('p', '• Section 80D also covers contributions to Central Government Health Scheme (CGHS)'),
    
    ('h2', 'Section 80DD – Deduction for Disabled Dependent'),
    ('p', '• Flat deduction of ₹75,000 for a dependent with disability (40–80% disability)'),
    ('p', '• ₹1,25,000 for severe disability (80%+ disability)'),
    ('p', 'No requirement to show actual expenditure; flat deduction applies.'),
    
    ('h2', 'Section 80DDB – Deduction for Treatment of Specified Diseases'),
    ('p', '• For specified serious disease treatment (like cancer, neurological disease, AIDS, kidney failure, thalassaemia, haematological disorders)'),
    ('p', '• Limit: ₹40,000 (below 60 years); ₹1,00,000 (senior citizens 60+ years)'),
    ('p', '• Actual expenditure up to the limit; must get certificate from specialist doctor in government hospital'),
    
    ('h2', 'Section 80E – Deduction on Education Loan Interest'),
    ('p', '• Deduction on INTEREST paid on education loan taken for higher education of self, spouse, children, or student for whom you are legal guardian'),
    ('p', '• NO upper limit on the amount of interest that can be deducted'),
    ('p', '• Deduction available for 8 consecutive years starting from the year repayment begins, or until interest is fully paid (whichever is earlier)'),
    ('p', '• The loan must be taken from a financial institution or approved charitable institution'),
    ('p', '• Only interest qualifies; principal repayment is NOT deductible under 80E'),
    
    ('h2', 'Section 80EE – Interest on Home Loan for First-Time Buyers'),
    ('p', '• Additional ₹50,000 deduction on home loan interest (over Section 24(b) ₹2 lakh limit)'),
    ('p', '• Conditions: Loan sanctioned between 1 April 2016 and 31 March 2017; property value ≤ ₹50 lakh; loan ≤ ₹35 lakh; no other residential property at time of sanction'),
    
    ('h2', 'Section 80EEA – Additional Interest Deduction for Affordable Housing (Current)'),
    ('p', '• Additional ₹1,50,000 deduction on home loan interest (over Section 24(b))'),
    ('p', '• Conditions: Loan sanctioned between 1 April 2019 and 31 March 2022; stamp duty value of property ≤ ₹45 lakh; first-time buyer (no other residential property)'),
    ('p', '• Combined 80EEA + Section 24(b) max interest deduction = ₹3,50,000'),

    ('h2', 'Section 80G – Deductions for Donations'),
    ('p', 'Donations to specified funds and charitable institutions are deductible:'),
    ('p', '100% deduction WITHOUT any qualifying limit:'),
    ('p', '• PM National Relief Fund, PM CARES Fund, National Defence Fund, PM Citizen Assistance Fund, Chief Minister National Relief Fund'),
    ('p', '• National Foundation for Communal Harmony, Zila Saksharta Samiti'),
    ('p', '50% deduction WITHOUT any qualifying limit:'),
    ('p', '• Jawaharlal Nehru Memorial Fund, Indira Gandhi Memorial Trust, Rajiv Gandhi Foundation'),
    ('p', '100% deduction WITH qualifying limit (10% of Adjusted GTI):'),
    ('p', '• Donations to government or local authority for family planning; donations to Indian Olympic Association'),
    ('p', '50% deduction WITH qualifying limit (10% of Adjusted GTI):'),
    ('p', '• Donations to any fund/institute covered under Section 80G'),
    ('p', 'Cash donations above ₹2,000 are NOT eligible from FY 2017-18 onwards. Must be via cheque, bank transfer, or digital mode.'),
    
    ('h2', 'Section 80GG – Deduction for Rent Paid (No HRA)'),
    ('p', '• For individuals NOT receiving HRA from employer (self-employed or those without HRA component)'),
    ('p', '• Deduction = Minimum of:'),
    ('p', '  (a) ₹5,000 per month (₹60,000 per year)'),
    ('p', '  (b) 25% of total income'),
    ('p', '  (c) Actual rent paid minus 10% of total income'),
    ('p', '• Cannot own any residential property in India (self or spouse or minor child)'),
    
    ('h2', 'Section 80TTA – Interest on Savings Account'),
    ('p', '• Deduction of up to ₹10,000 on interest earned from savings bank account (individuals and HUFs, not senior citizens)'),
    ('p', '• Applies to savings accounts in banks, co-operative banks, or post offices'),
    ('p', '• Does NOT apply to fixed deposit, recurring deposit, or other time deposits'),
    
    ('h2', 'Section 80TTB – Interest Income for Senior Citizens'),
    ('p', '• For senior citizens (60+): deduction up to ₹50,000 on interest from ALL deposits (savings, FD, RD) in banks, co-operative societies, and post offices'),
    ('p', '• Replaces Section 80TTA for senior citizens (cannot claim both)'),
    
    ('h2', 'Section 80U – Deduction for Disabled Individual'),
    ('p', '• For SELF being a person with disability (40–80%): flat ₹75,000 deduction'),
    ('p', '• For SELF being a person with severe disability (80%+): flat ₹1,25,000 deduction'),
    ('p', '• Must furnish certificate from medical authority. Differs from 80DD (80DD is for disabled dependents; 80U is for self)'),
    
    ('h2', 'Section 24(b) – Home Loan Interest Deduction'),
    ('p', '• Deduction for interest payable on home loan for self-occupied property: up to ₹2,00,000 per year'),
    ('p', '• For let-out property: full interest deductible (no cap) but set-off against other income limited to ₹2 lakh per year; remaining carried forward 8 years'),
    ('p', '• Pre-construction interest can be claimed in 5 equal instalments starting from year of possession'),
    
    ('h2', 'Section 87A – Tax Rebate'),
    ('p', '• New Tax Regime: Full income tax rebate (zero tax) if total income does not exceed ₹7,00,000'),
    ('p', '• Old Tax Regime: Rebate of up to ₹12,500 if total income does not exceed ₹5,00,000'),
    ('p', '• Rebate is deducted from tax payable before adding cess (4% Health and Education cess)'),
    
    ('h2', 'Section 10 – Exemptions from Income (Key Items)'),
    ('p', '• Section 10(10D): Life Insurance maturity proceeds – fully exempt (some conditions apply: premium ≤ 10% of sum assured or sum assured < ₹5 lakh for policies issued after 1.4.2023)'),
    ('p', '• Section 10(11): Statutory PF (EPF) – interest and maturity exempt (interest exempt up to ₹2.5 lakh contribution per year from FY 2021-22)'),
    ('p', '• Section 10(14): Special allowances like HRA, LTA, conveyance, uniform, children education allowance (₹100/month per child up to 2 children), hostel allowance (₹300/month per child)'),
    ('p', '• Section 10(26): Income of Scheduled Tribe members in specified areas – fully exempt'),
    ('p', '• Section 10(38): LTCG on equity shares – NOW TAXABLE under Section 112A; exemption removed from FY 2018-19'),
    
    ('h2', 'Standard Deduction for Salaried Employees'),
    ('p', '• Old Tax Regime: ₹50,000 standard deduction from salary income'),
    ('p', '• New Tax Regime (from FY 2024-25): ₹75,000 standard deduction (increased in Budget 2024)'),
    ('p', '• No bills or proof required; automatic deduction from salary/pension'),
    
    ('h2', 'HRA Exemption – Section 10(13A)'),
    ('p', 'House Rent Allowance is exempt to the extent of the MINIMUM of:'),
    ('p', '(a) Actual HRA received from employer'),
    ('p', '(b) Rent paid – 10% of (Basic + DA)'),
    ('p', '(c) 50% of (Basic + DA) for metro cities (Mumbai, Delhi, Chennai, Kolkata); 40% for non-metros'),
    ('p', 'Receipts required if rent exceeds ₹1,00,000 per year (PAN of landlord mandatory if rent > ₹1 lakh/year).'),
    
    ('h2', 'LTA – Leave Travel Allowance Section 10(5)'),
    ('p', '• Exempt for travel within India (shortest route) for self and family'),
    ('p', '• Claimed TWICE in a block of 4 calendar years (current block: 2022-2025)'),
    ('p', '• Only transport cost exempt (not hotel/food); air travel allowed only if destination connected by air'),
    ('p', '• Must actually travel; if not claimed, can be carried forward to next block (once)'),
]

# ─────────────────────────────────────────────────────────────────────────────
# INDIA – Capital Gains (dedicated file)
# ─────────────────────────────────────────────────────────────────────────────
INDIA_CAPITAL_GAINS = [
    ('h2', 'Capital Gains Tax in India – Comprehensive Guide (Budget 2024)'),
    ('p', 'Capital gains arise on transfer (sale/exchange/gift) of a capital asset. The tax treatment depends on the holding period (Short-term vs Long-term) and the type of asset.'),
    
    ('h2', 'Classification: Short-Term vs Long-Term'),
    ('p', '36 months holding = Long-term (general rule for most assets)'),
    ('p', '24 months = Long-term for: immovable property (land/building), unlisted shares, unlisted securities'),
    ('p', '12 months = Long-term for: listed equity shares, equity mutual funds, REITs, InvITs (STT paid)'),
    
    ('h2', 'STCG – Short-Term Capital Gains Tax Rates (After Budget 2024)'),
    ('p', '• Listed equity shares / equity mutual funds (STT paid): 20% (increased from 15% in Budget 2024, effective 23 July 2024)'),
    ('p', '• Debt mutual funds: Taxed as per individual income slab rate'),
    ('p', '• Other short-term capital gains: Taxed as per income slab rate'),
    
    ('h2', 'LTCG – Long-Term Capital Gains Tax Rates (After Budget 2024)'),
    ('p', '• Listed equity shares / equity mutual funds (STT paid): 12.5% (increased from 10% in Budget 2024) – threshold exemption of ₹1,25,000 per year (raised from ₹1 lakh)'),
    ('p', '• Immovable property (land/building): 12.5% WITHOUT indexation (indexation benefit removed in Budget 2024) OR 20% WITH indexation if purchased before 23 July 2024 (grandfathering provision)'),
    ('p', '• Unlisted shares (resident): 12.5% without indexation'),
    ('p', '• Debt mutual funds: As per slab rate (indexation removed from April 2023)'),
    ('p', '• Gold / Physical assets: 12.5% (holding 36+ months)'),
    
    ('h2', 'Exemptions on Capital Gains'),
    ('p', 'Section 54 – LTCG on sale of residential house:'),
    ('p', '  Invest in ONE new residential property in India within 1 year before / 2 years after sale, OR construct within 3 years. Exemption = lower of CG or cost of new house. Max exemption ₹10 crore (capped from FY 2023-24).'),
    ('p', 'Section 54EC – Invest in NHAI/RECL/PFC/REC bonds within 6 months of sale:'),
    ('p', '  Exemption up to ₹50 lakh; bonds have 5-year lock-in.'),
    ('p', 'Section 54F – LTCG on sale of any capital asset (not residential):'),
    ('p', '  Invest full SALE CONSIDERATION (not just gain) in one new residential property. Must not own more than one other house. Proportional exemption if partial investment.'),
    ('p', 'Section 54B – LTCG on agricultural land transferred and new agri-land purchased within 2 years.'),
    
    ('h2', 'Capital Gains on Property Sale – Practical Notes'),
    ('p', '• TDS at 1% of sale value if property value exceeds ₹50 lakh (buyer deducts)'),
    ('p', '• NRI sellers: TDS at 30% of gains (STCG) or 12.5% (LTCG); CA certificate under Sec 195 needed for variation'),
    ('p', '• Cost of Improvement and cost of acquisition are deductible from sale consideration'),
    ('p', '• Stamp duty value used as deemed consideration if higher than actual sale price (Section 50C)'),
]

# ─────────────────────────────────────────────────────────────────────────────
# INDIA – GST Comprehensive
# ─────────────────────────────────────────────────────────────────────────────
INDIA_GST = [
    ('h2', 'GST – Goods and Services Tax (India) Comprehensive Guide'),
    ('p', 'GST was introduced on 1 July 2017, replacing multiple state and central taxes under a single unified framework. It is a multi-stage, destination-based tax.'),
    
    ('h2', 'GST Rate Slabs'),
    ('h3', '0% (Nil) – GST Free Items'),
    ('p', 'Fresh vegetables, fresh fruits, rice (non-branded), wheat, salt, eggs, milk (non-packaged), curd, fresh fish/meat, bread, books, newspapers, educational services, healthcare services, agricultural equipment'),
    ('h3', '5% GST Rate'),
    ('p', 'Packaged food items, branded cereals, coffee, tea (not branded), sugar, edible oils, domestic LPG cylinders, footwear up to ₹1000, apparel up to ₹1000, rail transport (economy), life-saving drugs'),
    ('h3', '12% GST Rate'),
    ('p', 'Processed food, butter, cheese, ghee, agarbatti, mobile phones, non-AC hotels, business class air travel, frozen meat, fruit/vegetable juices, umbrellas, sewing machines, playing cards'),
    ('h3', '18% GST Rate'),
    ('p', 'Most services, computers, laptops, cameras, monitors, refrigerators, washing machines, paints, varnishes, shampoo, soap, toothpaste, ice cream, pasta, cornflakes, telecom services, banking services, insurance, restaurant services (AC), IT/software services'),
    ('h3', '28% GST Rate'),
    ('p', 'Aerated drinks (+ 12% compensation cess), tobacco, cigarettes (+ specific rate cess), pan masala, luxury cars, motorcycles above 350cc, aircraft for recreation, casinos/betting, five-star hotels'),
    ('h3', 'Special / Unique Rates'),
    ('p', '0.25% – Cut and semi-polished diamonds, rough precious stones'),
    ('p', '3% – Gold, silver, platinum jewellery and articles thereof'),
    ('p', '1.5% – Job work services for cutting and polishing of diamonds'),
    
    ('h2', 'GST Registration Thresholds'),
    ('p', '• General states: Mandatory if annual turnover exceeds ₹40 lakh (goods) or ₹20 lakh (services)'),
    ('p', '• Special category states (NE, hill states): ₹20 lakh (goods), ₹10 lakh (services)'),
    ('p', '• Composition scheme threshold: ₹1.5 crore (goods); ₹50 lakh (services); 1-6% flat tax'),
    ('p', '• Mandatory registration irrespective of turnover: inter-state supply, e-commerce, casual taxable person, non-resident taxable person, reverse charge mechanism transactions'),
    
    ('h2', 'GST Returns (Filing Calendar)'),
    ('p', '• GSTR-1 (Outward supplies): Monthly (11th of next month) or Quarterly (IFF / QRMP scheme)'),
    ('p', '• GSTR-3B (Summary + tax payment): Monthly or Quarterly; due 20th of next month'),
    ('p', '• GSTR-9 (Annual return): December 31 of following FY'),
    ('p', '• GSTR-2B (Auto-drafted ITC statement): Available 14th of each month'),
    
    ('h2', 'Input Tax Credit (ITC)'),
    ('p', '• Businesses can claim credit for GST paid on purchases (inputs) against GST payable on sales'),
    ('p', '• Conditions: Tax invoice required; goods/services actually received; tax paid by supplier; GSTR-3B filed; matches GSTR-2B'),
    ('p', '• Blocked credits (Section 17(5)): Motor vehicles (except for specified purposes), food and beverages, club membership, works contract for immovable property'),
    ('p', '• ITC reversal required if payment to supplier not made within 180 days'),
    
    ('h2', 'GST on Real Estate'),
    ('p', '• Under-construction residential flats: 5% (no ITC) for general; 1% for affordable housing (stamp duty value ≤ ₹45 lakh + area ≤ 60/90 sqmt)'),
    ('p', '• Ready-to-move or completed flats (with OC): 0% GST'),
    ('p', '• Commercial property under construction: 12%'),
    ('p', '• Transfer of development rights (TDR): 18%'),
    
    ('h2', 'Reverse Charge Mechanism (RCM)'),
    ('p', 'Under RCM, the recipient of goods/services is liable to pay GST instead of the supplier. Key examples:'),
    ('p', '• Legal services by advocate to business'),
    ('p', '• Services by director to company'),
    ('p', '• Import of services'),
    ('p', '• Goods from unregistered dealer (under certain conditions)'),
    ('p', '• Sponsorship services; Security services; Renting of motor vehicles'),
]

# ─────────────────────────────────────────────────────────────────────────────
# INDIA – TDS and TCS
# ─────────────────────────────────────────────────────────────────────────────
INDIA_TDS = [
    ('h2', 'TDS (Tax Deducted at Source) – Complete Rate Chart 2024-25'),
    ('p', 'TDS is deducted by the payer at the time of making specified payments. It is an advance collection of tax.'),
    
    ('h2', 'Key TDS Sections and Rates'),
    ('h3', 'Section 192 – Salary'),
    ('p', '• TDS deducted based on applicable income tax slab of the employee. No threshold if salary is taxable.'),
    ('h3', 'Section 193 – Interest on Securities'),
    ('p', '• Rate: 10%. Threshold: ₹5,000 (debentures, securities)'),
    ('h3', 'Section 194 – Dividend'),
    ('p', '• Rate: 10%. Threshold: ₹5,000 per year'),
    ('h3', 'Section 194A – Interest other than interest on securities'),
    ('p', '• Rate: 10%. Threshold: ₹40,000/year (₹50,000 for senior citizens) for banks/co-op societies/post offices; ₹5,000 for others'),
    ('h3', 'Section 194B – Winnings from Lottery/Crossword'),
    ('p', '• Rate: 30%. Threshold: ₹10,000 per prize. No deduction allowed.'),
    ('h3', 'Section 194C – Payment to Contractors/Sub-contractors'),
    ('p', '• Rate: 1% (individuals/HUF), 2% (others). Threshold: ₹30,000 per contract or ₹1,00,000 aggregate in FY'),
    ('h3', 'Section 194D – Insurance Commission'),
    ('p', '• Rate: 5%. Threshold: ₹15,000 per year'),
    ('h3', 'Section 194H – Commission/Brokerage'),
    ('p', '• Rate: 5%. Threshold: ₹15,000 per year. (Reduced to 2% from FY 2024-25 in Budget 2024)'),
    ('h3', 'Section 194I – Rent'),
    ('p', '• Rate: 10% (land/building/furniture/fittings), 2% (plant/machinery/equipment). Threshold: ₹2,40,000 per year'),
    ('h3', 'Section 194IA – TDS on Purchase of Property'),
    ('p', '• Rate: 1% of sale consideration. Threshold: Property value above ₹50 lakh. Buyer deducts and deposits.'),
    ('h3', 'Section 194J – Professional/Technical Services'),
    ('p', '• Rate: 10% (professional), 2% (technical services/royalties). Threshold: ₹30,000 per year'),
    ('h3', 'Section 194N – Cash Withdrawal from Bank'),
    ('p', '• Rate: 2% on cash withdrawal above ₹1 crore in FY (0% if ITR filed; 5% if no ITR filed for 3 years and withdrawal > ₹20 lakh)'),
    ('h3', 'Section 194O – TDS by E-Commerce Operator'),
    ('p', '• Rate: 1%. On gross amount of sales/services facilitated through e-commerce platform. Threshold: ₹5 lakh (for individual/HUF with PAN)'),
    ('h3', 'Section 194Q – TDS on Purchase of Goods (Buyer)'),
    ('p', '• Rate: 0.1%. Applies when buyer purchases goods worth ₹50 lakh+ in FY and buyer has turnover >₹10 crore in previous FY'),
    
    ('h2', 'TDS – Lower Deduction / Nil Deduction Certificate'),
    ('p', '• Form 13 application to AO for certificate allowing lower/nil TDS if income is below taxable limit or exempt'),
    ('p', '• Form 15G/15H: Self-declaration to bank for nil TDS on interest. Form 15G for individuals below 60; Form 15H for senior citizens'),
    
    ('h2', 'TDS Returns Filing'),
    ('p', '• Form 24Q: TDS on salaries (quarterly: 31 July, 31 Oct, 31 Jan, 31 May)'),
    ('p', '• Form 26Q: TDS on non-salary payments (same due dates)'),
    ('p', '• Form 27Q: TDS on payments to NRIs (same due dates)'),
    ('p', '• Form 26QB: TDS on property purchase (within 30 days from end of month of deduction)'),
    ('p', '• TDS certificate: Form 16 (salary), Form 16A (non-salary), Form 16B (property)'),
    
    ('h2', 'TCS – Tax Collected at Source'),
    ('h3', 'Section 206C – Key TCS Provisions'),
    ('p', '• Timber, tendu leaves, scrap, minerals: 1-2.5% by seller'),
    ('p', '• Motor vehicle sale above ₹10 lakh: 1%'),
    ('p', '• Overseas tour packages: 5% (20% if PAN not provided; threshold ₹7 lakh per year)'),
    ('p', '• Liberalised Remittance Scheme (LRS): 20% TCS on remittance above ₹7 lakh per year (for education loan: 0.5%; for education otherwise: 5%)'),
    ('p', '• Foreign credit/debit card transactions abroad: Exempt if < ₹7 lakh; 20% above ₹7 lakh (from July 2023)'),
]

# ─────────────────────────────────────────────────────────────────────────────
# INDIA – Business Income, Start-ups, Special Provisions
# ─────────────────────────────────────────────────────────────────────────────
INDIA_BUSINESS = [
    ('h2', 'Business Taxation – Presumptive Taxation'),
    ('h3', 'Section 44AD – Small Business (Turnover below ₹3 crore for FY 2024-25)'),
    ('p', '• Deemed profit: 8% of total turnover/gross receipts (6% if receipts via banking/digital mode)'),
    ('p', '• No need to maintain books or get audit if this scheme is used'),
    ('p', '• Cannot claim any deductions under Sections 30-38 if 44AD opted'),
    ('p', '• Not applicable to commission agents, professionals, or agency business'),
    ('h3', 'Section 44ADA – Presumptive Taxation for Professionals (Turnover below ₹75 lakh)'),
    ('p', '• Deemed profit: 50% of gross receipts for specified professionals (doctor, lawyer, CA, engineer, architect, journalist, technically qualified consultant, IT professional)'),
    ('h3', 'Section 44AE – Transport Business (owning up to 10 vehicles)'),
    ('p', '• ₹7,500 per month per heavy vehicle; ₹4,500 per month per light vehicle as deemed income'),
    
    ('h2', 'Start-up Tax Incentives'),
    ('p', '• Section 80-IAC: 100% profit deduction for 3 consecutive years out of 10 years from incorporation (for DPIIT-recognized startups incorporated between 1 April 2016 and 31 March 2025; turnover < ₹100 crore)'),
    ('p', '• Angel Tax exemption (Section 56(2)(viib)): Removed for resident investors from FY 2024-25; still applies to foreign investors (but DPIIT recognized startups can seek exemption)'),
    ('p', '• ESOPs taxed at point of sale (not at allotment) for qualifying startups'),
    ('p', '• Tax credit for MAT/AMT for startups'),
    
    ('h2', 'Alternate Minimum Tax (AMT) – For Individuals/LLPs'),
    ('p', '• Applies if regular income tax < 18.5% of Adjusted Total Income (ATI)'),
    ('p', '• AMT credit carried forward for 15 years'),
    
    ('h2', 'Audit Requirement – Section 44AB'),
    ('p', '• Mandatory tax audit if:'),
    ('p', '  (a) Business turnover exceeds ₹1 crore (OR ₹10 crore if 95%+ cash receipts/payments)'),
    ('p', '  (b) Professional receipts exceed ₹50 lakh'),
    ('p', '  (c) Presumptive scheme opted and declared profit lower than presumptive profit'),
    ('p', 'Audit report in Form 3CA/3CB and 3CD by a Chartered Accountant.'),
    
    ('h2', 'MAT – Minimum Alternate Tax (For Companies)'),
    ('p', '• Applicable if regular corporate tax < 15% of Book Profit'),
    ('p', '• MAT Rate: 15% of Book Profit + surcharge + cess'),
    ('p', '• Book Profit = Net Profit + adjustments (add-back depreciation, income tax, deferred tax, provisions, capital gains, etc.)'),
    ('p', '• MAT credit can be carried forward for 15 years'),
    ('p', '• Companies under Section 115BAA/115BAB (new regimes) are EXEMPT from MAT'),
    
    ('h2', 'Depreciation under Income Tax (Section 32)'),
    ('p', 'Rates for common assets:'),
    ('p', '• Buildings (residential): 5%; Commercial: 10%'),
    ('p', '• Plant & Machinery (general): 15%'),
    ('p', '• Computers and software: 40%'),
    ('p', '• Motor cars: 15% (30% for taxis)'),
    ('p', '• Furniture and fittings: 10%'),
    ('p', '• Intangible assets (patents, copyrights, knowhow): 25%'),
    ('p', '• Additional depreciation: 20% extra in first year for new plant/machinery (manufacturing; 35% in backward areas)'),
    ('p', '• WDV method used (not SLM except for power generation companies)'),
]

# ─────────────────────────────────────────────────────────────────────────────
# AUSTRALIA – Detailed deductions, land tax, negative gearing
# ─────────────────────────────────────────────────────────────────────────────
AUSTRALIA_DETAILED = [
    ('h2', 'Australia Detailed Tax Guide 2024-25 – Deductions, Property & Specific Rules'),
    
    ('h2', 'Work-Related Deductions (Schedule)'),
    ('p', '• Work-related expenses must relate directly to earning income; you must have incurred the expense yourself and not been reimbursed'),
    ('p', '• Under $300 total: claim without receipts (ATO spot check may occur)'),
    ('p', '• Over $300: all claims need receipts or other written evidence'),
    ('h3', 'Car & Travel Expenses'),
    ('p', 'Cents per km method: 85 cents/km (2024-25); maximum 5,000 km per vehicle without detailed log. No receipts required but must show work basis.'),
    ('p', 'Logbook method: Deduct business percentage of all car costs (fuel, insurance, registration, depreciation). 12-week logbook period required.'),
    ('h3', 'Home Office Expenses'),
    ('p', '• Fixed rate method: 67 cents per hour for all home office costs. Must keep a work diary/records.'),
    ('p', '• Actual cost method: Claim actual portion of rent/mortgage interest, utilities, phone, internet, depreciation of furniture used for work.'),
    ('h3', 'Self-Education Expenses'),
    ('p', '• Deductible if: upskilling for current job; maintaining current income stream; professional development required by employer'),
    ('p', '• Not deductible if: training for a new career; getting first employment'),
    ('p', '• Eligible: course fees, textbooks, stationery, depreciation of computer/desk if used for study'),
    ('h3', 'Tools, Equipment, Uniforms'),
    ('p', '• Tools and equipment under $300: immediate full deduction'),
    ('p', '• Over $300: depreciate over effective life'),
    ('p', '• Protective clothing (e.g., steel-cap boots, safety glasses, hi-vis): fully deductible'),
    ('p', '• Occupation-specific clothing (nurse uniform, chef\'s hat): deductible'),
    ('p', '• Conventional clothing (suit, business attire): NOT deductible even if required for work'),
    
    ('h2', 'Rental Property Deductions (Negative Gearing)'),
    ('p', '• Negative gearing = when property expenses exceed rental income; the loss is deductible against other income (salary, business income)'),
    ('p', 'Deductible rental property expenses:'),
    ('p', '• Loan interest on investment property loan (the largest deduction for most investors)'),
    ('p', '• Council rates, water rates, land tax'),
    ('p', '• Property agent management fees (typically 5-10% of rent)'),
    ('p', '• Insurance premiums (building, landlord insurance)'),
    ('p', '• Repairs and maintenance (but NOT capital improvements – those are depreciated)'),
    ('p', '• Depreciation of building structure (Division 43 – Capital works): 2.5% per year for buildings constructed after 15 September 1987'),
    ('p', '• Depreciation of fixtures/fittings (Division 40 – Assets): Claim on washers, ovens, hot water systems, carpets etc.'),
    ('p', '• Borrowing expenses (amortised over loan term or 5 years, whichever less)'),
    ('p', '• Stationery, phone calls relating to property management'),
    
    ('h2', 'Stage 3 Tax Cuts (Effective 1 July 2024)'),
    ('p', '• The Stage 3 reforms reduced the 19% tax rate bracket ceiling from $45,000 to $45,000 (unchanged)'),
    ('p', '• 32.5% tax rate now applies from $45,001 to $135,000 (old: $45,001 to $120,000)'),
    ('p', '• 37% bracket: $135,001 to $190,000 (new; old rate cut removed entirely)'),
    ('p', '• 45% rate: Over $190,000'),
    ('p', '• The 37% rate was reinstated at $135,001 (the original plan to abolish it was reversed)'),
    ('p', '• Low Income Tax Offset (LITO): Up to $700 for income under $37,500; phases out by $66,667'),
    ('p', '• Low and Middle Income Tax Offset (LMITO): Discontinued from FY 2022-23'),
    
    ('h2', 'Superannuation Tax Rules'),
    ('p', '• Concessional contributions (employer SG + salary sacrifice + personal deductible): 15% contributions tax; cap $27,500/year ($30,000 from FY 2024-25)'),
    ('p', '• Non-concessional contributions (after-tax): 0% contributions tax; cap $110,000/year ($120,000 from FY 2024-25). Bring-forward rule: 3× annual cap in 1 year if balance < $1.9M'),
    ('p', '• Superannuation Guarantee (SG) rate from employers: 11% (FY 2024-25); rising to 11.5% from 1 July 2025; 12% from 1 July 2025 (legislated)'),
    ('p', '• Fund earnings: 15% tax rate (0% for pension phase assets under $1.9M Transfer Balance Cap)'),
    ('p', '• Withdrawals after age 60 from taxed funds: Tax-FREE'),
    ('p', '• Division 293 tax: Additional 15% on concessional contributions for income >$250,000'),
    
    ('h2', 'State Land Taxes – Current Rates 2024-25'),
    ('p', 'NSW: 1.6% for value $1,075,001 to $6,571,000; 2.0% above $6,571,000; 0.02% special trust surcharge'),
    ('p', 'VIC: Progressive 0.2%-2.55%; 0% below $300,000; surcharge 2% for foreign owners'),
    ('p', 'QLD: 1.0% above $600,000; 1.5% above $1,000,000; 2% above $3,000,000 for individuals'),
    ('p', 'SA: 0.5% (>$723,000) up to 2.4% (>$1.35M); abolished for primary production'),
    ('p', 'WA: 0.6%-2.67% on unimproved land value above $300,000'),
    ('p', 'ACT: 0.74% – 2.25% varying by land value; land tax reform underway'),
    ('p', 'TAS: 0.55% up to 1.5% on unimproved value; 0% below $25,000'),
    
    ('h2', 'CGT Discount and Specific Events'),
    ('p', '• 50% CGT discount for individuals holding assets 12+ months'),
    ('p', '• 33.33% for complying super funds; 0% for companies (no discount)'),
    ('p', '• Main Residence Exemption: Full CGT exemption if property was your main home throughout ownership; partial exemption if rented at any stage'),
    ('p', '• Small Business CGT concessions (turnover <$2 million or net assets <$6M):'),
    ('p', '  15-year exemption (if owned 15+ years, age 55+): 100% exempt'),
    ('p', '  50% Active Asset Reduction: Reduces gain by 50%'),
    ('p', '  Retirement exemption: Up to $500,000 lifetime limit'),
    ('p', '  Rollover: Defer gain by purchasing replacement asset within 2 years'),
]

DOCUMENTS = {
    "INDIA": [
        ("INDIA_Deductions_80C_80D_80E_Comprehensive.pdf", "India – Complete Income Tax Deductions Guide (FY 2024-25)", INDIA_DEDUCTIONS),
        ("INDIA_Capital_Gains_Tax_Guide.pdf", "India – Capital Gains Tax Complete Guide (Budget 2024)", INDIA_CAPITAL_GAINS),
        ("INDIA_GST_Comprehensive.pdf", "India – GST Complete Guide: Rates, Compliance, ITC (2024)", INDIA_GST),
        ("INDIA_TDS_TCS_Comprehensive.pdf", "India – TDS & TCS Complete Rate Chart and Compliance (2024-25)", INDIA_TDS),
        ("INDIA_Business_Startup_Tax.pdf", "India – Business Tax, Presumptive Taxation, Startups, MAT (2024-25)", INDIA_BUSINESS),
    ],
    "AUSTRALIA": [
        ("AUSTRALIA_Detailed_Deductions_Super_CGT.pdf", "Australia – Detailed Tax: Deductions, Super, CGT, Land Tax (2024-25)", AUSTRALIA_DETAILED),
    ],
}

if __name__ == "__main__":
    print("📄 Generating supplemental comprehensive tax PDFs...")
    for country, docs in DOCUMENTS.items():
        folder = os.path.join(BASE, country)
        os.makedirs(folder, exist_ok=True)
        for filename, title, sections in docs:
            path = os.path.join(folder, filename)
            build_pdf(path, title, sections)
    print("🎉 All supplemental PDFs generated successfully!")
