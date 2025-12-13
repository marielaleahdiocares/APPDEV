from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'Satisbank@9'

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "satisbank"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"	
mysql=MySQL(app)
    

bank_data = [
    {
        "name": "Bank of the Philippine Islands",
        "logo_url": "bpi_logo.png",
        "reliability": 96,
        "satisfaction": 86,
        "efficiency": 97,
        "safety": 85
    },
    {
        "name": "Land Bank of the Philippines",
        "logo_url": "landbank_logo.png",
        "reliability": 97,
        "satisfaction": 85,
        "efficiency": 97,
        "safety": 88
    },
    # ... include all 10 banks shown in the image with their respective data
]

faq_data = {
    "account": [
        {"id":"create-account","question":"How can I create an account?","answer":"To create an account, click Sign Up on the homepage and follow the registration form. Provide your valid ID and verify your email."},
        {"id":"reset-password","question":"How do I reset my password?","answer":"Click \"Forgot Password\" on the login page. Enter your registered email; you will receive a reset link. Follow the link to set a new password."},
        {"id":"cant-login","question":"What should I do if I can’t log in?","answer":"Double-check your email and password. If you still can't log in, use Forgot Password or contact support at support@satisbank.com."}
    ],
    "bank-info": [
        {"id":"compare-banks","question":"How can I compare banks?","answer":"Use the Comparison page: pick the banks you want and view a side-by-side comparison of fees, interest rates, and features."},
        {"id":"bank-fees","question":"Where can I see bank fees and charges?","answer":"Fees and charges are listed on each bank's profile page under 'Fees & Charges' section."}
    ],
    "savings-loans": [
        {"id":"loan-app","question":"How do I apply for a loan?","answer":"Open the Loans area inside the bank profile, choose the product, complete the online application and submit required documents."},
        {"id":"savings-interest","question":"How are savings interest rates calculated?","answer":"Interest depends on the product, balance, and bank policy. Check the product page for computed APY details."}
    ],
    "dashboard": [
        {"id":"dashboard-use","question":"How do I customize my dashboard?","answer":"Go to Dashboard settings and choose widgets to show/hide, reorder sections, and save your preferred layout."}
    ],
    "security": [
        {"id":"security-info","question":"How secure is my personal information?","answer":"We use TLS encryption, secure servers, and strict access controls. Sensitive data is stored encrypted and access is audited."}
    ],
}

# Flatten lookup map id -> faq item
faq_lookup = {}
for cat, items in faq_data.items():
    for it in items:
        faq_lookup[it["id"]] = {"category": cat, **it}

# Category metadata (used for cards)
categories_meta = [
    {"key":"account","title":"Account & Login","icon":"fa-user"},
    {"key":"bank-info","title":"Bank Information","icon":"fa-university"},
    {"key":"savings-loans","title":"Savings & Loans","icon":"fa-piggy-bank"},
    {"key":"dashboard","title":"Dashboard","icon":"fa-th-large"},
    {"key":"security","title":"Security & Privacy","icon":"fa-shield-alt"},
]


@app.route("/")
def splash():
    return render_template("splash.html")

@app.route('/home')
def home():
    if 'user_email' not in session:
        return redirect(url_for('landing'))

    # Fetch user data from database
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT firstName, lastName, email
        FROM user
        WHERE email = %s
    """, (session['user_email'],))
    user_data = cur.fetchone()
    cur.close()

    if not user_data:
        return redirect(url_for('landing'))

    # Pass the whole user_data dictionary to the template
    return render_template('menu.html', user=user_data)


@app.route('/landing')
def landing():
    # Render the HTML template, passing a title variable
    return render_template('landing.html', page_title="Modern Banking Landing Page")

@app.route('/guest-dashboard')
def guest_dashboard():
    return render_template('guest_dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template('login.html')

        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT firstName, lastName, email, password
            FROM user
            WHERE email = %s
        """, (email,))
        user = cur.fetchone()
        cur.close()

        if not user:
            flash("Invalid email or password.", "danger")
            return render_template('login.html')

        stored_pw = user['password']
        is_valid = False

        try:
            if check_password_hash(stored_pw, password):
                is_valid = True
        except ValueError:
            pass

        if stored_pw == password:
            is_valid = True

        if not is_valid:
            flash("Invalid email or password.", "danger")
            return render_template('login.html')

        # SUCCESS
        session['user_email'] = user['email']
        flash(f"Welcome back, {user['firstName']}!", "success")
        return redirect(url_for('home'))

    return render_template('login.html')



@app.route('/register/step1', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':

        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        contact = request.form.get('contact')
        address = request.form.get('address')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('create_account'))

        session['reg_data'] = {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "ContactNo": contact,
            "Address": address,
            "password": password 
        }

        return redirect(url_for('user_type'))

    # GET: restore saved data
    reg = session.get('reg_data', {})

    return render_template(
        'create_account.html',
        step=1,
        firstName_value=reg.get('firstName', ''),
        lastName_value=reg.get('lastName', ''),
        email_value=reg.get('email', ''),
        contact_value=reg.get('ContactNo', ''),
        address_value=reg.get('Address', '')
    )



# Step 2: Tell Us About Yourself (User Type)
@app.route('/register/step2', methods=['GET', 'POST'])
def user_type():

    # If step1 was not completed
    if 'reg_data' not in session:
        return redirect(url_for('create_account'))

    if request.method == 'POST':
        user_type = request.form.get('user_type')

        session['reg_data']['user_type'] = user_type
        session.modified = True   # <-- REQUIRED

        if user_type == 'existing':
            return redirect(url_for('survey_bank'))
        
        return redirect(url_for('survey_interest'))

    selected_type = session['reg_data'].get('user_type', 'prospective')
    return render_template('user_type.html', step=2, selected_type=selected_type)


# Step 3.1 (Existing Clients): Banks Currently Used
@app.route('/register/step3/banks', methods=['GET', 'POST'])
def survey_bank():
    if request.method == 'POST':
        # Store selected banks in session (form.getlist for multiple checkboxes)
        session['reg_data']['banks_used'] = request.form.getlist('bank')
        session.modified = True

        return redirect(url_for('survey_interest'))
    
    # Pass the current step and sub-step for the progress indicators
    selected_banks = session.get('reg_data', {}).get('banks_used', [])
    return render_template('survey_bank.html', step=3, sub_step=1, selected_banks=selected_banks)


# Step 3.2: Services Interested In
@app.route('/register/step3/interest', methods=['GET', 'POST'])
def survey_interest():
    if request.method == 'POST':
        # Store selected services in session
        session['reg_data']['services_interested'] = request.form.getlist('service')
        session.modified = True
        return redirect(url_for('survey_preference'))
    
    selected_services = session.get('reg_data', {}).get('services_interested', [])
    back_url = url_for('survey_bank') if session.get('reg_data', {}).get('user_type') == 'existing' else url_for('user_type')
    return render_template('survey_interest.html', step=3, sub_step=2, back_url=back_url, selected_services=selected_services)

# Step 3.3: Banking Preferences (Mobile/In-Person) - Final Step
@app.route('/register/step3/preference', methods=['GET', 'POST'])
def survey_preference():
    if request.method == 'POST':

        if 'reg_data' not in session:
            flash("Please complete previous steps.", "danger")
            return redirect(url_for('create_account'))

        session['reg_data']['preference'] = request.form.get('preference')
        session.modified = True

        final_data = session.get('reg_data', {})

        customer_type = final_data.get('user_type')
        if not customer_type:
            flash("Customer type missing. Please complete Step 2.", "danger")
            return redirect(url_for('user_type'))

        # --- INSERT INTO DATABASE ---
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO user (firstName, lastName, email, password, ContactNo, Address, CustomerType)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            final_data.get('firstName'),
            final_data.get('lastName'),
            final_data.get('email'),
            final_data.get('password'),
            final_data.get('ContactNo'),
            final_data.get('Address'),
            customer_type
        ))
        mysql.connection.commit()

        # --- CLEAR SESSION AFTER SUCCESS ---
        session.pop('reg_data', None)

        session['user_email'] = final_data.get('email')
        flash("Account created successfully!", "success")
        return redirect(url_for('home'))

    selected_pref = session['reg_data'].get('preference', '')
    return render_template('survey_preference.html', step=3, sub_step=3, selected_pref=selected_pref)





@app.route('/comparison')
def comparison():
     if 'user_email' not in session:
        return redirect(url_for('login'))
     return render_template('comparison.html', user=session['user_email'])


@app.route('/reco')
def reco():
     if 'user_email' not in session:
        return redirect(url_for('login'))
     return render_template('reco.html', user=session['user_email'])


@app.route('/analysis')
def analysis():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT firstName, lastName
        FROM user
        WHERE email = %s
    """, (session['user_email'],))

    user_data = cur.fetchone()

    cur.close()

    if not user_data:
        return redirect(url_for('login'))

    return render_template("analysis.html", user=user_data)



@app.route('/bprofile')
def bprofile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT firstName, lastName
        FROM user
        WHERE email = %s
    """, (session['user_email'],))

    user_data = cur.fetchone()

    cur.close()

    if not user_data:
        return redirect(url_for('login'))

    return render_template("bprofile.html", user=user_data)


@app.route('/bdo_profile')
def bdo_profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    bank_data = {
        "name": "BDO",
        "full_name": "Banco de Oro Unibank, Inc.",
        "description": "BDO is one of the largest banks in the Philippines offering comprehensive financial services.",
        "rating_metrics": {
            "Satisfaction": 8,
            "Service Quality": 7,
            "Safety Rating": 9
        },
        "interest_rate": {
            "Savings": 0.10,
            "Time Deposit": 1.25,
            "Checking": 0.0
        },
        "key_features": [
            "Largest branch network",
            "Wide ATM availability",
            "Reliable customer support",
            "Strong digital banking"
        ]
    }
    service_ratings = {
        "labels": ["Loans", "Customer Service", "Mobile App", "ATM Availability"],
        "data": [8, 7, 6, 9],
        "max": 10
    }
    satisfaction_breakdown = {
        "labels": ["Speed", "Convenience", "Support", "Security", "Accessibility"],
        "data": [8, 7, 7, 9, 8],
        "max": 10
    }
    return render_template('banks/bdo_profile.html', user=session['user_email'], bank_data=bank_data, service_ratings=service_ratings, satisfaction_breakdown=satisfaction_breakdown)

@app.route('/cbank_profile')
def cbank_profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    # China Bank Data
    bank_data = {
        "name": "China Bank",
        "full_name": "China Banking Corporation",
        "description": "China Bank is one of the oldest private banks in the Philippines, known for strong financial stability and customer-focused services.",
        
        "rating_metrics": {
            "Satisfaction": 7,
            "Service Quality": 8,
            "Safety Rating": 9
        },

        "interest_rate": {
            "Savings": 0.25,
            "Time Deposit": 1.50,
            "Checking": 0.10
        },

        "key_features": [
            "Strong financial stability",
            "Excellent customer support",
            "Fast loan processing",
            "Trusted old banking institution",
            "Reliable over-the-counter transactions"
        ]
    }
    # Chart: Service Ratings
    service_ratings = {
        "labels": ["Customer Service", "Mobile Banking", "Loan Services", "ATM Availability"],
        "data": [8, 6, 9, 7],
        "max": 10
    }
    # Chart: Satisfaction Breakdown
    satisfaction_breakdown = {
        "labels": ["Speed", "Convenience", "Security", "Services", "Support"],
        "data": [7, 8, 9, 8, 7],
        "max": 10
    }
    return render_template('banks/cbank_profile.html', user=session['user_email'], bank_data=bank_data, service_ratings=service_ratings, satisfaction_breakdown=satisfaction_breakdown)

@app.route('/pnb_profile')
def pnb_profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    # PNB Bank Data
    bank_data = {
        "name": "PNB",
        "full_name": "Philippine National Bank",
        "description": "PNB is one of the oldest and most established banks in the Philippines, known for its wide network, overseas presence, and strong financial stability.",

        "rating_metrics": {
            "Satisfaction": 7,
            "Service Quality": 7,
            "Safety Rating": 8
        },

        "interest_rate": {
            "Savings": 0.10,
            "Time Deposit": 1.25,
            "Checking": 0.05
        },

        "key_features": [
            "Strong international remittance network",
            "Wide branch coverage nationwide",
            "Over 100 years in Philippine banking",
            "Trusted for overseas Filipino services",
            "Stable and secure banking operations"
        ]
    }
    # Services Ratings
    service_ratings = {
        "labels": ["Customer Service", "Mobile Banking", "Remittance", "ATM Availability"],
        "data": [7, 6, 9, 7],
        "max": 10
    }
    # Satisfaction Breakdown
    satisfaction_breakdown = {
        "labels": ["Speed", "Convenience", "Security", "Support", "Accessibility"],
        "data": [6, 7, 8, 7, 8],
        "max": 10
    }
    return render_template('banks/pnb_profile.html', user=session['user_email'], bank_data=bank_data, service_ratings=service_ratings, satisfaction_breakdown=satisfaction_breakdown)

@app.route('/eastwest_profile')
def eastwest_profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    # EastWest Bank Data
    bank_data = {
        "name": "EastWest",
        "full_name": "EastWest Banking Corporation",
        "description": "EastWest Bank is known for its strong retail banking presence, competitive loan offerings, and user-friendly digital banking solutions.",

        "rating_metrics": {
            "Satisfaction": 7,
            "Service Quality": 7,
            "Safety Rating": 8
        },

        "interest_rate": {
            "Savings": 0.15,
            "Time Deposit": 1.30,
            "Checking": 0.05
        },

        "key_features": [
            "Competitive loan products",
            "User-friendly mobile banking",
            "Good customer support",
            "Affordable credit card rates",
            "Growing branch and ATM network"
        ]
    }

    # Services Ratings (Bar Chart)
    service_ratings = {
        "labels": ["Mobile App", "Customer Service", "Loans", "ATM Network"],
        "data": [7, 7, 8, 6],
        "max": 10
    }

    # Satisfaction Breakdown (Radar Chart)
    satisfaction_breakdown = {
        "labels": ["Speed", "Convenience", "Security", "Support", "Reliability"],
        "data": [7, 7, 8, 7, 7],
        "max": 10
    }
    return render_template('banks/eastwest_profile.html', user=session['user_email'], bank_data=bank_data, service_ratings=service_ratings, satisfaction_breakdown=satisfaction_breakdown)

@app.route('/secbank_profile')
def secbank_profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    # Security Bank Data
    bank_data = {
        "name": "Security Bank",
        "full_name": "Security Bank Corporation",
        "description": "Security Bank is known for customer-focused services, competitive interest rates, and strong digital banking performance.",

        "rating_metrics": {
            "Satisfaction": 8,
            "Service Quality": 8,
            "Safety Rating": 9
        },

        "interest_rate": {
            "Savings": 0.25,
            "Time Deposit": 1.40,
            "Checking": 0.10
        },

        "key_features": [
            "Award-winning customer service",
            "Competitive loan and credit card products",
            "Strong digital banking features",
            "Wide ATM network",
            "Fast account opening"
        ]
    }

    # Services Ratings
    service_ratings = {
        "labels": ["Mobile App", "Customer Service", "Loans", "ATM Network"],
        "data": [8, 9, 8, 7],
        "max": 10
    }

    # Satisfaction Breakdown
    satisfaction_breakdown = {
        "labels": ["Speed", "Convenience", "Security", "Support", "Reliability"],
        "data": [8, 8, 9, 9, 8],
        "max": 10
    }
    return render_template('banks/secbank_profile.html', user=session['user_email'], bank_data=bank_data, service_ratings=service_ratings, satisfaction_breakdown=satisfaction_breakdown)

@app.route('/metrobank_profile')
def metrobank_profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    # Metrobank Data
    bank_data = {
        "name": "Metrobank",
        "full_name": "Metropolitan Bank & Trust Company",
        "description": "Metrobank is one of the largest Philippine banks, known for strong financial services, stability, and broad nationwide coverage.",

        "rating_metrics": {
            "Satisfaction": 8,
            "Service Quality": 9,
            "Safety Rating": 9
        },

        "interest_rate": {
            "Savings": 0.25,
            "Time Deposit": 1.50,
            "Checking": 0.10
        },

        "key_features": [
            "Wide branch and ATM network",
            "Reliable mobile and online banking",
            "Strong loan and credit card offerings",
            "High trust and safety rating",
            "Fast over-the-counter services"
        ]
    }

    # Services Ratings
    service_ratings = {
        "labels": ["Mobile App", "Customer Service", "Loans", "ATM Network"],
        "data": [8, 9, 9, 8],
        "max": 10
    }

    # Satisfaction Breakdown
    satisfaction_breakdown = {
        "labels": ["Speed", "Convenience", "Security", "Support", "Reliability"],
        "data": [8, 9, 9, 9, 8],
        "max": 10
    }
    return render_template('banks/metrobank_profile.html', user=session['user_email'], bank_data=bank_data, service_ratings=service_ratings, satisfaction_breakdown=satisfaction_breakdown)

@app.route('/rcbc_profile')
def rcbc_profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    # RCBC Bank Data
    bank_data = {
        "name": "RCBC",
        "full_name": "Rizal Commercial Banking Corporation",
        "description": "RCBC is known for innovative digital banking, strong customer service, and competitive savings and loan products.",

        "rating_metrics": {
            "Satisfaction": 8,
            "Service Quality": 8,
            "Safety Rating": 9
        },

        "interest_rate": {
            "Savings": 0.30,
            "Time Deposit": 1.60,
            "Checking": 0.10
        },

        "key_features": [
            "Award-winning digital banking (RCBC Digital)",
            "Fast money transfers and QR payments",
            "Strong customer support",
            "Competitive personal and business loans",
            "High security and reliability"
        ]
    }

    # Services Ratings
    service_ratings = {
        "labels": ["Mobile App", "Customer Service", "Loans", "ATM Network"],
        "data": [9, 8, 8, 7],
        "max": 10
    }

    # Satisfaction Breakdown
    satisfaction_breakdown = {
        "labels": ["Speed", "Convenience", "Security", "Support", "Reliability"],
        "data": [8, 9, 9, 8, 8],
        "max": 10
    }
    return render_template('banks/rcbc_profile.html', user=session['user_email'], bank_data=bank_data, service_ratings=service_ratings, satisfaction_breakdown=satisfaction_breakdown)

@app.route('/boc_profile')
def boc_profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    # BANK OF COMMERCE DATA
    bank_data = {
        "name": "BankCom",
        "full_name": "Bank of Commerce",
        "description": "Bank of Commerce is known for its dependable banking services, corporate solutions, and expanding digital banking capabilities.",

        "rating_metrics": {
            "Satisfaction": 7,
            "Service Quality": 7,
            "Safety Rating": 8
        },

        "interest_rate": {
            "Savings": 0.20,
            "Time Deposit": 1.40,
            "Checking": 0.05
        },

        "key_features": [
            "Strong corporate banking services",
            "Improved digital banking platform",
            "Stable and secure bank operations",
            "Nationwide branch presence",
            "Competitive loan products"
        ]
    }

    # SERVICES RATINGS
    service_ratings = {
        "labels": ["Mobile App", "Customer Service", "Loans", "ATM Network"],
        "data": [6, 7, 8, 7],
        "max": 10
    }

    # SATISFACTION BREAKDOWN
    satisfaction_breakdown = {
        "labels": ["Speed", "Convenience", "Security", "Support", "Reliability"],
        "data": [7, 7, 8, 7, 7],
        "max": 10
    }
    return render_template('banks/boc_profile.html', user=session['user_email'], bank_data=bank_data, service_ratings=service_ratings, satisfaction_breakdown=satisfaction_breakdown)

@app.route('/landbank_profile')
def landbank_profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    # LANDBANK DATA
    bank_data = {
        "name": "Landbank",
        "full_name": "Land Bank of the Philippines",
        "description": "Landbank is a government-owned bank focused on serving farmers, rural communities, and public-sector clients while expanding digital banking services.",

        "rating_metrics": {
            "Satisfaction": 7,
            "Service Quality": 7,
            "Safety Rating": 9
        },

        "interest_rate": {
            "Savings": 0.15,
            "Time Deposit": 1.40,
            "Checking": 0.05
        },

        "key_features": [
            "Strong government partnerships",
            "Loans for agriculture and SMEs",
            "Wide rural branch presence",
            "Secure digital banking",
            "Public-service-focused programs"
        ]
    }

    # SERVICES RATINGS
    service_ratings = {
        "labels": ["Mobile App", "Customer Service", "Loans", "ATM Network"],
        "data": [6, 7, 8, 8],
        "max": 10
    }

    # SATISFACTION BREAKDOWN
    satisfaction_breakdown = {
        "labels": ["Speed", "Convenience", "Security", "Support", "Reliability"],
        "data": [7, 6, 9, 7, 8],
        "max": 10
    }
    return render_template('banks/landbank_profile.html', user=session['user_email'], bank_data=bank_data, service_ratings=service_ratings, satisfaction_breakdown=satisfaction_breakdown)

@app.route('/bpiprofile')
def bpiprofile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    # BPI DATA
    bank_data = {
        "name": "BPI",
        "full_name": "Bank of the Philippine Islands",
        "description": "BPI is one of the oldest and most trusted banks in the Philippines, known for strong digital banking, stability, and a large nationwide network.",

        "rating_metrics": {
            "Satisfaction": 8,
            "Service Quality": 9,
            "Safety Rating": 9
        },

        "interest_rate": {
            "Savings": 0.10,
            "Time Deposit": 1.25,
            "Checking": 0.00
        },

        "key_features": [
            "Strong Digital Banking",
            "Large ATM and Branch Network",
            "Secure Mobile Banking App",
            "Wide Range of Loan Products",
            "International Banking Support"
        ]
    }

    # SERVICES RATINGS (Bar Chart)
    service_ratings = {
        "labels": ["Mobile App", "Customer Service", "Loans", "ATM Network"],
        "data": [9, 8, 8, 9],
        "max": 10
    }

    # SATISFACTION BREAKDOWN (Radar Chart)
    satisfaction_breakdown = {
        "labels": ["Speed", "Convenience", "Security", "Support", "Reliability"],
        "data": [9, 8, 9, 8, 9],
        "max": 10
    }
    return render_template('banks/bpiprofile.html', user=session['user_email'], bank_data=bank_data, service_ratings=service_ratings, satisfaction_breakdown=satisfaction_breakdown)

@app.route('/settings')
def settings():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html', user=session['user_email'])

from flask import request, session, redirect, url_for, render_template, flash

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Get updated data from form
        firstName = request.form.get('firstName')
        lastName  = request.form.get('lastName')
        contactNo = request.form.get('contactNo')
        address   = request.form.get('address')
        # If you want to allow email change:
        email     = request.form.get('email')  # optional

        # Update query — adjust table name ("user" or "users") as per your schema
        cur.execute("""
            UPDATE user
            SET firstName = %s,
                lastName  = %s,
                contactNo = %s,
                Address   = %s
            WHERE email = %s
        """, (firstName, lastName, contactNo, address, session['user_email']))
        mysql.connection.commit()
        # If you allow updating email:
        if email and email != session['user_email']:
            # Be careful: check for duplicates, etc.
            cur.execute("""
                UPDATE user
                SET email = %s
                WHERE email = %s
            """, (email, session['user_email']))
            mysql.connection.commit()
            session['user_email'] = email

        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))

    # On GET or after POST redirect: fetch user data
    cur.execute("SELECT firstName, lastName, email, contactNo, Address FROM user WHERE email = %s", 
                (session['user_email'],))
    user = cur.fetchone()
    cur.close()

    if not user:
        return redirect(url_for('login'))

    return render_template('profile.html', user=user)


@app.route('/references')
def references():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('references.html', user=session['user_email'])

@app.route('/savedBanks')
def savedBanks():
    # Pass the bank data to the HTML template
    return render_template('savedbanks.html', banks=bank_data)

@app.route("/help_center")
def help_center():
    return render_template("help_center.html", categories=categories_meta, faqs=faq_data)

@app.route("/category/<cat_key>")
def category_page(cat_key):
    items = faq_data.get(cat_key, [])
    meta = next((c for c in categories_meta if c["key"] == cat_key), {"title":cat_key})
    return render_template("category.html", category=meta, items=items, categories=categories_meta)

@app.route("/faq/<faq_id>")
def faq_answer(faq_id):
    faq = faq_lookup.get(faq_id)
    if not faq:
        return redirect(url_for('help_center'))
    return render_template("answer.html", faq=faq, categories=categories_meta)

@app.route("/search")
def search():
    q = request.args.get("q","").strip().lower()
    results = []
    if q:
        for cat, items in faq_data.items():
            for it in items:
                if q in it["question"].lower() or q in it["answer"].lower():
                    results.append({"category": cat, **it})
    return render_template("search_result.html", query=q, results=results, categories=categories_meta)


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
