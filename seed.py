"""
Seed script – populates the InternAI database with realistic demo data.
Safe to re-run: existing rows (matched by email / unique field) are skipped.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from app import app, db
from app import (
    User, StudentProfile, StudentPortfolio, StudentCertificate,
    StudentInternshipExperience, Organization, Internship, Application
)
from werkzeug.security import generate_password_hash
from datetime import date, datetime

def seed():
    with app.app_context():
        db.create_all()

        # ── 1. ORGANIZATIONS ────────────────────────────────────────────────
        # ── PARTNER COMPANIES (from approved/verified PDF list) ─────────────
        partner_orgs_data = [
            # ── IT & Technology ──────────────────────────────────────────────────
            dict(email='careers@tcs.com',         password='admin123', name='Tata Consultancy Services',
                 company='Tata Consultancy Services Limited', gst='27AAACT2727Q1ZW', domain='tcs.com',
                 linkedin='https://linkedin.com/company/tata-consultancy-services', industry='IT Services',
                 location='Mumbai', desc='Global IT services, consulting, and business solutions company.'),
            dict(email='hr@infosys.com',           password='admin123', name='Infosys',
                 company='Infosys Limited', gst='29AAACI1372J1ZY', domain='infosys.com',
                 linkedin='https://linkedin.com/company/infosys', industry='IT Services',
                 location='Bengaluru', desc='Leading global technology services and consulting company.'),
            dict(email='jobs@wipro.com',           password='admin123', name='Wipro',
                 company='Wipro Limited', gst='29AAACW0305L1ZB', domain='wipro.com',
                 linkedin='https://linkedin.com/company/wipro', industry='IT Services',
                 location='Bengaluru', desc='Global IT, consulting and business process services company.'),
            dict(email='recruit@hcltech.com',      password='admin123', name='HCL Technologies',
                 company='HCL Technologies Limited', gst='09AAACC3713J2ZH', domain='hcltech.com',
                 linkedin='https://linkedin.com/company/hcl-technologies', industry='IT Services',
                 location='Noida', desc='Global technology company providing IT services and products.'),
            dict(email='hr@techmahindra.com',      password='admin123', name='Tech Mahindra',
                 company='Tech Mahindra Limited', gst='27AABCT6098K1Z7', domain='techmahindra.com',
                 linkedin='https://linkedin.com/company/tech-mahindra', industry='IT Services',
                 location='Pune', desc='Digital transformation, consulting and IT services company.'),
            dict(email='jobs@cognizant.com',       password='admin123', name='Cognizant',
                 company='Cognizant Technology Solutions India', gst='33AABCC9414P1ZQ', domain='cognizant.com',
                 linkedin='https://linkedin.com/company/cognizant', industry='IT Services',
                 location='Chennai', desc='Multinational IT services and consulting corporation.'),
            dict(email='hr@ltimindtree.com',       password='admin123', name='LTIMindtree',
                 company='LTIMindtree Limited', gst='27AAACL3082F1ZW', domain='ltimindtree.com',
                 linkedin='https://linkedin.com/company/ltimindtree', industry='IT Services',
                 location='Mumbai', desc='Technology consulting and digital solutions company.'),
            dict(email='recruit@zoho.com',         password='admin123', name='Zoho Corporation',
                 company='Zoho Corporation Pvt Ltd', gst='33AABCZ1234K1ZP', domain='zoho.com',
                 linkedin='https://linkedin.com/company/zoho', industry='SaaS / Software',
                 location='Chennai', desc='Cloud software suite and SaaS application development company.'),
            dict(email='careers@mphasis.com',      password='admin123', name='Mphasis',
                 company='Mphasis Limited', gst='29AAAMC1234H1ZT', domain='mphasis.com',
                 linkedin='https://linkedin.com/company/mphasis', industry='IT Services',
                 location='Bengaluru', desc='IT solutions company specializing in cloud and cognitive services.'),
            dict(email='hr@persistent.com',        password='admin123', name='Persistent Systems',
                 company='Persistent Systems Limited', gst='27AABCP2341M1ZN', domain='persistent.com',
                 linkedin='https://linkedin.com/company/persistent-systems', industry='IT Services',
                 location='Pune', desc='Technology services firm focused on software engineering and digital transformation.'),
            dict(email='careers@cyient.com',       password='admin123', name='Cyient',
                 company='Cyient Limited', gst='36AABCC4567D1ZR', domain='cyient.com',
                 linkedin='https://linkedin.com/company/cyient', industry='Engineering IT',
                 location='Hyderabad', desc='Engineering and technology solutions company for global industries.'),
            dict(email='jobs@capgemini.com',       password='admin123', name='Capgemini India',
                 company='Capgemini Technology Services India', gst='27AABCC8899F1ZM', domain='capgemini.com',
                 linkedin='https://linkedin.com/company/capgemini', industry='IT Services',
                 location='Mumbai', desc='Consulting, technology, and digital transformation services.'),
            dict(email='hr@accenture.com',         password='admin123', name='Accenture India',
                 company='Accenture Solutions Pvt Ltd', gst='29AAAAA1234B1ZT', domain='accenture.com',
                 linkedin='https://linkedin.com/company/accenture', industry='IT Consulting',
                 location='Bengaluru', desc='Global professional services company in IT and consulting.'),
            dict(email='recruit@ibm.com',          password='admin123', name='IBM India',
                 company='IBM India Pvt Ltd', gst='29AAACI4321G1ZS', domain='ibm.com',
                 linkedin='https://linkedin.com/company/ibm', industry='IT Services',
                 location='Bengaluru', desc='Multinational technology corporation offering cloud, AI, and consulting.'),
            dict(email='careers@oracle.com',       password='admin123', name='Oracle India',
                 company='Oracle India Pvt Ltd', gst='29AAACO8765H1ZL', domain='oracle.com',
                 linkedin='https://linkedin.com/company/oracle', industry='Enterprise Software',
                 location='Bengaluru', desc='Global enterprise software and cloud solutions provider.'),
            dict(email='hr@microsoft.com',         password='admin123', name='Microsoft India',
                 company='Microsoft Corporation India Pvt Ltd', gst='29AAACM3456J1ZK', domain='microsoft.com',
                 linkedin='https://linkedin.com/company/microsoft', industry='Software / Cloud',
                 location='Hyderabad', desc='Global leader in software, cloud services, and AI.'),
            dict(email='recruit@adobe.com',        password='admin123', name='Adobe India',
                 company='Adobe Systems India Pvt Ltd', gst='29AAACA5678K1ZJ', domain='adobe.com',
                 linkedin='https://linkedin.com/company/adobe', industry='Software / Creative',
                 location='Bengaluru', desc='Creative, marketing, and document management solutions company.'),
            dict(email='careers@intel.com',        password='admin123', name='Intel India',
                 company='Intel Technology India Pvt Ltd', gst='29AAACI9012L1ZI', domain='intel.com',
                 linkedin='https://linkedin.com/company/intel', industry='Semiconductors',
                 location='Bengaluru', desc='Global semiconductor and computing technology company.'),
            dict(email='hr@dell.com',              password='admin123', name='Dell India',
                 company='Dell International Services India Pvt Ltd', gst='29AAACD3456M1ZH', domain='dell.com',
                 linkedin='https://linkedin.com/company/dell-technologies', industry='Hardware / IT',
                 location='Bengaluru', desc='Multinational technology company selling computers and IT solutions.'),
            dict(email='careers@google.com',       password='admin123', name='Google India',
                 company='Google India Pvt Ltd', gst='29AAACG7890N1ZG', domain='google.com',
                 linkedin='https://linkedin.com/company/google', industry='Internet / AI',
                 location='Hyderabad', desc='Global technology company specializing in search, cloud, and AI.'),
            dict(email='hr@samsung.com',           password='admin123', name='Samsung India',
                 company='Samsung India Electronics Pvt Ltd', gst='07AAACS1234P1ZF', domain='samsung.com',
                 linkedin='https://linkedin.com/company/samsung', industry='Electronics',
                 location='Delhi', desc='Multinational electronics and semiconductor manufacturing company.'),
            dict(email='recruit@ericsson.com',     password='admin123', name='Ericsson India',
                 company='Ericsson India Global Services Pvt Ltd', gst='29AAACE5678Q1ZE', domain='ericsson.com',
                 linkedin='https://linkedin.com/company/ericsson', industry='Telecom Technology',
                 location='Bengaluru', desc='Global leader in telecom equipment and managed services.'),
            dict(email='careers@nokia.com',        password='admin123', name='Nokia India',
                 company='Nokia Solutions and Networks India Pvt Ltd', gst='29AAACN9012R1ZD', domain='nokia.com',
                 linkedin='https://linkedin.com/company/nokia', industry='Telecom Technology',
                 location='Bengaluru', desc='Multinational telecommunications, information technology and consumer electronics company.'),
            dict(email='hr@genpact.com',           password='admin123', name='Genpact India',
                 company='Genpact India Pvt Ltd', gst='29AAACG3456S1ZC', domain='genpact.com',
                 linkedin='https://linkedin.com/company/genpact', industry='BPO / IT Services',
                 location='Hyderabad', desc='Global professional services firm delivering digital-led innovation and solutions.'),
            dict(email='recruit@wns.com',          password='admin123', name='WNS Global Services',
                 company='WNS Global Services Pvt Ltd', gst='27AAACW7890T1ZB', domain='wns.com',
                 linkedin='https://linkedin.com/company/wns-global-services', industry='BPO',
                 location='Mumbai', desc='Business process management company delivering digital-led analytics solutions.'),
            dict(email='careers@dxc.com',          password='admin123', name='DXC Technology India',
                 company='DXC Technology India Pvt Ltd', gst='29AAACD1234U1ZA', domain='dxc.com',
                 linkedin='https://linkedin.com/company/dxc-technology', industry='IT Services',
                 location='Bengaluru', desc='Global IT services company helping businesses run mission-critical systems.'),
            dict(email='hr@infosysbpm.com',        password='admin123', name='Infosys BPM',
                 company='Infosys BPM Limited', gst='29AAACI5678V1ZZ', domain='infosysbpm.com',
                 linkedin='https://linkedin.com/company/infosys-bpm', industry='BPO',
                 location='Bengaluru', desc='Business process outsourcing subsidiary of Infosys.'),
            dict(email='recruit@ofss.co.in',       password='admin123', name='Oracle Financial Services',
                 company='Oracle Financial Services Software Limited', gst='27AAACO9012W1ZY', domain='ofss.co.in',
                 linkedin='https://linkedin.com/company/oracle-financial-services', industry='Fintech / IT',
                 location='Mumbai', desc='IT solutions provider to the financial services industry.'),
            dict(email='careers@edgeverve.com',    password='admin123', name='EdgeVerve Systems',
                 company='EdgeVerve Systems Limited', gst='29AAACE3456X1ZX', domain='edgeverve.com',
                 linkedin='https://linkedin.com/company/edgeverve', industry='IT Products',
                 location='Bengaluru', desc='Product subsidiary of Infosys providing enterprise software products.'),
            dict(email='hr@sterlitetech.com',      password='admin123', name='Sterlite Technologies',
                 company='Sterlite Technologies Limited', gst='27AAACS7890Y1ZW', domain='sterlitetech.com',
                 linkedin='https://linkedin.com/company/sterlite-technologies', industry='Telecom / IT',
                 location='Pune', desc='Global data network solutions company building smarter networks.'),
            dict(email='careers@vmware.com',       password='admin123', name='VMware India',
                 company='VMware Software India Pvt Ltd', gst='29AAACV1234Z1ZV', domain='vmware.com',
                 linkedin='https://linkedin.com/company/vmware', industry='Cloud / Software',
                 location='Bengaluru', desc='Cloud computing and virtualization technology company.'),
            dict(email='hr@huawei.com',            password='admin123', name='Huawei India',
                 company='Huawei Telecommunications India Co Pvt Ltd', gst='29AAACH5678A2ZU', domain='huawei.com',
                 linkedin='https://linkedin.com/company/huawei', industry='Telecom Technology',
                 location='Gurugram', desc='Global provider of ICT infrastructure and smart devices.'),
            dict(email='recruit@ltts.com',         password='admin123', name='L&T Technology Services',
                 company='L&T Technology Services Limited', gst='27AAACL9012B2ZT', domain='ltts.com',
                 linkedin='https://linkedin.com/company/larsen-toubro-technology-services', industry='Engineering IT',
                 location='Mumbai', desc='Engineering research and development services company.'),

            # ── Banking & Financial Services ─────────────────────────────────────
            dict(email='careers@hdfcbank.com',     password='admin123', name='HDFC Bank',
                 company='HDFC Bank Limited', gst='27AAACH2702H1ZN', domain='hdfcbank.com',
                 linkedin='https://linkedin.com/company/hdfc-bank', industry='Banking',
                 location='Mumbai', desc='India\'s largest private sector bank offering retail and corporate banking.'),
            dict(email='hr@icicibank.com',         password='admin123', name='ICICI Bank',
                 company='ICICI Bank Limited', gst='27AAACI3678K1ZM', domain='icicibank.com',
                 linkedin='https://linkedin.com/company/icici-bank', industry='Banking',
                 location='Mumbai', desc='Leading private sector bank in India with pan-India presence.'),
            dict(email='recruit@axisbank.com',     password='admin123', name='Axis Bank',
                 company='Axis Bank Limited', gst='27AAACA4789L1ZL', domain='axisbank.com',
                 linkedin='https://linkedin.com/company/axis-bank', industry='Banking',
                 location='Mumbai', desc='Third largest private sector bank in India.'),
            dict(email='careers@kotak.com',        password='admin123', name='Kotak Mahindra Bank',
                 company='Kotak Mahindra Bank Limited', gst='27AAACK5890M1ZK', domain='kotak.com',
                 linkedin='https://linkedin.com/company/kotak-mahindra-bank', industry='Banking',
                 location='Mumbai', desc='Private sector bank offering financial services across segments.'),
            dict(email='hr@indusind.com',          password='admin123', name='IndusInd Bank',
                 company='IndusInd Bank Limited', gst='27AAACI6901N1ZJ', domain='indusind.com',
                 linkedin='https://linkedin.com/company/indusind-bank', industry='Banking',
                 location='Mumbai', desc='New generation private sector bank with retail and corporate banking.'),
            dict(email='recruit@bandhanbank.com',  password='admin123', name='Bandhan Bank',
                 company='Bandhan Bank Limited', gst='19AAACB7012O1ZI', domain='bandhanbank.com',
                 linkedin='https://linkedin.com/company/bandhan-bank', industry='Banking',
                 location='Kolkata', desc='Commercial bank focusing on financial inclusion and microfinance.'),
            dict(email='careers@federalbank.co.in',password='admin123', name='Federal Bank',
                 company='Federal Bank Limited', gst='32AAACF8123P1ZH', domain='federalbank.co.in',
                 linkedin='https://linkedin.com/company/the-federal-bank', industry='Banking',
                 location='Kochi', desc='Private sector commercial bank based in Kerala.'),
            dict(email='hr@rblbank.com',           password='admin123', name='RBL Bank',
                 company='RBL Bank Limited', gst='27AAACR9234Q1ZG', domain='rblbank.com',
                 linkedin='https://linkedin.com/company/rbl-bank', industry='Banking',
                 location='Mumbai', desc='Fast-growing private sector bank offering diversified financial services.'),
            dict(email='recruit@idfcfirstbank.com',password='admin123', name='IDFC First Bank',
                 company='IDFC First Bank Limited', gst='27AAACI0345R1ZF', domain='idfcfirstbank.com',
                 linkedin='https://linkedin.com/company/idfcfirstbank', industry='Banking',
                 location='Mumbai', desc='Diversified financial institution offering banking and financial services.'),
            dict(email='careers@aubank.in',        password='admin123', name='AU Small Finance Bank',
                 company='AU Small Finance Bank Limited', gst='08AAACA1456S1ZE', domain='aubank.in',
                 linkedin='https://linkedin.com/company/au-small-finance-bank', industry='Banking',
                 location='Jaipur', desc='Small finance bank headquartered in Rajasthan offering retail banking.'),
            dict(email='hr@equitasbank.com',       password='admin123', name='Equitas Small Finance Bank',
                 company='Equitas Small Finance Bank Limited', gst='33AAACE2567T1ZD', domain='equitasbank.com',
                 linkedin='https://linkedin.com/company/equitas-small-finance-bank', industry='Banking',
                 location='Chennai', desc='Small finance bank providing inclusive financial services.'),
            dict(email='recruit@bajajfinance.in',  password='admin123', name='Bajaj Finance',
                 company='Bajaj Finance Limited', gst='27AAACB3678U1ZC', domain='bajajfinance.in',
                 linkedin='https://linkedin.com/company/bajaj-finance', industry='NBFC',
                 location='Pune', desc='Leading non-banking financial company with diversified lending.'),
            dict(email='careers@shriramfinance.in',password='admin123', name='Shriram Finance',
                 company='Shriram Finance Limited', gst='33AAACS4789V1ZB', domain='shriramfinance.in',
                 linkedin='https://linkedin.com/company/shriram-finance', industry='NBFC',
                 location='Chennai', desc='Financial services company focused on commercial vehicle financing.'),
            dict(email='hr@muthootfinance.com',    password='admin123', name='Muthoot Finance',
                 company='Muthoot Finance Limited', gst='32AAACM5890W1ZA', domain='muthootfinance.com',
                 linkedin='https://linkedin.com/company/muthoot-finance', industry='NBFC / Gold Loans',
                 location='Kochi', desc='Largest gold financing company in India.'),
            dict(email='recruit@hdbfs.com',        password='admin123', name='HDB Financial Services',
                 company='HDB Financial Services Limited', gst='27AAACH6901X1ZZ', domain='hdbfs.com',
                 linkedin='https://linkedin.com/company/hdb-financial-services', industry='NBFC',
                 location='Mumbai', desc='Non-banking financial company and subsidiary of HDFC Bank.'),
            dict(email='careers@iifl.com',         password='admin123', name='IIFL Finance',
                 company='IIFL Finance Limited', gst='27AAACI7012Y1ZY', domain='iifl.com',
                 linkedin='https://linkedin.com/company/iifl-finance', industry='NBFC',
                 location='Mumbai', desc='Diversified financial services company offering loans and investments.'),
            dict(email='hr@tatacapital.com',       password='admin123', name='Tata Capital',
                 company='Tata Capital Financial Services Limited', gst='27AAACT8123Z1ZX', domain='tatacapital.com',
                 linkedin='https://linkedin.com/company/tata-capital', industry='NBFC',
                 location='Mumbai', desc='Financial services arm of the Tata Group offering loans and wealth management.'),
            dict(email='recruit@mahindrafinance.com', password='admin123', name='Mahindra Finance',
                 company='Mahindra & Mahindra Financial Services Limited', gst='27AAACM9234A2ZW', domain='mahindrafinance.com',
                 linkedin='https://linkedin.com/company/mahindra-finance', industry='NBFC',
                 location='Mumbai', desc='NBFC providing financial services to rural and semi-urban India.'),
            dict(email='careers@bajajhousing.com', password='admin123', name='Bajaj Housing Finance',
                 company='Bajaj Housing Finance Limited', gst='27AAACB0345B2ZV', domain='bajajhousing.com',
                 linkedin='https://linkedin.com/company/bajaj-housing-finance', industry='Housing Finance',
                 location='Pune', desc='Housing finance company providing home loans and property solutions.'),
            dict(email='hr@lichousing.com',        password='admin123', name='LIC Housing Finance',
                 company='LIC Housing Finance Limited', gst='27AAACL1456C2ZU', domain='lichousing.com',
                 linkedin='https://linkedin.com/company/lic-housing-finance', industry='Housing Finance',
                 location='Mumbai', desc='Largest housing finance company in India under the LIC umbrella.'),
            dict(email='recruit@hdfclife.com',     password='admin123', name='HDFC Life',
                 company='HDFC Life Insurance Company Limited', gst='27AAACH2567D2ZT', domain='hdfclife.com',
                 linkedin='https://linkedin.com/company/hdfc-life', industry='Insurance',
                 location='Mumbai', desc='Leading long-term life insurance solutions provider.'),
            dict(email='careers@iciciprulife.com', password='admin123', name='ICICI Prudential Life',
                 company='ICICI Prudential Life Insurance Co Ltd', gst='27AAACI3678E2ZS', domain='iciciprulife.com',
                 linkedin='https://linkedin.com/company/icici-prudential-life-insurance', industry='Insurance',
                 location='Mumbai', desc='Joint venture life insurance company between ICICI Bank and Prudential.'),
            dict(email='hr@icicilombard.com',      password='admin123', name='ICICI Lombard',
                 company='ICICI Lombard General Insurance Co Ltd', gst='27AAACI4789F2ZR', domain='icicilombard.com',
                 linkedin='https://linkedin.com/company/icici-lombard', industry='Insurance',
                 location='Mumbai', desc='Leading private sector general insurance company in India.'),
            dict(email='recruit@bajajallianz.com', password='admin123', name='Bajaj Allianz General Insurance',
                 company='Bajaj Allianz General Insurance Co Ltd', gst='27AAACB5890G2ZQ', domain='bajajallianz.com',
                 linkedin='https://linkedin.com/company/bajaj-allianz-general-insurance', industry='Insurance',
                 location='Pune', desc='General insurance joint venture between Bajaj Finserv and Allianz SE.'),
            dict(email='careers@maxlifeinsurance.com', password='admin123', name='Max Life Insurance',
                 company='Max Life Insurance Company Limited', gst='07AAACM6901H2ZP', domain='maxlifeinsurance.com',
                 linkedin='https://linkedin.com/company/max-life-insurance', industry='Insurance',
                 location='Delhi', desc='Joint venture life insurance company between Max Financial Services and Mitsui Sumitomo.'),
            dict(email='hr@sbigeneral.in',         password='admin123', name='SBI General Insurance',
                 company='SBI General Insurance Company Limited', gst='27AAACS7012I2ZO', domain='sbigeneral.in',
                 linkedin='https://linkedin.com/company/sbi-general-insurance', industry='Insurance',
                 location='Mumbai', desc='General insurance company promoted by State Bank of India.'),
            dict(email='recruit@hdfcergo.com',     password='admin123', name='HDFC Ergo',
                 company='HDFC Ergo General Insurance Co Ltd', gst='27AAACH8123J2ZN', domain='hdfcergo.com',
                 linkedin='https://linkedin.com/company/hdfc-ergo', industry='Insurance',
                 location='Mumbai', desc='Joint venture general insurance company of HDFC Bank and ERGO Group.'),
            dict(email='careers@hdfcfund.com',     password='admin123', name='HDFC AMC',
                 company='HDFC Asset Management Company Limited', gst='27AAACH9234K2ZM', domain='hdfcfund.com',
                 linkedin='https://linkedin.com/company/hdfc-amc', industry='Asset Management',
                 location='Mumbai', desc='One of India\'s largest mutual fund companies.'),
            dict(email='hr@sbicard.com',           password='admin123', name='SBI Cards',
                 company='SBI Cards and Payment Services Limited', gst='27AAACS0345L2ZL', domain='sbicard.com',
                 linkedin='https://linkedin.com/company/sbi-cards', industry='Fintech / Payments',
                 location='Gurugram', desc='Second largest credit card issuer in India promoted by SBI.'),
            dict(email='recruit@nseindia.com',     password='admin123', name='NSE India',
                 company='National Stock Exchange of India Limited', gst='27AAACN1456M2ZK', domain='nseindia.com',
                 linkedin='https://linkedin.com/company/national-stock-exchange-of-india', industry='Capital Markets',
                 location='Mumbai', desc='India\'s largest financial market infrastructure.'),
            dict(email='careers@npci.org.in',      password='admin123', name='NPCI',
                 company='National Payments Corporation of India', gst='27AAACN2567N2ZJ', domain='npci.org.in',
                 linkedin='https://linkedin.com/company/npci-national-payments-corporation-of-india', industry='Payments',
                 location='Mumbai', desc='Umbrella organisation for retail payments and settlement systems in India.'),
            dict(email='hr@zerodha.com',           password='admin123', name='Zerodha',
                 company='Zerodha Broking Limited', gst='29AAACZ3678O2ZI', domain='zerodha.com',
                 linkedin='https://linkedin.com/company/zerodha', industry='Fintech / Broking',
                 location='Bengaluru', desc='India\'s largest retail stockbroker by active clients.'),
            dict(email='careers@barclays.com',     password='admin123', name='Barclays India',
                 company='Barclays Bank India', gst='27AAACB4789P2ZH', domain='barclays.com',
                 linkedin='https://linkedin.com/company/barclays', industry='Banking',
                 location='Mumbai', desc='British multinational investment bank and financial services company.'),
            dict(email='hr@citi.com',              password='admin123', name='Citicorp India',
                 company='Citicorp Finance India Limited', gst='27AAACF5890Q2ZG', domain='citi.com',
                 linkedin='https://linkedin.com/company/citi', industry='Banking',
                 location='Mumbai', desc='Global bank offering consumer, corporate, and investment banking.'),
            dict(email='recruit@sc.com',           password='admin123', name='Standard Chartered India',
                 company='Standard Chartered Bank India', gst='27AAACS6901R2ZF', domain='sc.com',
                 linkedin='https://linkedin.com/company/standard-chartered', industry='Banking',
                 location='Mumbai', desc='International banking group operating across Asia, Africa, and the Middle East.'),
            dict(email='careers@jpmorgan.com',     password='admin123', name='J.P. Morgan India',
                 company='J.P. Morgan Services India Pvt Ltd', gst='27AAACJ7012S2ZE', domain='jpmorgan.com',
                 linkedin='https://linkedin.com/company/jpmorgan-chase', industry='Investment Banking',
                 location='Mumbai', desc='Global financial services firm offering investment banking and asset management.'),
            dict(email='hr@aexp.com',              password='admin123', name='American Express India',
                 company='American Express Banking Corp India', gst='07AAACA8123T2ZD', domain='aexp.com',
                 linkedin='https://linkedin.com/company/american-express', industry='Financial Services',
                 location='Delhi', desc='Global financial services company known for charge and credit cards.'),
            dict(email='recruit@franklintempletonindia.com', password='admin123', name='Franklin Templeton India',
                 company='Franklin Templeton Asset Management India', gst='27AAACF9234U2ZC', domain='franklintempletonindia.com',
                 linkedin='https://linkedin.com/company/franklin-templeton', industry='Asset Management',
                 location='Mumbai', desc='Global investment management firm offering mutual funds and financial products.'),
            dict(email='careers@hdfcsec.com',      password='admin123', name='HDFC Securities',
                 company='HDFC Securities Limited', gst='27AAACH0345V2ZB', domain='hdfcsec.com',
                 linkedin='https://linkedin.com/company/hdfc-securities', industry='Broking',
                 location='Mumbai', desc='Equity and derivatives broking subsidiary of HDFC Bank.'),
            dict(email='hr@kotaksecurities.com',   password='admin123', name='Kotak Securities',
                 company='Kotak Securities Limited', gst='27AAACK1456W2ZA', domain='kotaksecurities.com',
                 linkedin='https://linkedin.com/company/kotak-securities', industry='Broking',
                 location='Mumbai', desc='Full-service stockbroker and subsidiary of Kotak Mahindra Bank.'),
            dict(email='recruit@icicisecurities.com', password='admin123', name='ICICI Securities',
                 company='ICICI Securities Limited', gst='27AAACI2567X2ZZ', domain='icicisecurities.com',
                 linkedin='https://linkedin.com/company/icici-securities', industry='Broking',
                 location='Mumbai', desc='Technology-based securities firm and subsidiary of ICICI Bank.'),
            dict(email='careers@cholamandalam.com',password='admin123', name='Cholamandalam Investment',
                 company='Cholamandalam Investment and Finance Co Ltd', gst='33AAACC3678Y2ZY', domain='cholamandalam.com',
                 linkedin='https://linkedin.com/company/cholamandalam-investment-and-finance', industry='NBFC',
                 location='Chennai', desc='Diversified financial services company offering vehicle and home loans.'),

            # ── Oil, Gas & Energy ────────────────────────────────────────────────
            dict(email='hr@ongc.co.in',            password='admin123', name='ONGC',
                 company='Oil and Natural Gas Corporation Limited', gst='05AAACO4789Z2ZX', domain='ongc.co.in',
                 linkedin='https://linkedin.com/company/ongc', industry='Oil & Gas',
                 location='Dehradun', desc='India\'s largest crude oil and natural gas company.'),
            dict(email='careers@iocl.com',         password='admin123', name='Indian Oil Corporation',
                 company='Indian Oil Corporation Limited', gst='07AAACI5890A3ZW', domain='iocl.com',
                 linkedin='https://linkedin.com/company/indian-oil-corporation', industry='Oil & Gas',
                 location='Delhi', desc='India\'s largest commercial enterprise in petroleum refining and pipelines.'),
            dict(email='hr@hindustanpetroleum.com',password='admin123', name='Hindustan Petroleum',
                 company='Hindustan Petroleum Corporation Limited', gst='27AAACH6901B3ZV', domain='hindustanpetroleum.com',
                 linkedin='https://linkedin.com/company/hpcl', industry='Oil & Gas',
                 location='Mumbai', desc='Major oil refining and downstream petroleum company in India.'),
            dict(email='recruit@bharatpetroleum.com', password='admin123', name='BPCL',
                 company='Bharat Petroleum Corporation Limited', gst='27AAACB7012C3ZU', domain='bharatpetroleum.com',
                 linkedin='https://linkedin.com/company/bharat-petroleum', industry='Oil & Gas',
                 location='Mumbai', desc='Government-owned oil and gas company engaged in refining and marketing.'),
            dict(email='careers@gail.co.in',       password='admin123', name='GAIL India',
                 company='GAIL (India) Limited', gst='07AAACG8123D3ZT', domain='gail.co.in',
                 linkedin='https://linkedin.com/company/gail-india', industry='Natural Gas',
                 location='Delhi', desc='India\'s principal natural gas processing and distribution company.'),
            dict(email='hr@oil-india.com',         password='admin123', name='Oil India',
                 company='Oil India Limited', gst='18AAACO9234E3ZS', domain='oil-india.com',
                 linkedin='https://linkedin.com/company/oil-india', industry='Oil & Gas',
                 location='Duliajan', desc='Premier national oil company engaged in exploration and production.'),
            dict(email='recruit@petronetlng.com',  password='admin123', name='Petronet LNG',
                 company='Petronet LNG Limited', gst='07AAACP0345F3ZR', domain='petronetlng.com',
                 linkedin='https://linkedin.com/company/petronet-lng', industry='Natural Gas',
                 location='Delhi', desc='India\'s largest LNG importing and re-gasification company.'),
            dict(email='careers@nayaraenergy.com', password='admin123', name='Nayara Energy',
                 company='Nayara Energy Limited', gst='24AAACN1456G3ZQ', domain='nayaraenergy.com',
                 linkedin='https://linkedin.com/company/nayara-energy', industry='Oil & Gas',
                 location='Vadodara', desc='Fully integrated Indian energy company with India\'s second-largest refinery.'),

            # ── Power & Utilities ────────────────────────────────────────────────
            dict(email='hr@ntpc.co.in',            password='admin123', name='NTPC',
                 company='NTPC Limited', gst='07AAACN2567H3ZP', domain='ntpc.co.in',
                 linkedin='https://linkedin.com/company/ntpc-ltd', industry='Power Generation',
                 location='Delhi', desc='India\'s largest power generation company.'),
            dict(email='careers@powergrid.in',     password='admin123', name='Power Grid Corporation',
                 company='Power Grid Corporation of India Limited', gst='07AAACP3678I3ZO', domain='powergrid.in',
                 linkedin='https://linkedin.com/company/power-grid-corporation-of-india', industry='Power Transmission',
                 location='Gurugram', desc='Central transmission utility owning and operating India\'s transmission network.'),
            dict(email='hr@recindia.nic.in',       password='admin123', name='REC Limited',
                 company='REC Limited', gst='07AAACR4789J3ZN', domain='recindia.nic.in',
                 linkedin='https://linkedin.com/company/rec-limited', industry='Power Finance',
                 location='Gurugram', desc='Non-banking financial company financing power sector projects.'),
            dict(email='recruit@pfcindia.com',     password='admin123', name='Power Finance Corporation',
                 company='Power Finance Corporation Limited', gst='07AAACP5890K3ZM', domain='pfcindia.com',
                 linkedin='https://linkedin.com/company/power-finance-corporation', industry='Power Finance',
                 location='Delhi', desc='Government financial institution dedicated to power sector funding.'),
            dict(email='careers@nhpcindia.com',    password='admin123', name='NHPC',
                 company='NHPC Limited', gst='07AAACN6901L3ZL', domain='nhpcindia.com',
                 linkedin='https://linkedin.com/company/nhpc-ltd', industry='Hydro Power',
                 location='Faridabad', desc='India\'s premier hydropower generation company.'),
            dict(email='hr@sjvn.nic.in',           password='admin123', name='SJVN',
                 company='SJVN Limited', gst='02AAACS7012M3ZK', domain='sjvn.nic.in',
                 linkedin='https://linkedin.com/company/sjvn-limited', industry='Power Generation',
                 location='Shimla', desc='Hydropower company operating thermal and renewable power projects.'),
            dict(email='recruit@nlcindia.in',      password='admin123', name='NLC India',
                 company='NLC India Limited', gst='33AAACN8123N3ZJ', domain='nlcindia.in',
                 linkedin='https://linkedin.com/company/nlc-india', industry='Power & Lignite',
                 location='Neyveli', desc='Navratna CPSE engaged in mining lignite and generating power.'),
            dict(email='careers@npcil.co.in',      password='admin123', name='NPCIL',
                 company='Nuclear Power Corporation of India Limited', gst='27AAACN9234O3ZI', domain='npcil.co.in',
                 linkedin='https://linkedin.com/company/nuclear-power-corporation-of-india', industry='Nuclear Power',
                 location='Mumbai', desc='Government-owned company developing and operating nuclear power reactors.'),
            dict(email='hr@adanipower.com',        password='admin123', name='Adani Power',
                 company='Adani Power Limited', gst='24AAACA0345P3ZH', domain='adanipower.com',
                 linkedin='https://linkedin.com/company/adani-power', industry='Power Generation',
                 location='Ahmedabad', desc='Largest private thermal power producer in India.'),
            dict(email='recruit@torrentpower.com', password='admin123', name='Torrent Power',
                 company='Torrent Power Limited', gst='24AAACT1456Q3ZG', domain='torrentpower.com',
                 linkedin='https://linkedin.com/company/torrent-power', industry='Power',
                 location='Ahmedabad', desc='Integrated utility company in power generation, transmission, and distribution.'),
            dict(email='careers@adanitotalgas.com',password='admin123', name='Adani Total Gas',
                 company='Adani Total Gas Limited', gst='24AAACA2567R3ZF', domain='adanitotalgas.com',
                 linkedin='https://linkedin.com/company/adani-total-gas', industry='City Gas Distribution',
                 location='Ahmedabad', desc='Joint venture between Adani and Total for city gas distribution.'),

            # ── Mining & Metals ──────────────────────────────────────────────────
            dict(email='hr@coalindia.in',          password='admin123', name='Coal India',
                 company='Coal India Limited', gst='20AAACC3678S3ZE', domain='coalindia.in',
                 linkedin='https://linkedin.com/company/coal-india-limited', industry='Mining',
                 location='Kolkata', desc='World\'s largest coal producer and state-owned company.'),
            dict(email='careers@ncl.co.in',        password='admin123', name='Northern Coalfields',
                 company='Northern Coalfields Limited', gst='23AAACN4789T3ZD', domain='ncl.co.in',
                 linkedin='https://linkedin.com/company/northern-coalfields-limited', industry='Mining',
                 location='Singrauli', desc='Subsidiary of Coal India operating opencast coal mines.'),
            dict(email='hr@mcl.gov.in',            password='admin123', name='Mahanadi Coalfields',
                 company='Mahanadi Coalfields Limited', gst='21AAACM5890U3ZC', domain='mcl.gov.in',
                 linkedin='https://linkedin.com/company/mahanadi-coalfields-limited', industry='Mining',
                 location='Sambalpur', desc='Coal mining subsidiary of Coal India in Odisha.'),
            dict(email='recruit@nmdc.co.in',       password='admin123', name='NMDC',
                 company='NMDC Limited', gst='36AAACN6901V3ZB', domain='nmdc.co.in',
                 linkedin='https://linkedin.com/company/nmdc-limited', industry='Mining',
                 location='Hyderabad', desc='India\'s largest iron ore producer and state-owned mining company.'),
            dict(email='careers@nalcoindia.com',   password='admin123', name='National Aluminium',
                 company='National Aluminium Company Limited', gst='21AAACN7012W3ZA', domain='nalcoindia.com',
                 linkedin='https://linkedin.com/company/nalco', industry='Aluminium',
                 location='Bhubaneswar', desc='Navratna PSU engaged in bauxite mining and aluminium production.'),
            dict(email='hr@tatasteel.com',         password='admin123', name='Tata Steel',
                 company='Tata Steel Limited', gst='20AAACT8123X3ZZ', domain='tatasteel.com',
                 linkedin='https://linkedin.com/company/tata-steel', industry='Steel',
                 location='Mumbai', desc='One of the world\'s top 10 steel producers.'),
            dict(email='recruit@jsw.in',           password='admin123', name='JSW Steel',
                 company='JSW Steel Limited', gst='27AAACJ9234Y3ZY', domain='jsw.in',
                 linkedin='https://linkedin.com/company/jsw-steel', industry='Steel',
                 location='Mumbai', desc='India\'s leading private sector steel company.'),
            dict(email='careers@sail.co.in',       password='admin123', name='SAIL',
                 company='Steel Authority of India Limited', gst='07AAACS0345Z3ZX', domain='sail.co.in',
                 linkedin='https://linkedin.com/company/sail-steel-authority-of-india', industry='Steel',
                 location='Delhi', desc='India\'s largest state-owned steel-making company.'),
            dict(email='hr@hindalco.com',          password='admin123', name='Hindalco',
                 company='Hindalco Industries Limited', gst='27AAACH1456A4ZW', domain='hindalco.com',
                 linkedin='https://linkedin.com/company/hindalco', industry='Aluminium / Copper',
                 location='Mumbai', desc='World\'s largest aluminium rolling and recycling company.'),
            dict(email='recruit@vedanta.com',      password='admin123', name='Vedanta',
                 company='Vedanta Limited', gst='27AAACV2567B4ZV', domain='vedanta.com',
                 linkedin='https://linkedin.com/company/vedanta-limited', industry='Mining / Metals',
                 location='Mumbai', desc='Global diversified natural resources company with operations in zinc, oil, and power.'),
            dict(email='careers@hindzinc.com',     password='admin123', name='Hindustan Zinc',
                 company='Hindustan Zinc Limited', gst='08AAACH3678C4ZU', domain='hindzinc.com',
                 linkedin='https://linkedin.com/company/hindustan-zinc', industry='Zinc',
                 location='Udaipur', desc='World\'s second largest and India\'s largest zinc-lead-silver producer.'),
            dict(email='hr@jindalsteelpower.com',  password='admin123', name='Jindal Steel & Power',
                 company='Jindal Steel & Power Limited', gst='22AAACJ4789D4ZT', domain='jindalsteelpower.com',
                 linkedin='https://linkedin.com/company/jindal-steel-and-power', industry='Steel / Power',
                 location='New Delhi', desc='Integrated steel and power company part of the O.P. Jindal Group.'),
            dict(email='recruit@am-nsindia.com',   password='admin123', name='ArcelorMittal Nippon Steel India',
                 company='ArcelorMittal Nippon Steel India Limited', gst='24AAACA5890E4ZS', domain='am-nsindia.com',
                 linkedin='https://linkedin.com/company/arcelormittal-nippon-steel-india', industry='Steel',
                 location='Surat', desc='India\'s first private sector steel company to produce flat-rolled products.'),
            dict(email='careers@bharatforge.com',  password='admin123', name='Bharat Forge',
                 company='Bharat Forge Limited', gst='27AAACB6901F4ZR', domain='bharatforge.com',
                 linkedin='https://linkedin.com/company/bharat-forge', industry='Auto Components / Forging',
                 location='Pune', desc='World\'s largest forging company supplying auto and non-auto sectors.'),

            # ── FMCG & Consumer ──────────────────────────────────────────────────
            dict(email='hr@hul.co.in',             password='admin123', name='Hindustan Unilever',
                 company='Hindustan Unilever Limited', gst='27AAACH7012G4ZQ', domain='hul.co.in',
                 linkedin='https://linkedin.com/company/hindustan-unilever', industry='FMCG',
                 location='Mumbai', desc='India\'s largest FMCG company with brands in food, beverages, and personal care.'),
            dict(email='recruit@itcportal.com',    password='admin123', name='ITC',
                 company='ITC Limited', gst='19AAACI8123H4ZP', domain='itcportal.com',
                 linkedin='https://linkedin.com/company/itc-limited', industry='FMCG / Hotels / Agri',
                 location='Kolkata', desc='Multi-business conglomerate with leadership in cigarettes, FMCG, hotels, and paper.'),
            dict(email='careers@britannia.co.in',  password='admin123', name='Britannia',
                 company='Britannia Industries Limited', gst='19AAACB9234I4ZO', domain='britannia.co.in',
                 linkedin='https://linkedin.com/company/britannia-industries', industry='FMCG / Food',
                 location='Kolkata', desc='India\'s largest food company with signature biscuit and dairy brands.'),
            dict(email='hr@dabur.com',             password='admin123', name='Dabur India',
                 company='Dabur India Limited', gst='07AAACD0345J4ZN', domain='dabur.com',
                 linkedin='https://linkedin.com/company/dabur', industry='FMCG / Ayurvedic',
                 location='Ghaziabad', desc='World\'s largest Ayurvedic and natural health care company.'),
            dict(email='recruit@godrejcp.com',     password='admin123', name='Godrej Consumer Products',
                 company='Godrej Consumer Products Limited', gst='27AAACG1456K4ZM', domain='godrejcp.com',
                 linkedin='https://linkedin.com/company/godrej-consumer-products', industry='FMCG',
                 location='Mumbai', desc='Leading emerging markets company in household insecticides and personal care.'),
            dict(email='careers@colgate.co.in',    password='admin123', name='Colgate-Palmolive India',
                 company='Colgate-Palmolive (India) Limited', gst='27AAACL2567L4ZL', domain='colgate.co.in',
                 linkedin='https://linkedin.com/company/colgate', industry='FMCG / Oral Care',
                 location='Mumbai', desc='Leading provider of oral care, personal care, and home care products.'),
            dict(email='hr@reckitt.com',           password='admin123', name='Reckitt India',
                 company='Reckitt Benckiser (India) Limited', gst='27AAACR3678M4ZK', domain='reckitt.com',
                 linkedin='https://linkedin.com/company/reckitt', industry='FMCG / Health',
                 location='Gurugram', desc='Global consumer health and hygiene company with brands like Dettol and Harpic.'),
            dict(email='recruit@pg.com',           password='admin123', name='Procter & Gamble India',
                 company='Procter & Gamble Hygiene and Health Care Ltd', gst='27AAACP4789N4ZJ', domain='pg.com',
                 linkedin='https://linkedin.com/company/pg', industry='FMCG',
                 location='Mumbai', desc='Multinational consumer goods company known for Ariel, Pampers, and Pantene.'),
            dict(email='careers@patanjaliayurved.net', password='admin123', name='Patanjali Ayurved',
                 company='Patanjali Ayurved Limited', gst='05AAACP5890O4ZI', domain='patanjaliayurved.net',
                 linkedin='https://linkedin.com/company/patanjali-ayurved', industry='FMCG / Ayurvedic',
                 location='Haridwar', desc='Major FMCG company producing Ayurvedic, herbal, and food products.'),
            dict(email='hr@asianpaints.com',       password='admin123', name='Asian Paints',
                 company='Asian Paints Limited', gst='27AAACA6901P4ZH', domain='asianpaints.com',
                 linkedin='https://linkedin.com/company/asian-paints', industry='Paints / Coatings',
                 location='Mumbai', desc='India\'s largest and Asia\'s third largest paint company.'),
            dict(email='recruit@bergerindia.com',  password='admin123', name='Berger Paints',
                 company='Berger Paints India Limited', gst='19AAACB7012Q4ZG', domain='bergerindia.com',
                 linkedin='https://linkedin.com/company/berger-paints-india', industry='Paints',
                 location='Kolkata', desc='India\'s second largest paint company with decorative and industrial paints.'),
            dict(email='careers@pidilite.com',     password='admin123', name='Pidilite',
                 company='Pidilite Industries Limited', gst='27AAACP8123R4ZF', domain='pidilite.com',
                 linkedin='https://linkedin.com/company/pidilite-industries', industry='Adhesives / Chemicals',
                 location='Mumbai', desc='Market leader in adhesives and construction chemicals in India.'),
            dict(email='hr@tataconsumer.com',      password='admin123', name='Tata Consumer Products',
                 company='Tata Consumer Products Limited', gst='33AAACT9234S4ZE', domain='tataconsumer.com',
                 linkedin='https://linkedin.com/company/tata-consumer-products', industry='FMCG / Food & Beverages',
                 location='Kolkata', desc='FMCG company of the Tata Group with Tata Tea, Tata Salt, and Himalayan brands.'),

            # ── Pharma & Healthcare ──────────────────────────────────────────────
            dict(email='recruit@sunpharma.com',    password='admin123', name='Sun Pharma',
                 company='Sun Pharmaceutical Industries Limited', gst='24AAACS0345T4ZD', domain='sunpharma.com',
                 linkedin='https://linkedin.com/company/sun-pharma', industry='Pharmaceuticals',
                 location='Mumbai', desc='World\'s fourth largest specialty generic pharma company.'),
            dict(email='careers@cipla.com',        password='admin123', name='Cipla',
                 company='Cipla Limited', gst='27AAACC1456U4ZC', domain='cipla.com',
                 linkedin='https://linkedin.com/company/cipla', industry='Pharmaceuticals',
                 location='Mumbai', desc='Global pharmaceutical company focused on healthcare in India and emerging markets.'),
            dict(email='hr@drreddys.com',          password='admin123', name='Dr. Reddy\'s Laboratories',
                 company='Dr. Reddy\'s Laboratories Limited', gst='36AAACD2567V4ZB', domain='drreddys.com',
                 linkedin='https://linkedin.com/company/dr-reddys-laboratories', industry='Pharmaceuticals',
                 location='Hyderabad', desc='Integrated pharmaceutical company offering generic medicines globally.'),
            dict(email='recruit@lupin.com',        password='admin123', name='Lupin',
                 company='Lupin Limited', gst='27AAACL3678W4ZA', domain='lupin.com',
                 linkedin='https://linkedin.com/company/lupin', industry='Pharmaceuticals',
                 location='Mumbai', desc='Transnational pharmaceutical company with a strong US generic drug portfolio.'),
            dict(email='careers@aurobindopharma.com', password='admin123', name='Aurobindo Pharma',
                 company='Aurobindo Pharma Limited', gst='36AAACA4789X4ZZ', domain='aurobindopharma.com',
                 linkedin='https://linkedin.com/company/aurobindo-pharma', industry='Pharmaceuticals',
                 location='Hyderabad', desc='Global pharma company manufacturing and exporting active pharma ingredients.'),
            dict(email='hr@zyduslife.com',         password='admin123', name='Zydus Lifesciences',
                 company='Zydus Lifesciences Limited', gst='24AAACZ5890Y4ZY', domain='zyduslife.com',
                 linkedin='https://linkedin.com/company/zydus-lifesciences', industry='Pharmaceuticals',
                 location='Ahmedabad', desc='Global innovative life sciences company committed to healthy living.'),
            dict(email='recruit@glenmark.com',     password='admin123', name='Glenmark Pharmaceuticals',
                 company='Glenmark Pharmaceuticals Limited', gst='27AAACG6901Z4ZX', domain='glenmark.com',
                 linkedin='https://linkedin.com/company/glenmark-pharmaceuticals', industry='Pharmaceuticals',
                 location='Mumbai', desc='Research-based pharmaceutical company with branded generics and specialty products.'),
            dict(email='careers@divis.com',        password='admin123', name='Divi\'s Laboratories',
                 company='Divi\'s Laboratories Limited', gst='36AAACD7012A5ZW', domain='divis.com',
                 linkedin='https://linkedin.com/company/divis-laboratories', industry='Pharma / API',
                 location='Hyderabad', desc='World leader in manufacturing active pharmaceutical ingredients and nutraceuticals.'),
            dict(email='hr@alkem.com',             password='admin123', name='Alkem Laboratories',
                 company='Alkem Laboratories Limited', gst='27AAACA8123B5ZV', domain='alkem.com',
                 linkedin='https://linkedin.com/company/alkem-laboratories', industry='Pharmaceuticals',
                 location='Mumbai', desc='Multinational pharmaceutical company ranked among India\'s top pharma firms.'),
            dict(email='recruit@intaspharma.com',  password='admin123', name='Intas Pharmaceuticals',
                 company='Intas Pharmaceuticals Limited', gst='24AAACI9234C5ZU', domain='intaspharma.com',
                 linkedin='https://linkedin.com/company/intas-pharmaceuticals', industry='Pharmaceuticals',
                 location='Ahmedabad', desc='Research-driven global pharmaceutical company with diversified portfolio.'),
            dict(email='careers@torrentpharma.com',password='admin123', name='Torrent Pharmaceuticals',
                 company='Torrent Pharmaceuticals Limited', gst='24AAACT0345D5ZT', domain='torrentpharma.com',
                 linkedin='https://linkedin.com/company/torrent-pharmaceuticals', industry='Pharmaceuticals',
                 location='Ahmedabad', desc='Pharmaceutical company with therapeutic focus on cardiology and CNS.'),
            dict(email='hr@glandpharma.com',       password='admin123', name='Gland Pharma',
                 company='Gland Pharma Limited', gst='36AAACG1456E5ZS', domain='glandpharma.com',
                 linkedin='https://linkedin.com/company/gland-pharma', industry='Pharma / Injectable',
                 location='Hyderabad', desc='Global pharma company specializing in injectable formulations.'),
            dict(email='recruit@lauruslabs.com',   password='admin123', name='Laurus Labs',
                 company='Laurus Labs Limited', gst='36AAACL2567F5ZR', domain='lauruslabs.com',
                 linkedin='https://linkedin.com/company/laurus-labs', industry='Pharmaceuticals',
                 location='Hyderabad', desc='Leading pharmaceutical company focused on anti-retroviral APIs and formulations.'),
            dict(email='careers@suven.com',        password='admin123', name='Suven Pharmaceuticals',
                 company='Suven Pharmaceuticals Limited', gst='36AAACS3678G5ZQ', domain='suven.com',
                 linkedin='https://linkedin.com/company/suven-pharmaceuticals', industry='Pharma / CRAMS',
                 location='Hyderabad', desc='Contract research and manufacturing services company in specialty chemicals and pharma.'),
            dict(email='hr@glenmarkls.com',        password='admin123', name='Glenmark Life Sciences',
                 company='Glenmark Life Sciences Limited', gst='24AAACG4789H5ZP', domain='glenmarkls.com',
                 linkedin='https://linkedin.com/company/glenmark-life-sciences', industry='Pharma / API',
                 location='Navi Mumbai', desc='Developer and manufacturer of high-value active pharmaceutical ingredients.'),
            dict(email='recruit@seruminstitute.com', password='admin123', name='Serum Institute of India',
                 company='Serum Institute of India Pvt Ltd', gst='27AAACS5890I5ZO', domain='seruminstitute.com',
                 linkedin='https://linkedin.com/company/serum-institute-of-india', industry='Vaccines / Pharma',
                 location='Pune', desc='World\'s largest vaccine manufacturer by doses produced and sold.'),
            dict(email='careers@bharatbiotech.com',password='admin123', name='Bharat Biotech',
                 company='Bharat Biotech International Limited', gst='36AAACB6901J5ZN', domain='bharatbiotech.com',
                 linkedin='https://linkedin.com/company/bharat-biotech', industry='Biotech / Vaccines',
                 location='Hyderabad', desc='Pioneer in vaccine development including Covaxin for COVID-19.'),
            dict(email='hr@pfizer.co.in',          password='admin123', name='Pfizer India',
                 company='Pfizer Limited India', gst='27AAACP7012K5ZM', domain='pfizer.co.in',
                 linkedin='https://linkedin.com/company/pfizer', industry='Pharmaceuticals',
                 location='Mumbai', desc='Leading global pharmaceutical company with innovative medicines and vaccines.'),
            dict(email='recruit@abbott.com',       password='admin123', name='Abbott India',
                 company='Abbott India Limited', gst='27AAACA8123L5ZL', domain='abbott.com',
                 linkedin='https://linkedin.com/company/abbott', industry='Healthcare / Pharma',
                 location='Mumbai', desc='Global healthcare company in diagnostics, medical devices, and nutrition.'),
            dict(email='careers@gsk.com',          password='admin123', name='GlaxoSmithKline India',
                 company='GlaxoSmithKline Pharmaceuticals Limited', gst='27AAACG9234M5ZK', domain='gsk.com',
                 linkedin='https://linkedin.com/company/gsk', industry='Pharmaceuticals',
                 location='Mumbai', desc='Global pharma company with medicines, vaccines, and consumer healthcare products.'),
            dict(email='hr@jnj.com',               password='admin123', name='Johnson & Johnson India',
                 company='Johnson & Johnson Pvt Ltd India', gst='27AAACJ0345N5ZJ', domain='jnj.com',
                 linkedin='https://linkedin.com/company/johnson-johnson', industry='Healthcare / Pharma',
                 location='Mumbai', desc='Global healthcare company operating in medical devices, pharma, and consumer health.'),
            dict(email='recruit@apollohospitals.com', password='admin123', name='Apollo Hospitals',
                 company='Apollo Hospitals Enterprise Limited', gst='33AAACA1456O5ZI', domain='apollohospitals.com',
                 linkedin='https://linkedin.com/company/apollo-hospitals', industry='Healthcare',
                 location='Chennai', desc='Largest private hospital chain in Asia.'),
            dict(email='careers@fortishealthcare.com', password='admin123', name='Fortis Healthcare',
                 company='Fortis Healthcare Limited', gst='07AAACF2567P5ZH', domain='fortishealthcare.com',
                 linkedin='https://linkedin.com/company/fortis-healthcare', industry='Healthcare',
                 location='Gurugram', desc='Leading integrated healthcare delivery service provider in India.'),
            dict(email='hr@maxhealthcare.in',      password='admin123', name='Max Healthcare',
                 company='Max Healthcare Institute Limited', gst='07AAACM3678Q5ZG', domain='maxhealthcare.in',
                 linkedin='https://linkedin.com/company/max-healthcare', industry='Healthcare',
                 location='Delhi', desc='Hospital network providing comprehensive healthcare services in North India.'),
            dict(email='recruit@narayanahealth.org',password='admin123', name='Narayana Health',
                 company='Narayana Hrudayalaya Limited', gst='29AAACN4789R5ZF', domain='narayanahealth.org',
                 linkedin='https://linkedin.com/company/narayana-health', industry='Healthcare',
                 location='Bengaluru', desc='Chain of multispecialty hospitals known for affordable healthcare.'),
            dict(email='careers@asterhospitals.com', password='admin123', name='Aster DM Healthcare',
                 company='Aster DM Healthcare Limited', gst='32AAACA5890S5ZE', domain='asterhospitals.com',
                 linkedin='https://linkedin.com/company/aster-dm-healthcare', industry='Healthcare',
                 location='Kochi', desc='Integrated healthcare organization with hospitals and clinics across India and GCC.'),
            dict(email='hr@manipalhospitals.com',  password='admin123', name='Manipal Hospitals',
                 company='Manipal Health Enterprises Pvt Ltd', gst='29AAACM6901T5ZD', domain='manipalhospitals.com',
                 linkedin='https://linkedin.com/company/manipal-hospitals', industry='Healthcare',
                 location='Bengaluru', desc='Largest hospital chain in India with focus on multi-specialty care.'),
            dict(email='recruit@lalpathlabs.com',  password='admin123', name='Dr. Lal PathLabs',
                 company='Dr Lal PathLabs Limited', gst='07AAACD7012U5ZC', domain='lalpathlabs.com',
                 linkedin='https://linkedin.com/company/dr-lal-pathlabs', industry='Diagnostics',
                 location='Delhi', desc='India\'s leading pathology services provider.'),

            # ── Automobiles ──────────────────────────────────────────────────────
            dict(email='careers@marutisuzuki.com', password='admin123', name='Maruti Suzuki',
                 company='Maruti Suzuki India Limited', gst='06AAACM8123V5ZB', domain='marutisuzuki.com',
                 linkedin='https://linkedin.com/company/maruti-suzuki-india', industry='Automobiles',
                 location='Delhi', desc='India\'s largest passenger car manufacturer.'),
            dict(email='hr@tatamotors.com',        password='admin123', name='Tata Motors',
                 company='Tata Motors Limited', gst='27AAACT9234W5ZA', domain='tatamotors.com',
                 linkedin='https://linkedin.com/company/tata-motors', industry='Automobiles',
                 location='Mumbai', desc='Multinational automotive manufacturer with commercial and passenger vehicles.'),
            dict(email='recruit@mahindra.com',     password='admin123', name='Mahindra & Mahindra',
                 company='Mahindra & Mahindra Limited', gst='27AAACM0345X5ZZ', domain='mahindra.com',
                 linkedin='https://linkedin.com/company/mahindra', industry='Automobiles',
                 location='Mumbai', desc='Largest tractor producer in the world and leading utility vehicle maker in India.'),
            dict(email='careers@bajajauto.com',    password='admin123', name='Bajaj Auto',
                 company='Bajaj Auto Limited', gst='27AAACB1456Y5ZY', domain='bajajauto.com',
                 linkedin='https://linkedin.com/company/bajaj-auto', industry='Two-wheelers / Three-wheelers',
                 location='Pune', desc='World\'s largest three-wheeler manufacturer and major two-wheeler company.'),
            dict(email='hr@heromotocorp.com',      password='admin123', name='Hero MotoCorp',
                 company='Hero MotoCorp Limited', gst='06AAACH2567Z5ZX', domain='heromotocorp.com',
                 linkedin='https://linkedin.com/company/hero-motocorp', industry='Two-wheelers',
                 location='Delhi', desc='World\'s largest manufacturer of motorcycles and scooters.'),
            dict(email='recruit@hyundai.com',      password='admin123', name='Hyundai Motor India',
                 company='Hyundai Motor India Limited', gst='33AAACH3678A6ZW', domain='hyundai.com',
                 linkedin='https://linkedin.com/company/hyundai-motor-company', industry='Automobiles',
                 location='Chennai', desc='India\'s second largest car manufacturer with wholly-owned subsidiary of Hyundai Motor Company.'),
            dict(email='careers@eichergroup.com',  password='admin123', name='Eicher Motors',
                 company='Eicher Motors Limited', gst='07AAACE4789B6ZV', domain='eichergroup.com',
                 linkedin='https://linkedin.com/company/eicher-motors', industry='Automobiles / Motorcycles',
                 location='Delhi', desc='Manufacturer of commercial vehicles and owner of the Royal Enfield brand.'),
            dict(email='hr@ashokleyland.com',      password='admin123', name='Ashok Leyland',
                 company='Ashok Leyland Limited', gst='33AAACA5890C6ZU', domain='ashokleyland.com',
                 linkedin='https://linkedin.com/company/ashok-leyland', industry='Commercial Vehicles',
                 location='Chennai', desc='India\'s second largest commercial vehicle manufacturer.'),
            dict(email='recruit@mrftyres.com',     password='admin123', name='MRF',
                 company='MRF Limited', gst='33AAACM6901D6ZT', domain='mrftyres.com',
                 linkedin='https://linkedin.com/company/mrf', industry='Tyres',
                 location='Chennai', desc='India\'s largest tyre manufacturer and the most expensive stock by value in Indian markets.'),
            dict(email='careers@apollotyres.com',  password='admin123', name='Apollo Tyres',
                 company='Apollo Tyres Limited', gst='06AAACA7012E6ZS', domain='apollotyres.com',
                 linkedin='https://linkedin.com/company/apollo-tyres', industry='Tyres',
                 location='Gurugram', desc='Leading tyre manufacturer with global operations in India and Europe.'),
            dict(email='hr@bosch.in',              password='admin123', name='Bosch India',
                 company='Bosch Limited India', gst='29AAACB8123F6ZR', domain='bosch.in',
                 linkedin='https://linkedin.com/company/bosch', industry='Auto Components',
                 location='Bengaluru', desc='Multinational engineering and technology company known for auto parts and power tools.'),
            dict(email='recruit@cummins.com',      password='admin123', name='Cummins India',
                 company='Cummins India Limited', gst='27AAACG9234G6ZQ', domain='cummins.com',
                 linkedin='https://linkedin.com/company/cummins', industry='Engines / Industrial',
                 location='Pune', desc='Designs, manufactures, and distributes engines, filtration, and power systems.'),
            dict(email='careers@exideindustries.com', password='admin123', name='Exide Industries',
                 company='Exide Industries Limited', gst='19AAACE0345H6ZP', domain='exideindustries.com',
                 linkedin='https://linkedin.com/company/exide-industries', industry='Auto Components / Batteries',
                 location='Kolkata', desc='India\'s largest manufacturer of lead-acid storage batteries.'),
            dict(email='hr@adanitransmission.com', password='admin123', name='Adani Transmission',
                 company='Adani Transmission Limited', gst='24AAACA1456I6ZO', domain='adanitransmission.com',
                 linkedin='https://linkedin.com/company/adani-transmission', industry='Power Transmission',
                 location='Ahmedabad', desc='India\'s largest private power transmission company.'),

            # ── Conglomerates & Others ───────────────────────────────────────────
            dict(email='recruit@ril.com',          password='admin123', name='Reliance Industries',
                 company='Reliance Industries Limited', gst='27AAACR2567J6ZN', domain='ril.com',
                 linkedin='https://linkedin.com/company/reliance-industries', industry='Conglomerate',
                 location='Mumbai', desc='India\'s largest company by market cap, with energy, petrochemicals, retail, and telecom.'),
            dict(email='careers@jio.com',          password='admin123', name='Reliance Jio',
                 company='Reliance Jio Infocomm Limited', gst='27AAACR3678K6ZM', domain='jio.com',
                 linkedin='https://linkedin.com/company/reliance-jio', industry='Telecom / Internet',
                 location='Mumbai', desc='India\'s largest mobile network operator by subscribers.'),
            dict(email='hr@relianceretail.com',    password='admin123', name='Reliance Retail',
                 company='Reliance Retail Limited', gst='27AAACR4789L6ZL', domain='relianceretail.com',
                 linkedin='https://linkedin.com/company/reliance-retail', industry='Retail',
                 location='Mumbai', desc='India\'s largest retailer operating across fashion, grocery, electronics and more.'),
            dict(email='recruit@tata.com',         password='admin123', name='Tata Sons',
                 company='Tata Sons Private Limited', gst='27AAACT5890M6ZK', domain='tata.com',
                 linkedin='https://linkedin.com/company/tata-sons', industry='Conglomerate',
                 location='Mumbai', desc='Principal investment holding company and promoter of Tata Group companies.'),
            dict(email='careers@larsentoubro.com', password='admin123', name='Larsen & Toubro',
                 company='Larsen & Toubro Limited', gst='27AAACL6901N6ZJ', domain='larsentoubro.com',
                 linkedin='https://linkedin.com/company/larsen-and-toubro', industry='Engineering / Construction',
                 location='Mumbai', desc='Indian multinational engaged in technology, engineering, construction, manufacturing and finance.'),
            dict(email='hr@hal-india.co.in',       password='admin123', name='HAL',
                 company='Hindustan Aeronautics Limited', gst='29AAACH7012O6ZI', domain='hal-india.co.in',
                 linkedin='https://linkedin.com/company/hindustan-aeronautics-limited', industry='Defence / Aeronautics',
                 location='Bengaluru', desc='Indian state-owned aerospace and defence company.'),
            dict(email='recruit@bel-india.in',     password='admin123', name='Bharat Electronics',
                 company='Bharat Electronics Limited', gst='29AAACB8123P6ZH', domain='bel-india.in',
                 linkedin='https://linkedin.com/company/bharat-electronics-limited', industry='Defence Electronics',
                 location='Bengaluru', desc='Indian government-owned producer of advanced electronic products for defence.'),
            dict(email='careers@bdl-india.in',     password='admin123', name='Bharat Dynamics',
                 company='Bharat Dynamics Limited', gst='36AAACB9234Q6ZG', domain='bdl-india.in',
                 linkedin='https://linkedin.com/company/bharat-dynamics-limited', industry='Defence',
                 location='Hyderabad', desc='Defence PSU manufacturing guided missile systems and allied defence equipment.'),
            dict(email='hr@mazagondock.in',        password='admin123', name='Mazagon Dock',
                 company='Mazagon Dock Shipbuilders Limited', gst='27AAACM0345R6ZF', domain='mazagondock.in',
                 linkedin='https://linkedin.com/company/mazagon-dock', industry='Shipbuilding / Defence',
                 location='Mumbai', desc='India\'s premier shipyard building warships and submarines for the Indian Navy.'),
            dict(email='recruit@ultratechcement.com', password='admin123', name='UltraTech Cement',
                 company='UltraTech Cement Limited', gst='27AAACG1456S6ZE', domain='ultratechcement.com',
                 linkedin='https://linkedin.com/company/ultratech-cement', industry='Cement',
                 location='Mumbai', desc='India\'s largest and world\'s third largest cement company.'),
            dict(email='careers@shreecement.com',  password='admin123', name='Shree Cement',
                 company='Shree Cement Limited', gst='08AAACS2567T6ZD', domain='shreecement.com',
                 linkedin='https://linkedin.com/company/shree-cement', industry='Cement',
                 location='Kolkata', desc='One of India\'s largest cement producers with significant energy efficiency.'),
            dict(email='hr@ambuja.com',            password='admin123', name='Ambuja Cements',
                 company='Ambuja Cements Limited', gst='24AAACA3678U6ZC', domain='ambuja.com',
                 linkedin='https://linkedin.com/company/ambuja-cements', industry='Cement',
                 location='Mumbai', desc='One of the leading cement companies in India backed by Adani Group.'),
            dict(email='recruit@dmartindia.com',   password='admin123', name='Avenue Supermarts (DMart)',
                 company='Avenue Supermarts Limited', gst='27AAACA4789V6ZB', domain='dmartindia.com',
                 linkedin='https://linkedin.com/company/avenue-supermarts', industry='Retail / Supermarkets',
                 location='Mumbai', desc='Operator of DMart, one of India\'s largest supermarket chains.'),
            dict(email='careers@titancompany.in',  password='admin123', name='Titan Company',
                 company='Titan Company Limited', gst='33AAACT5890W6ZA', domain='titancompany.in',
                 linkedin='https://linkedin.com/company/titan-company', industry='Retail / Lifestyle',
                 location='Bengaluru', desc='Largest Indian manufacturer of watches, jewellery, and eyewear.'),
            dict(email='hr@siemens.com',           password='admin123', name='Siemens India',
                 company='Siemens Limited India', gst='27AAACS6901X6ZZ', domain='siemens.com',
                 linkedin='https://linkedin.com/company/siemens', industry='Engineering / Electronics',
                 location='Mumbai', desc='German-Indian multinational conglomerate focused on digitalization and electrification.'),
            dict(email='recruit@havells.com',      password='admin123', name='Havells India',
                 company='Havells India Limited', gst='06AAACH7012Y6ZY', domain='havells.com',
                 linkedin='https://linkedin.com/company/havells-india', industry='Electricals / Consumer Durables',
                 location='Noida', desc='India\'s leading electrical equipment company with fast-moving electrical goods.'),
            dict(email='careers@crompton.co.in',   password='admin123', name='Crompton Greaves Consumer',
                 company='Crompton Greaves Consumer Electricals Limited', gst='27AAACG8123Z6ZX', domain='crompton.co.in',
                 linkedin='https://linkedin.com/company/crompton-greaves-consumer-electricals', industry='Consumer Electricals',
                 location='Mumbai', desc='India\'s leading consumer electrical goods company known for fans and lighting.'),
            dict(email='hr@voltas.com',            password='admin123', name='Voltas',
                 company='Voltas Limited', gst='27AAACV9234A7ZW', domain='voltas.com',
                 linkedin='https://linkedin.com/company/voltas', industry='Consumer Durables / Engineering',
                 location='Mumbai', desc='India\'s leading room air conditioner brand and engineering services company under Tata.'),
            dict(email='recruit@grasim.com',       password='admin123', name='Grasim Industries',
                 company='Grasim Industries Limited', gst='23AAACG0345B7ZV', domain='grasim.com',
                 linkedin='https://linkedin.com/company/grasim-industries', industry='Diversified',
                 location='Mumbai', desc='Flagship company of Aditya Birla Group with operations in chemicals, textiles, and cement.'),
            dict(email='careers@upl-ltd.com',      password='admin123', name='UPL',
                 company='UPL Limited', gst='27AAACP1456C7ZU', domain='upl-ltd.com',
                 linkedin='https://linkedin.com/company/upl', industry='Agrochemicals',
                 location='Mumbai', desc='Global provider of sustainable agriculture products and solutions.'),
            dict(email='hr@aartiindustries.com',   password='admin123', name='Aarti Industries',
                 company='Aarti Industries Limited', gst='24AAAAA2567D7ZT', domain='aartiindustries.com',
                 linkedin='https://linkedin.com/company/aarti-industries', industry='Specialty Chemicals',
                 location='Vapi', desc='Leading manufacturer of benzene-based specialty chemicals and pharma ingredients.'),
            dict(email='recruit@tatachemicals.com',password='admin123', name='Tata Chemicals',
                 company='Tata Chemicals Limited', gst='24AAACT3678E7ZS', domain='tatachemicals.com',
                 linkedin='https://linkedin.com/company/tata-chemicals', industry='Specialty Chemicals',
                 location='Mumbai', desc='Global chemicals company making soda ash, sodium bicarbonate, and specialty products.'),
            dict(email='careers@kecrpg.com',       password='admin123', name='KEC International',
                 company='KEC International Limited', gst='27AAACK4789F7ZR', domain='kecrpg.com',
                 linkedin='https://linkedin.com/company/kec-international', industry='Power Transmission / Infrastructure',
                 location='Mumbai', desc='Global infrastructure company providing end-to-end solutions in power transmission.'),
            dict(email='hr@adaniports.com',        password='admin123', name='Adani Ports',
                 company='Adani Ports and Special Economic Zone Limited', gst='24AAACA5890G7ZQ', domain='adaniports.com',
                 linkedin='https://linkedin.com/company/adani-ports-and-sez', industry='Ports / Logistics',
                 location='Ahmedabad', desc='India\'s largest commercial ports and logistics operator.'),
            dict(email='recruit@adani.com',        password='admin123', name='Adani Enterprises',
                 company='Adani Enterprises Limited', gst='24AAACA6901H7ZP', domain='adani.com',
                 linkedin='https://linkedin.com/company/adani-enterprises-limited', industry='Conglomerate',
                 location='Ahmedabad', desc='Flagship company of the Adani Group with interests in resources, logistics, and agri.'),
            dict(email='careers@adaniwilmar.com',  password='admin123', name='Adani Wilmar',
                 company='Adani Wilmar Limited', gst='24AAACA7012I7ZO', domain='adaniwilmar.com',
                 linkedin='https://linkedin.com/company/adani-wilmar', industry='FMCG / Edible Oil',
                 location='Ahmedabad', desc='Joint venture of Adani and Wilmar, maker of Fortune edible oils and foods.'),
            dict(email='hr@dlf.in',                password='admin123', name='DLF',
                 company='DLF Limited', gst='06AAACD8123J7ZN', domain='dlf.in',
                 linkedin='https://linkedin.com/company/dlf', industry='Real Estate',
                 location='Gurugram', desc='India\'s largest real estate developer.'),
            dict(email='recruit@lodhagroup.com',   password='admin123', name='Macrotech Developers (Lodha)',
                 company='Macrotech Developers Limited', gst='27AAACM9234K7ZM', domain='lodhagroup.com',
                 linkedin='https://linkedin.com/company/macrotech-developers-lodha', industry='Real Estate',
                 location='Mumbai', desc='India\'s largest real estate developer by sales, known as Lodha Group.'),
            dict(email='careers@prestigeconstructions.com', password='admin123', name='Prestige Estates',
                 company='Prestige Estates Projects Limited', gst='29AAACP0345L7ZL', domain='prestigeconstructions.com',
                 linkedin='https://linkedin.com/company/prestige-group', industry='Real Estate',
                 location='Bengaluru', desc='Leading real estate developer in South India.'),
            dict(email='hr@goindigo.in',           password='admin123', name='IndiGo',
                 company='InterGlobe Aviation Limited', gst='07AAACI1456M7ZK', domain='goindigo.in',
                 linkedin='https://linkedin.com/company/indigo-airlines', industry='Aviation',
                 location='Gurugram', desc='India\'s largest passenger airline by market share.'),
            dict(email='recruit@airindia.in',      password='admin123', name='Air India',
                 company='Tata SIA Airlines Limited (Air India)', gst='07AAACA2567N7ZJ', domain='airindia.in',
                 linkedin='https://linkedin.com/company/air-india', industry='Aviation',
                 location='Delhi', desc='India\'s flagship carrier now owned by the Tata Group.'),
            dict(email='careers@tatacommunications.com', password='admin123', name='Tata Communications',
                 company='Tata Communications Limited', gst='27AAACT3678O7ZI', domain='tatacommunications.com',
                 linkedin='https://linkedin.com/company/tata-communications', industry='Telecom / Cloud',
                 location='Mumbai', desc='Global digital infrastructure company enabling digital transformation.'),
            dict(email='hr@vodafoneidea.com',      password='admin123', name='Vodafone Idea',
                 company='Vodafone Idea Limited', gst='27AAACV4789P7ZH', domain='vodafoneidea.com',
                 linkedin='https://linkedin.com/company/vodafone-idea', industry='Telecom',
                 location='Mumbai', desc='Telecom operator providing voice, data, and broadband services across India.'),
            dict(email='recruit@industowers.com',  password='admin123', name='Indus Towers',
                 company='Indus Towers Limited', gst='27AAACI5890Q7ZG', domain='industowers.com',
                 linkedin='https://linkedin.com/company/indus-towers', industry='Telecom Infrastructure',
                 location='Gurugram', desc='India\'s largest telecom tower company and the world\'s largest outside China.'),
            dict(email='hr@zee.com',               password='admin123', name='Zee Entertainment',
                 company='ZEE Entertainment Enterprises Limited', gst='27AAACZ7012S7ZE', domain='zee.com',
                 linkedin='https://linkedin.com/company/zee-entertainment', industry='Media / Entertainment',
                 location='Mumbai', desc='One of the world\'s largest broadcast companies with a strong India presence.'),
            dict(email='recruit@cibil.com',        password='admin123', name='TransUnion CIBIL',
                 company='TransUnion CIBIL Limited', gst='27AAACT8123T7ZD', domain='cibil.com',
                 linkedin='https://linkedin.com/company/transunion-cibil', industry='Credit Information',
                 location='Mumbai', desc='India\'s first credit information company providing credit scores and reports.'),
            dict(email='careers@deloitte.com',     password='admin123', name='Deloitte India',
                 company='Deloitte Touche Tohmatsu India LLP', gst='27AAACD9234U7ZC', domain='deloitte.com',
                 linkedin='https://linkedin.com/company/deloitte', industry='Professional Services',
                 location='Mumbai', desc='Multinational professional services network offering audit, consulting, and tax advisory.'),
            dict(email='hr@apple.com',             password='admin123', name='Apple India',
                 company='Apple India Pvt Ltd', gst='29AAACA0345V7ZB', domain='apple.com',
                 linkedin='https://linkedin.com/company/apple', industry='Technology / Consumer Electronics',
                 location='Bengaluru', desc='World\'s most valuable company, designing consumer electronics, software, and services.'),
            dict(email='recruit@schneider-electric.com', password='admin123', name='Schneider Electric India',
                 company='Schneider Electric India Pvt Ltd', gst='29AAACS1456W7ZA', domain='schneider-electric.com',
                 linkedin='https://linkedin.com/company/schneider-electric', industry='Energy Management',
                 location='Bengaluru', desc='Global leader in energy management and automation solutions.'),
            dict(email='careers@jockey.in',        password='admin123', name='Page Industries',
                 company='Page Industries Limited', gst='29AAACP2567X7ZZ', domain='jockey.in',
                 linkedin='https://linkedin.com/company/page-industries', industry='Apparel / Retail',
                 location='Bengaluru', desc='Exclusive licensee of Jockey International in India and other South Asian countries.'),
            dict(email='hr@metrobrands.com',       password='admin123', name='Metro Brands',
                 company='Metro Brands Limited', gst='27AAACM3678Y7ZY', domain='metrobrands.com',
                 linkedin='https://linkedin.com/company/metro-brands', industry='Retail / Footwear',
                 location='Mumbai', desc='One of India\'s largest footwear speciality retailers.'),
            dict(email='recruit@decathlon.in',     password='admin123', name='Decathlon India',
                 company='Decathlon Sports India Pvt Ltd', gst='29AAACD4789Z7ZX', domain='decathlon.in',
                 linkedin='https://linkedin.com/company/decathlon', industry='Retail / Sporting Goods',
                 location='Bengaluru', desc='World\'s largest sporting goods retailer with strong India presence.'),
            dict(email='careers@marriott.com',     password='admin123', name='Marriott India',
                 company='Marriott International India', gst='29AAACM5890A8ZW', domain='marriott.com',
                 linkedin='https://linkedin.com/company/marriott-international', industry='Hospitality',
                 location='Bengaluru', desc='World\'s largest hotel company with multiple brands across India.'),
            dict(email='hr@adidas.in',             password='admin123', name='Adidas India',
                 company='Adidas India Marketing Pvt Ltd', gst='07AAACA6901B8ZV', domain='adidas.in',
                 linkedin='https://linkedin.com/company/adidas', industry='Sporting Goods / Apparel',
                 location='Gurugram', desc='Multinational sportswear brand with growing India retail and e-commerce.'),
            dict(email='recruit@bajaj.com',        password='admin123', name='Bajaj Holdings',
                 company='Bajaj Holdings & Investment Limited', gst='27AAACB7012C8ZU', domain='bajaj.com',
                 linkedin='https://linkedin.com/company/bajaj-holdings', industry='Investment / Conglomerate',
                 location='Pune', desc='Core investment company of the Bajaj Group holding stakes across financial and manufacturing firms.'),
            dict(email='careers@bajajlife.com',    password='admin123', name='Bajaj Allianz Life Insurance',
                 company='Bajaj Allianz Life Insurance Company Limited', gst='27AAACB8123D8ZT', domain='bajajlife.com',
                 linkedin='https://linkedin.com/company/bajaj-allianz-life-insurance', industry='Insurance',
                 location='Pune', desc='Life insurance joint venture between Bajaj Finserv and Allianz SE.'),
            dict(email='hr@sterlitepower.com',     password='admin123', name='Sterlite Power',
                 company='Sterlite Power Transmission Limited', gst='27AAACS9234E8ZS', domain='sterlitepower.com',
                 linkedin='https://linkedin.com/company/sterlite-power', industry='Power Transmission',
                 location='Gurugram', desc='Global developer and operator of power transmission infrastructure.'),
            dict(email='recruit@icicipruamc.com',   password='admin123', name='ICICI Prudential AMC',
                 company='ICICI Prudential Asset Management Company', gst='27AAACI0345F8ZR', domain='icicipruamc.com',
                 linkedin='https://linkedin.com/company/icici-prudential-amc', industry='Asset Management',
                 location='Mumbai', desc='India\'s largest asset management company offering mutual funds.'),
            dict(email='careers@naukri.com',       password='admin123', name='Naukri.com (Info Edge)',
                 company='Info Edge India Limited', gst='07AAACI1456G8ZQ', domain='naukri.com',
                 linkedin='https://linkedin.com/company/info-edge', industry='Internet / Recruitment',
                 location='Noida', desc='India\'s No.1 job portal with Naukri.com, 99acres, Jeevansathi, and Shiksha.'),
        ]

        admin_pwd_hash = generate_password_hash('admin123')
        
        for o in partner_orgs_data:
            user = User.query.filter_by(email=o['email']).first()
            if not user:
                user = User(email=o['email'], name=o['name'],
                            password=admin_pwd_hash, role='organization')
                db.session.add(user)
                db.session.flush()
                org = Organization(
                    user_id=user.id, company_name=o['company'], gst_number=o['gst'],
                    domain_email=o['domain'], linkedin_profile=o['linkedin'],
                    industry=o['industry'], location=o['location'], description=o['desc'],
                    is_verified=True, verification_status='approved',
                )
                db.session.add(org)
                db.session.flush()
                print(f'  ✅ Partner Org: {o["company"]}')
            else:
                print(f'  ⏭️  Partner Org exists: {o["company"]}')

        db.session.commit()

        # ── DEMO ORGANIZATIONS ───────────────────────────────────────────────
        orgs_data = [
            dict(email='hr@technova.io',      password='org123', name='TechNova Solutions',
                 company='TechNova Solutions',  gst='27AABCT1332L1ZG', domain='technova.io',
                 linkedin='https://linkedin.com/company/technova', industry='Software',
                 location='Bangalore', desc='Full-stack product company building SaaS tools for SMEs.'),
            dict(email='careers@datamind.ai',  password='org123', name='DataMind Analytics',
                 company='DataMind Analytics',  gst='27AABCD5566M1ZH', domain='datamind.ai',
                 linkedin='https://linkedin.com/company/datamind', industry='Data & AI',
                 location='Hyderabad', desc='AI-first analytics firm delivering predictive intelligence.'),
            dict(email='jobs@cloudedge.com',   password='org123', name='CloudEdge Systems',
                 company='CloudEdge Systems',   gst='07AABCE1234N1ZI', domain='cloudedge.com',
                 linkedin='https://linkedin.com/company/cloudedge', industry='Cloud Computing',
                 location='Mumbai', desc='Cloud-native infrastructure and DevOps consulting.'),
            dict(email='studio@designhub.in',  password='org123', name='DesignHub Studio',
                 company='DesignHub Studio',    gst='29AABCD9988P1ZJ', domain='designhub.in',
                 linkedin='https://linkedin.com/company/designhub', industry='Design',
                 location='Pune', desc='Award-winning UX/UI design studio for mobile and web.'),
            dict(email='recruit@securenet.co', password='org123', name='SecureNet Technologies',
                 company='SecureNet Technologies', gst='06AABCS3344Q1ZK', domain='securenet.co',
                 linkedin='https://linkedin.com/company/securenet', industry='Cybersecurity',
                 location='Chennai', desc='Cybersecurity solutions for enterprise and government.'),
            dict(email='team@innostartup.in',  password='org123', name='InnoStartup Labs',
                 company='InnoStartup Labs',    gst='19AABCI7755R1ZL', domain='innostartup.in',
                 linkedin='https://linkedin.com/company/innostartup', industry='Startup',
                 location='Delhi', desc='Early-stage startup incubator specializing in EdTech and FinTech.'),
        ]

        org_objects = {}
        for o in orgs_data:
            user = User.query.filter_by(email=o['email']).first()
            if not user:
                user = User(email=o['email'], name=o['name'],
                            password=generate_password_hash(o['password']), role='organization')
                db.session.add(user)
                db.session.flush()
                org = Organization(
                    user_id=user.id, company_name=o['company'], gst_number=o['gst'],
                    domain_email=o['domain'], linkedin_profile=o['linkedin'],
                    industry=o['industry'], location=o['location'], description=o['desc'],
                    is_verified=True, verification_status='approved',
                )
                db.session.add(org)
                db.session.flush()
                print(f'  ✅ Org: {o["company"]}')
            else:
                org = Organization.query.filter_by(user_id=user.id).first()
                print(f'  ⏭️  Org exists: {o["company"]}')
            org_objects[o['company']] = org

        db.session.commit()

        # ── 2. INTERNSHIPS (Dynamic ~200 count) ───────────────────────────
        import random
        
        job_titles_skills = [
            ('Full Stack Web Development Intern', 'React, Node.js, JavaScript, HTML, CSS, REST API, Git'),
            ('Backend Engineer Intern', 'Python, Flask, PostgreSQL, REST API, Docker, Git'),
            ('Mobile App Development Intern', 'React Native, JavaScript, Firebase, REST API, Git'),
            ('AI / Data Science Intern', 'Python, Machine Learning, Pandas, NumPy, Scikit-learn, SQL'),
            ('Data Analyst Intern', 'SQL, Python, Tableau, Excel, Statistics, Data Visualization'),
            ('Machine Learning Research Intern', 'Python, TensorFlow, PyTorch, Deep Learning, NLP, Computer Vision'),
            ('Cloud Infrastructure Intern', 'AWS, Azure, Docker, Kubernetes, Linux, Terraform, Python'),
            ('DevOps Engineer Intern', 'CI/CD, Jenkins, Git, Docker, Python, Linux, Bash'),
            ('UI/UX Design Intern', 'Figma, Adobe XD, User Research, Prototyping, HTML, CSS'),
            ('Graphic Design Intern', 'Adobe Illustrator, Photoshop, Figma, Typography, Branding'),
            ('Cybersecurity Analyst Intern', 'Network Security, Python, Linux, Penetration Testing, SIEM, Firewalls'),
            ('Ethical Hacking Intern', 'Python, Kali Linux, OWASP, Burp Suite, Network Security, CTF'),
            ('Product Management Intern', 'Product Roadmap, Agile, Scrum, User Stories, Market Research, SQL'),
            ('Growth Marketing Intern', 'Digital Marketing, SEO, Content Writing, Analytics, Social Media'),
            ('Business Development Intern', 'Sales, Communication, CRM, Excel, Market Research, Presentation'),
            ('Software Testing Intern', 'Selenium, Java, Python, Manual Testing, Automated Testing, QA'),
            ('Data Engineering Intern', 'Apache Spark, Hadoop, Python, SQL, ETL, Airflow'),
            ('Frontend Developer Intern', 'Vue.js, React, HTML5, CSS3, JavaScript, Tailwind CSS'),
            ('Cloud Security Intern', 'AWS Security, IAM, CloudTrail, Azure Policy, Network Security'),
            ('Blockchain Developer Intern', 'Solidity, Ethereum, Web3.js, Smart Contracts, Crypto'),
        ]
        
        locations = ['Bangalore', 'Hyderabad', 'Mumbai', 'Pune', 'Chennai', 'Delhi', 'Remote', 'Noida', 'Gurugram', 'Kolkata']
        durations = ['2 months', '3 months', '6 months']
        stipends = ['10000', '12000', '15000', '18000', '20000', '25000', '30000', '8000']

        all_orgs = Organization.query.all()
        # Ensure we have at least 200 jobs by generating them based on random choices
        if all_orgs:
            for i in range(200):
                org = random.choice(all_orgs)
                job = random.choice(job_titles_skills)
                # To allow the same title in the same org, append a varying identifier if needed, or simply let filter_by catch duplicates
                # But to reach 200, we might need unique titles if the combination (org, title) happens to collide often.
                # Since we have ~60+ orgs and 20 titles, 1200 possible combinations, collisions shouldn't limit us too much.
                
                title = f"{job[0]} {random.choice(['I', 'II', 'III']) if random.random() > 0.7 else ''}".strip()
                skills = job[1]
                capacity = random.randint(2, 8)
                location = random.choice(locations)
                duration = random.choice(durations)
                stipend = random.choice(stipends)
                
                existing = Internship.query.filter_by(
                    organization_id=org.id, title=title).first()
                if not existing:
                    intern = Internship(
                        organization_id=org.id, title=title,
                        skills_required=skills, capacity=capacity,
                        location=location, duration=duration,
                        stipend=stipend, status='approved',
                    )
                    db.session.add(intern)
            print("  ✅ Seeded ~200 Internships.")

        db.session.commit()

        # ── 3. STUDENTS (Dynamic ~150 count) ───────────────────────────────
        import random
        
        first_names = ['Amit', 'Anjali', 'Arjun', 'Divya', 'Karan', 'Kriti', 'Neha', 'Pooja', 'Rahul', 'Rohan', 'Sneha', 'Vikram', 'Aditi', 'Siddharth', 'Riya', 'Karthik', 'Manisha', 'Nitin', 'Meera', 'Ravi']
        last_names = ['Sharma', 'Verma', 'Gupta', 'Kumar', 'Singh', 'Patel', 'Das', 'Reddy', 'Joshi', 'Mehta', 'Nair', 'Iyer', 'Desai', 'Rao', 'Chauhan', 'Menon', 'Pillai', 'Rajan', 'Kapoor', 'Tiwari']
        skill_sets = [
            'Python, Machine Learning, SQL, Data Analysis, NumPy, Pandas',
            'React, JavaScript, HTML, CSS, Node.js, Git, REST API',
            'Python, TensorFlow, Deep Learning, Computer Vision, OpenCV',
            'AWS, Docker, Linux, Python, Kubernetes, CI/CD, Terraform',
            'Figma, Adobe XD, UI/UX Design, Prototyping, User Research, CSS',
            'Cybersecurity, Python, Linux, Network Security, Penetration Testing',
            'Java, Spring Boot, SQL, REST API, Git, Microservices, Docker',
            'Python, Flask, Django, PostgreSQL, REST API, Redis, Docker',
            'React Native, JavaScript, Firebase, Git, REST API, Redux',
            'Data Analysis, Python, SQL, Tableau, Excel, Statistics, Power BI',
            'C++, Data Structures, Algorithms, Problem Solving, OOP',
            'Go, C, Embedded Systems, Linux Kernel, Microcontrollers',
            'Ruby, Go, Microservices, Docker, Kubernetes, AWS',
            'Salesforce, CRM, Apex, SOQL, Data Management',
            'SEO, Digital Marketing, Google Analytics, Content Strategy',
        ]
        
        stu_locations = ['Bangalore', 'Hyderabad', 'Mumbai', 'Pune', 'Chennai', 'Delhi', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Noida']

        # Ensure we have ~150 students
        student_emails = []
        student_pwd_hash = generate_password_hash('student123')
        
        for i in range(150):
            fname = random.choice(first_names)
            lname = random.choice(last_names)
            email = f"student{i+1}_{fname.lower()}@student.com"
            student_emails.append(email)
            name = f"{fname} {lname}"
            loc = random.choice(stu_locations)
            skills = random.choice(skill_sets)
            
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(email=email, name=name,
                            password=student_pwd_hash, role='student')
                db.session.add(user)
                db.session.flush()
                profile = StudentProfile(user_id=user.id, skills=skills, location=loc)
                db.session.add(profile)
        
        db.session.commit()
        print("  ✅ Seeded ~150 Students.")

        # Re-fetch profiles cleanly
        all_student_users = User.query.filter_by(role='student').all()
        student_profiles = {}
        for u in all_student_users:
            p = StudentProfile.query.filter_by(user_id=u.id).first()
            student_profiles[u.email] = (u, p)

        # ── 4. CERTIFICATES ────────────────────────────────────────────────
        certs_data = [
            ('alice@student.com',  'AWS Certified Cloud Practitioner', 'Amazon Web Services',
             date(2023, 6, 15), date(2026, 6, 15)),
            ('alice@student.com',  'Google Data Analytics Certificate', 'Google',
             date(2023, 9, 20), None),
            ('bob@student.com',    'Meta Front-End Developer Certificate', 'Meta',
             date(2023, 7, 10), None),
            ('carol@student.com',  'TensorFlow Developer Certificate', 'Google',
             date(2023, 11, 5), date(2026, 11, 5)),
            ('david@student.com',  'AWS Solutions Architect – Associate', 'Amazon Web Services',
             date(2023, 8, 22), date(2026, 8, 22)),
            ('david@student.com',  'Certified Kubernetes Administrator (CKA)', 'CNCF',
             date(2024, 1, 10), date(2027, 1, 10)),
            ('emma@student.com',   'Google UX Design Certificate', 'Google',
             date(2023, 5, 30), None),
            ('frank@student.com',  'CompTIA Security+', 'CompTIA',
             date(2023, 7, 18), date(2026, 7, 18)),
            ('frank@student.com',  'Certified Ethical Hacker (CEH)', 'EC-Council',
             date(2024, 2, 14), date(2027, 2, 14)),
            ('grace@student.com',  'Oracle Java SE Programmer', 'Oracle',
             date(2023, 10, 5), date(2026, 10, 5)),
            ('henry@student.com',  'Django REST Framework Certification', 'Udemy',
             date(2023, 12, 12), None),
            ('irene@student.com',  'React Native Specialist', 'Coursera',
             date(2024, 1, 20), None),
            ('james@student.com',  'Tableau Desktop Specialist', 'Tableau',
             date(2023, 9, 8), date(2026, 9, 8)),
            ('james@student.com',  'Microsoft Power BI Data Analyst', 'Microsoft',
             date(2024, 3, 1), date(2027, 3, 1)),
            ('bob@student.com',    'JavaScript Algorithms & Data Structures', 'freeCodeCamp',
             date(2023, 6, 25), None),
            ('carol@student.com',  'Deep Learning Specialization', 'Coursera / DeepLearning.AI',
             date(2023, 8, 15), None),
        ]

        for email, cert_name, issuer, issue_dt, expiry_dt in certs_data:
            user, _ = student_profiles.get(email, (None, None))
            if not user:
                continue
            existing = StudentCertificate.query.filter_by(
                user_id=user.id, certificate_name=cert_name).first()
            if not existing:
                c = StudentCertificate(user_id=user.id, certificate_name=cert_name,
                    issuing_organization=issuer, issue_date=issue_dt, expiry_date=expiry_dt)
                db.session.add(c)
                print(f'  ✅ Cert: {cert_name} → {email}')
            else:
                print(f'  ⏭️  Cert exists: {cert_name}')

        db.session.commit()

        # ── 5. EXPERIENCES ────────────────────────────────────────────────
        experiences_data = [
            ('alice@student.com',  'InfoSys BPM', 'Data Science Intern',
             date(2023, 5, 1), date(2023, 8, 31), 'Bangalore', '12000',
             'Python, SQL, Data Visualization', 'Built sales dashboards and ML models for churn prediction.'),
            ('bob@student.com',    'Wipro Digital', 'Frontend Intern',
             date(2023, 6, 1), date(2023, 9, 30), 'Hyderabad', '10000',
             'React, CSS, JavaScript', 'Developed responsive UI components for client web portals.'),
            ('carol@student.com',  'NVIDIA AI Labs', 'ML Research Intern',
             date(2023, 7, 1), date(2023, 12, 31), 'Bangalore', '25000',
             'Python, PyTorch, Computer Vision', 'Researched object detection models for autonomous drones.'),
            ('david@student.com',  'HCL Cloud Services', 'Cloud Operations Intern',
             date(2023, 5, 15), date(2023, 9, 15), 'Mumbai', '15000',
             'AWS, Linux, Docker', 'Managed cloud infrastructure and automated deployment pipelines.'),
            ('frank@student.com',  'Qualys', 'Security Analyst Intern',
             date(2023, 6, 1), date(2023, 11, 30), 'Chennai', '14000',
             'Penetration Testing, Python, SIEM', 'Conducted vulnerability assessments and security audits.'),
            ('emma@student.com',   'Zomato', 'UX Design Intern',
             date(2023, 3, 1), date(2023, 6, 30), 'Pune', '11000',
             'Figma, User Research, Prototyping', 'Redesigned the restaurant partner onboarding flow.'),
        ]

        for email, company, role, start, end, loc, stipend, skills, desc in experiences_data:
            user, _ = student_profiles.get(email, (None, None))
            if not user:
                continue
            existing = StudentInternshipExperience.query.filter_by(
                user_id=user.id, company_name=company).first()
            if not existing:
                e = StudentInternshipExperience(
                    user_id=user.id, company_name=company, role=role,
                    start_date=start, end_date=end, location=loc,
                    stipend=stipend, skills_used=skills, work_description=desc,
                )
                db.session.add(e)
                print(f'  ✅ Experience: {role} @ {company} → {email}')
            else:
                print(f'  ⏭️  Experience exists: {role} @ {company}')

        db.session.commit()

        # ── 6. APPLICATIONS (Dynamic Applications Generation) ────────────────
        all_internships = Internship.query.filter_by(status='approved').all()
        # Separate out targeted company internships if we want them specifically applied to
        target_company_emails = ['jobs@cognizant.com', 'careers@hdfcbank.com', 'hr@ltimindtree.com', 'recruit@zoho.com', 'hr@sunpharma.com']
        target_org_ids = [org.id for org in Organization.query.join(User, Organization.user_id == User.id).filter(User.email.in_(target_company_emails)).all()]
        
        target_internships = [i for i in all_internships if i.organization_id in target_org_ids]
        other_internships = [i for i in all_internships if i.organization_id not in target_org_ids]
        
        all_profiles = StudentProfile.query.all()
        
        if all_internships and all_profiles:
            statuses = ['pending', 'approved', 'rejected']
            added_apps = 0
            
            for profile in all_profiles:
                # Decide how many internships this student applies to (1 to 5)
                num_apps = random.randint(1, 5)
                
                # Biasing towards targeted internships
                chosen_internships = []
                if target_internships and random.random() > 0.3: # 70% chance to apply to at least one target company
                    chosen_internships.append(random.choice(target_internships))
                    
                # Pick remaining from either target or others
                remaining = num_apps - len(chosen_internships)
                if remaining > 0:
                    pool = target_internships + other_internships
                    chosen_internships.extend(random.choices(pool, k=remaining))
                
                # Make unique
                chosen_internships = list(set(chosen_internships))
                
                for intern in chosen_internships:
                    existing = Application.query.filter_by(student_id=profile.id, internship_id=intern.id).first()
                    if not existing:
                        a = Application(student_id=profile.id, internship_id=intern.id, status=random.choice(statuses))
                        db.session.add(a)
                        added_apps += 1
                        
            print(f"  ✅ Seeded {added_apps} Applications.")
        
        db.session.commit()

        # ── SUMMARY ────────────────────────────────────────────────────────
        print('\n' + '='*52)
        print(f'  Users:        {User.query.count()}')
        print(f'  Organizations:{Organization.query.count()}')
        print(f'  Internships:  {Internship.query.count()}')
        print(f'  Students:     {StudentProfile.query.count()}')
        print(f'  Certificates: {StudentCertificate.query.count()}')
        print(f'  Experiences:  {StudentInternshipExperience.query.count()}')
        print(f'  Applications: {Application.query.count()}')
        print('='*52)
        print('  Seed complete!')


if __name__ == '__main__':
    seed()
