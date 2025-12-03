from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# FAQ data grouped by category
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
    return render_template("search_results.html", query=q, results=results, categories=categories_meta)

if __name__ == "__main__":
    app.run(debug=True)
