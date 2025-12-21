from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "1234"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "bankComparison"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Optional: logo mapping (use your real filenames)
BANK_LOGOS = {
    "BDO": "images/BDO.jpg",
    "LANDBANK": "images/BDO.jpg",
    "METROBANK": "images/BDO.jpg",
    "BPI": "images/BDO.jpg",
    "PNB": "images/BDO.jpg",
    "CHINABANK": "images/BDO.jpg",
    "RCBC": "images/BDO.jpg",
    "SECB": "images/BDO.jpg",
    "EASTWEST": "images/BDO.jpg",
    "BOC": "images/BDO.jpg",
}

@app.route("/")
def index():
    return render_template("sidebar.html")

@app.route("/home")
def home():
    return render_template("sidebar.html")


# -------------------------------
# Page 1: Select banks
# -------------------------------
@app.route("/comparison", methods=["GET", "POST"])
def comparison():
    cur = mysql.connection.cursor()
    cur.execute("SELECT bank_code, bank_name FROM banks ORDER BY bank_name")
    all_banks = cur.fetchall()
    cur.close()

    # attach logos for template
    for b in all_banks:
        b["logo"] = BANK_LOGOS.get(b["bank_code"], "images/BDO.jpg")  # fallback

    if request.method == "POST":
        selected_codes = request.form.getlist("selected_banks")

        if len(selected_codes) < 2:
            return render_template("page1_select_banks.html", all_banks=all_banks)

        banks_csv = ",".join(selected_codes)
        return redirect(url_for("detailed_table_banks", banks=banks_csv))

    return render_template("page1_select_banks.html", all_banks=all_banks)


# -------------------------------
# Page 2: Detailed table (default)
# -------------------------------
@app.route("/compare")
def detailed_table():
    return render_template("page2_detailed_table.html", active_view="Detailed Table")


# -------------------------------
# Page 2: Detailed table for selected banks
# -------------------------------
@app.route("/compare/<banks>")
def detailed_table_banks(banks):
    selected_codes = [c.strip().upper() for c in banks.split(",") if c.strip()]
    if len(selected_codes) < 2:
        return redirect(url_for("comparison"))

    cur = mysql.connection.cursor()

    # Get selected bank details (for headers)
    placeholders = ",".join(["%s"] * len(selected_codes))
    cur.execute(
        f"""
        SELECT bank_id, bank_code, bank_name
        FROM banks
        WHERE bank_code IN ({placeholders})
        ORDER BY bank_name
        """,
        selected_codes
    )
    selected_banks = cur.fetchall()

    # ✅ Build table using service_type (description per bank per category)
    cur.execute(
        f"""
        SELECT
            c.category_id,
            c.category_name,
            b.bank_code,
            GROUP_CONCAT(DISTINCT st.description ORDER BY st.description SEPARATOR ', ') AS service_list
        FROM service_categories c
        JOIN banks b ON b.bank_code IN ({placeholders})
        LEFT JOIN service_type st
               ON st.category_id = c.category_id
              AND st.bank_id = b.bank_id
        GROUP BY c.category_id, c.category_name, b.bank_code
        ORDER BY c.category_id, b.bank_code
        """,
        selected_codes
    )
    raw = cur.fetchall()
    cur.close()

    # Pivot into: [{category_name, values:{BANKCODE: text}}]
    rows_map = {}
    for r in raw:
        cat = r["category_name"]
        bank_code = r["bank_code"]
        service_list = r["service_list"] if r["service_list"] else "N/A"

        if cat not in rows_map:
            rows_map[cat] = {"category_name": cat, "values": {}}

        rows_map[cat]["values"][bank_code] = service_list

    table_rows = list(rows_map.values())

    # Ensure every category row has every selected bank column
    for row in table_rows:
        for b in selected_banks:
            row["values"].setdefault(b["bank_code"], "N/A")

    return render_template(
        "page2_detailed_table.html",
        active_view="Detailed Table",
        banks=",".join(selected_codes),
        selected_banks=selected_banks,
        table_rows=table_rows
    )



# -------------------------------
# Placeholder tabs
# -------------------------------
@app.route("/financial-services")
def financial_services():
    # URL example: /financial-services?banks=BPI,BDO,RCBC
    banks_csv = request.args.get("banks", "")
    selected_codes = [c.strip().upper() for c in banks_csv.split(",") if c.strip()]

    if len(selected_codes) < 2:
        return redirect(url_for("comparison"))

    cur = mysql.connection.cursor()

    # Get selected banks (validated + sorted)
    placeholders = ",".join(["%s"] * len(selected_codes))
    cur.execute(
        f"""
        SELECT bank_id, bank_code, bank_name
        FROM banks
        WHERE bank_code IN ({placeholders})
        ORDER BY bank_name
        """,
        selected_codes
    )
    selected_banks = cur.fetchall()
    selected_codes = [b["bank_code"] for b in selected_banks]  # re-sync

    # Pull services + rates
    cur.execute(
        f"""
        SELECT
            c.category_id,
            c.category_name,
            s.service_id,
            s.service_name,
            b.bank_code,
            COALESCE(sr.rate_value, 'N/A') AS rate_value
        FROM service_categories c
        JOIN services s ON s.category_id = c.category_id
        JOIN banks b ON b.bank_code IN ({placeholders})
        LEFT JOIN service_rates sr
            ON sr.bank_id = b.bank_id
           AND sr.service_id = s.service_id
        ORDER BY c.category_id, s.service_id, b.bank_code
        """,
        selected_codes
    )
    raw = cur.fetchall()
    cur.close()

    # Structure as:
    # { "Deposit...": [ {"service": "Regular Savings", "BPI": "...", "BDO": "..."} , ... ] }
    data = {}
    row_index = {}  # (category_name, service_name) -> row dict

    for r in raw:
        section = r["category_name"]
        service = r["service_name"]
        bank = r["bank_code"]
        value = r["rate_value"]

        key = (section, service)

        if section not in data:
            data[section] = []

        if key not in row_index:
            row_index[key] = {"service": service}
            for code in selected_codes:
                row_index[key][code] = "N/A"
            data[section].append(row_index[key])

        row_index[key][bank] = value

    return render_template(
        "page3_financial_services.html",
        banks=",".join(selected_codes),
        selected_banks=selected_banks,
        financial_data_structured=data
    )


@app.route("/visual-graphs")
def visual_graphs():
    return "Visual Graphs page (coming soon)"

@app.route("/insights-summary")
def insights_summary():
    return "Insights Summary page (coming soon)"


@app.route("/reco")
def reco():
    return render_template("reco.html")

@app.route("/analysis")
def analysis():
    return render_template("sidebar.html")

@app.route("/bank-profile")
def bprofile():
    return render_template("bank_profile.html")

@app.route("/profile")
def profile():
    return render_template("sidebar.html")

@app.route("/logout")
def logout():
    return "Logged out"

@app.route("/help-center")
def help_center():
    return render_template("sidebar.html")

if __name__ == "__main__":
    app.run(debug=True)
