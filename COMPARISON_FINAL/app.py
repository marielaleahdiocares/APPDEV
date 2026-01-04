from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "1234"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "apple"
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


# # -------------------------------
# # Page 2: Detailed table (default)
# # -------------------------------
# @app.route("/compare")
# def detailed_table():
#     return render_template("page2_detailed_table.html", active_view="Detailed Table")


# # -------------------------------
# # Page 2: Detailed table for selected banks
# # -------------------------------
# @app.route("/compare/<banks>")
# def detailed_table_banks(banks):
#     selected_codes = [c.strip().upper() for c in banks.split(",") if c.strip()]
#     if len(selected_codes) < 2:
#         return redirect(url_for("comparison"))

#     cur = mysql.connection.cursor()

#     # Get selected bank details (for headers)
#     placeholders = ",".join(["%s"] * len(selected_codes))
#     cur.execute(
#         f"""
#         SELECT bank_id, bank_code, bank_name
#         FROM banks
#         WHERE bank_code IN ({placeholders})
#         ORDER BY bank_name
#         """,
#         selected_codes
#     )
#     selected_banks = cur.fetchall()

#     # ✅ Build table using service_type (description per bank per category)
#     cur.execute(
#         f"""
#         SELECT
#             c.category_id,
#             c.category_name,
#             b.bank_code,
#             GROUP_CONCAT(DISTINCT st.description ORDER BY st.description SEPARATOR ', ') AS service_list
#         FROM service_categories c
#         JOIN banks b ON b.bank_code IN ({placeholders})
#         LEFT JOIN service_type st
#                ON st.category_id = c.category_id
#               AND st.bank_id = b.bank_id
#         GROUP BY c.category_id, c.category_name, b.bank_code
#         ORDER BY c.category_id, b.bank_code
#         """,
#         selected_codes
#     )
#     raw = cur.fetchall()
#     cur.close()

#     # Pivot into: [{category_name, values:{BANKCODE: text}}]
#     rows_map = {}
#     for r in raw:
#         cat = r["category_name"]
#         bank_code = r["bank_code"]
#         service_list = r["service_list"] if r["service_list"] else "N/A"

#         if cat not in rows_map:
#             rows_map[cat] = {"category_name": cat, "values": {}}

#         rows_map[cat]["values"][bank_code] = service_list

#     table_rows = list(rows_map.values())

#     # Ensure every category row has every selected bank column
#     for row in table_rows:
#         for b in selected_banks:
#             row["values"].setdefault(b["bank_code"], "N/A")

#     return render_template(
#         "page2_detailed_table.html",
#         active_view="Detailed Table",
#         banks=",".join(selected_codes),
#         selected_banks=selected_banks,
#         table_rows=table_rows
#     )


from flask import render_template, request, redirect, url_for

# -------------------------------
# Page 2: Detailed table (default)
# -------------------------------
@app.route("/compare")
def detailed_table():
    # still show page, but no banks selected
    selected_filter = request.args.get("filter", "All Services")

    # dropdown options from DB
    cur = mysql.connection.cursor()
    cur.execute("SELECT category_name FROM service_categories ORDER BY category_id")
    categories = cur.fetchall()
    cur.close()

    service_types = ["All Services"] + [c["category_name"] for c in categories]

    return render_template(
        "page2_detailed_table.html",
        active_view="Detailed Table",
        banks="",
        selected_banks=[],
        table_rows=[],
        service_types=service_types,
        selected_filter=selected_filter
    )


# -------------------------------
# Page 2: Detailed table for selected banks + filter
# -------------------------------
@app.route("/compare/<banks>")
def detailed_table_banks(banks):
    selected_codes = [c.strip().upper() for c in banks.split(",") if c.strip()]
    if len(selected_codes) < 2:
        return redirect(url_for("comparison"))

    selected_filter = request.args.get("filter", "All Services")

    cur = mysql.connection.cursor()

    # ✅ dropdown options from DB
    cur.execute("SELECT category_name FROM service_categories ORDER BY category_id")
    categories = cur.fetchall()
    service_types = ["All Services"] + [c["category_name"] for c in categories]

    placeholders = ",".join(["%s"] * len(selected_codes))

    # Get selected bank details (for headers)
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

    # ✅ FILTER SQL PART
    filter_sql = ""
    params = selected_codes[:]  # for the IN (...) on banks

    # If not all services, filter by category_name
    if selected_filter != "All Services":
        filter_sql = " WHERE c.category_name = %s "
        params.append(selected_filter)

    # ✅ Build table using service_type descriptions per bank per category
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
        {filter_sql}
        GROUP BY c.category_id, c.category_name, b.bank_code
        ORDER BY c.category_id, b.bank_code
        """,
        params
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
        table_rows=table_rows,
        service_types=service_types,
        selected_filter=selected_filter
    )






# # -------------------------------
# # Page 3:  Financial Services
# # -------------------------------
# @app.route("/financial-services")
# def financial_services():
#     # URL example: /financial-services?banks=BPI,BDO,RCBC
#     banks_csv = request.args.get("banks", "")
#     selected_codes = [c.strip().upper() for c in banks_csv.split(",") if c.strip()]

#     if len(selected_codes) < 2:
#         return redirect(url_for("comparison"))

#     cur = mysql.connection.cursor()

#     # Get selected banks (validated + sorted)
#     placeholders = ",".join(["%s"] * len(selected_codes))
#     cur.execute(
#         f"""
#         SELECT bank_id, bank_code, bank_name
#         FROM banks
#         WHERE bank_code IN ({placeholders})
#         ORDER BY bank_name
#         """,
#         selected_codes
#     )
#     selected_banks = cur.fetchall()
#     selected_codes = [b["bank_code"] for b in selected_banks]  # re-sync

#     # Pull services + rates
#     cur.execute(
#         f"""
#         SELECT
#             c.category_id,
#             c.category_name,
#             s.service_id,
#             s.service_name,
#             b.bank_code,
#             COALESCE(sr.rate_value, 'N/A') AS rate_value
#         FROM service_categories c
#         JOIN services s ON s.category_id = c.category_id
#         JOIN banks b ON b.bank_code IN ({placeholders})
#         LEFT JOIN service_rates sr
#             ON sr.bank_id = b.bank_id
#            AND sr.service_id = s.service_id
#         ORDER BY c.category_id, s.service_id, b.bank_code
#         """,
#         selected_codes
#     )
#     raw = cur.fetchall()
#     cur.close()

#     # Structure as:
#     # { "Deposit...": [ {"service": "Regular Savings", "BPI": "...", "BDO": "..."} , ... ] }
#     data = {}
#     row_index = {}  # (category_name, service_name) -> row dict

#     for r in raw:
#         section = r["category_name"]
#         service = r["service_name"]
#         bank = r["bank_code"]
#         value = r["rate_value"]

#         key = (section, service)

#         if section not in data:
#             data[section] = []

#         if key not in row_index:
#             row_index[key] = {"service": service}
#             for code in selected_codes:
#                 row_index[key][code] = "N/A"
#             data[section].append(row_index[key])

#         row_index[key][bank] = value

#     return render_template(
#         "page3_financial_services.html",
#         banks=",".join(selected_codes),
#         selected_banks=selected_banks,
#         financial_data_structured=data
#     )


# -------------------------------
# Page 3: Financial Services (WITH FILTER)
# -------------------------------
@app.route("/financial-services")
def financial_services():
    # URL example: /financial-services?banks=BPI,BDO,RCBC&filter=Deposit and Account Services
    banks_csv = request.args.get("banks", "")
    selected_filter = request.args.get("filter", "All Services")

    selected_codes = [c.strip().upper() for c in banks_csv.split(",") if c.strip()]
    if len(selected_codes) < 2:
        return redirect(url_for("comparison"))

    cur = mysql.connection.cursor()

    # ✅ dropdown options from DB
    cur.execute("SELECT category_name FROM service_categories ORDER BY category_id")
    categories = cur.fetchall()
    service_types = ["All Services"] + [c["category_name"] for c in categories]

    # ✅ validate banks
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
    selected_codes = [b["bank_code"] for b in selected_banks]  # re-sync sorted + valid

    # ✅ FILTER SQL
    filter_sql = ""
    params = selected_codes[:]  # banks IN (...) params

    if selected_filter != "All Services":
        filter_sql = " AND c.category_name = %s "
        params.append(selected_filter)

    # ✅ Pull services + rates (filtered)
    placeholders2 = ",".join(["%s"] * len(selected_codes))
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
        JOIN banks b ON b.bank_code IN ({placeholders2})
        LEFT JOIN service_rates sr
            ON sr.bank_id = b.bank_id
           AND sr.service_id = s.service_id
        WHERE 1=1
        {filter_sql}
        ORDER BY c.category_id, s.service_id, b.bank_code
        """,
        params
    )
    raw = cur.fetchall()
    cur.close()

    # Structure:
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
        financial_data_structured=data,
        service_types=service_types,
        selected_filter=selected_filter
    )






# # -------------------------------
# # Visual Graphs (Page 4)
# # -------------------------------
# # @app.route("/visual-graphs")
# # def visual_graphs():
# #     return "Insights Summary page (coming soon)"

# @app.route("/visual-graphs")
# def visual_graphs():
#     # URL example: /visual-graphs?banks=BPI,BDO,RCBC&filter=All%20Services
#     banks_csv = request.args.get("banks", "")
#     selected_filter = request.args.get("filter", "All Services")

#     selected_codes = [c.strip().upper() for c in banks_csv.split(",") if c.strip()]
#     if len(selected_codes) < 2:
#         return redirect(url_for("comparison"))

#     cur = mysql.connection.cursor()
#     placeholders = ",".join(["%s"] * len(selected_codes))

#     # 1) Validate + sort selected banks
#     cur.execute(
#         f"""
#         SELECT bank_id, bank_code, bank_name
#         FROM banks
#         WHERE bank_code IN ({placeholders})
#         ORDER BY bank_name
#         """,
#         selected_codes
#     )
#     selected_banks = cur.fetchall()
#     if len(selected_banks) < 2:
#         cur.close()
#         return redirect(url_for("comparison"))

#     # re-sync in sorted order
#     selected_codes = [b["bank_code"] for b in selected_banks]
#     bank_ids_by_code = {b["bank_code"]: b["bank_id"] for b in selected_banks}

#     # 2) Service filter dropdown values (categories)
#     cur.execute("SELECT category_name FROM service_categories ORDER BY category_id")
#     categories = [r["category_name"] for r in cur.fetchall()]
#     service_types = ["All Services"] + categories

#     if selected_filter not in service_types:
#         selected_filter = "All Services"

#     # helper: find category_id for filter
#     filter_category_id = None
#     if selected_filter != "All Services":
#         cur.execute("SELECT category_id FROM service_categories WHERE category_name=%s LIMIT 1", (selected_filter,))
#         row = cur.fetchone()
#         filter_category_id = row["category_id"] if row else None

#     # -----------------------------
#     # GRAPH METRICS (simple + stable)
#     # -----------------------------

#     # A) Overall Satisfaction (Service Coverage Score) -> based on count of DISTINCT service_type descriptions
#     #    scaled to 80-100 using max among selected banks
#     overall_counts = {}
#     if selected_filter == "All Services":
#         cur.execute(
#             f"""
#             SELECT b.bank_code, COUNT(DISTINCT st.description) AS cnt
#             FROM banks b
#             LEFT JOIN service_type st ON st.bank_id = b.bank_id
#             WHERE b.bank_code IN ({placeholders})
#             GROUP BY b.bank_code
#             """,
#             selected_codes
#         )
#     else:
#         # filtered by selected category_id (if found)
#         if filter_category_id is None:
#             # fallback: no category match
#             cur.close()
#             return redirect(url_for("visual_graphs", banks=",".join(selected_codes), filter="All Services"))
#         cur.execute(
#             f"""
#             SELECT b.bank_code, COUNT(DISTINCT st.description) AS cnt
#             FROM banks b
#             LEFT JOIN service_type st
#               ON st.bank_id = b.bank_id AND st.category_id = %s
#             WHERE b.bank_code IN ({placeholders})
#             GROUP BY b.bank_code
#             """,
#             [filter_category_id] + selected_codes
#         )

#     for r in cur.fetchall():
#         overall_counts[r["bank_code"]] = int(r["cnt"] or 0)

#     max_overall = max(overall_counts.values()) if overall_counts else 1
#     overall_satisfaction = []
#     for code in selected_codes:
#         cnt = overall_counts.get(code, 0)
#         score = 80 + (cnt / max_overall) * 20 if max_overall else 80
#         overall_satisfaction.append(round(score, 1))

#     # B) Digital Performance (Digital Services Score) -> use Digital and Electronic Banking category
#     digital_counts = {code: 0 for code in selected_codes}
#     cur.execute(
#         """
#         SELECT category_id
#         FROM service_categories
#         WHERE category_name = 'Digital and Electronic Banking'
#         LIMIT 1
#         """
#     )
#     digital_row = cur.fetchone()
#     digital_cat_id = digital_row["category_id"] if digital_row else None

#     if digital_cat_id:
#         cur.execute(
#             f"""
#             SELECT b.bank_code, COUNT(DISTINCT st.description) AS cnt
#             FROM banks b
#             LEFT JOIN service_type st
#               ON st.bank_id = b.bank_id AND st.category_id = %s
#             WHERE b.bank_code IN ({placeholders})
#             GROUP BY b.bank_code
#             """,
#             [digital_cat_id] + selected_codes
#         )
#         for r in cur.fetchall():
#             digital_counts[r["bank_code"]] = int(r["cnt"] or 0)

#     max_digital = max(digital_counts.values()) if digital_counts else 1
#     digital_performance = []
#     for code in selected_codes:
#         cnt = digital_counts.get(code, 0)
#         score = 4.0 + (cnt / max_digital) * 1.0 if max_digital else 4.0
#         digital_performance.append(round(score, 2))

#     # C) Savings vs Loan Rate (Average from DB)
#     #    savings = Deposit and Account Services
#     #    loan    = Lending and Credit Services
#     def avg_rate_for_category(cat_name: str):
#         cur.execute("SELECT category_id FROM service_categories WHERE category_name=%s LIMIT 1", (cat_name,))
#         rr = cur.fetchone()
#         if not rr:
#             return {code: 0 for code in selected_codes}

#         cat_id = rr["category_id"]
#         cur.execute(
#             f"""
#             SELECT b.bank_code,
#                    AVG(
#                      CASE
#                        WHEN sr.rate_value REGEXP '^[0-9]+(\\.[0-9]+)?$'
#                          THEN CAST(sr.rate_value AS DECIMAL(10,4))
#                        ELSE NULL
#                      END
#                    ) AS avg_rate
#             FROM banks b
#             JOIN services s ON s.category_id = %s
#             LEFT JOIN service_rates sr
#               ON sr.bank_id = b.bank_id AND sr.service_id = s.service_id
#             WHERE b.bank_code IN ({placeholders})
#             GROUP BY b.bank_code
#             """,
#             [cat_id] + selected_codes
#         )
#         out = {code: 0 for code in selected_codes}
#         for r in cur.fetchall():
#             out[r["bank_code"]] = float(r["avg_rate"] or 0)
#         return out

#     savings_map = avg_rate_for_category("Deposit and Account Services")
#     loan_map = avg_rate_for_category("Lending and Credit Services")

#     savings_rate = [round(savings_map.get(code, 0), 4) for code in selected_codes]
#     loan_rate = [round(loan_map.get(code, 0), 4) for code in selected_codes]

#     # D) Service Diversity (Distinct Rated Services)
#     #    count distinct services with numeric rate_value
#     cur.execute(
#         f"""
#         SELECT b.bank_code,
#                COUNT(DISTINCT sr.service_id) AS cnt
#         FROM banks b
#         LEFT JOIN service_rates sr
#           ON sr.bank_id = b.bank_id
#          AND sr.rate_value REGEXP '^[0-9]+(\\.[0-9]+)?$'
#         WHERE b.bank_code IN ({placeholders})
#         GROUP BY b.bank_code
#         """,
#         selected_codes
#     )
#     diversity_map = {code: 0 for code in selected_codes}
#     for r in cur.fetchall():
#         diversity_map[r["bank_code"]] = int(r["cnt"] or 0)

#     service_diversity = [diversity_map.get(code, 0) for code in selected_codes]

#     cur.close()

#     graph_data = {
#         "banks": selected_codes,
#         "overall_satisfaction": overall_satisfaction,
#         "digital_performance": digital_performance,
#         "savings_rate": savings_rate,
#         "loan_rate": loan_rate,
#         "service_diversity": service_diversity
#     }

#     return render_template(
#         "page4_visual_graphs.html",
#         banks_csv=",".join(selected_codes),
#         selected_banks=selected_banks,
#         service_types=service_types,
#         selected_filter=selected_filter,
#         graph_data=graph_data
#     )

@app.route("/visual-graphs")
def visual_graphs():
    banks_csv = request.args.get("banks", "")
    selected_filter = request.args.get("filter", "All Services")

    selected_codes = [c.strip().upper() for c in banks_csv.split(",") if c.strip()]
    if len(selected_codes) < 2:
        return redirect(url_for("comparison"))

    cur = mysql.connection.cursor()
    placeholders = ",".join(["%s"] * len(selected_codes))

    # 1) Validate + sort selected banks
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
    if len(selected_banks) < 2:
        cur.close()
        return redirect(url_for("comparison"))

    selected_codes = [b["bank_code"] for b in selected_banks]  # sorted
    placeholders2 = ",".join(["%s"] * len(selected_codes))

    # 2) Service filter dropdown values
    cur.execute("SELECT category_id, category_name FROM service_categories ORDER BY category_id")
    cat_rows = cur.fetchall()
    service_types = ["All Services"] + [r["category_name"] for r in cat_rows]

    if selected_filter not in service_types:
        selected_filter = "All Services"

    filter_category_id = None
    if selected_filter != "All Services":
        for r in cat_rows:
            if r["category_name"] == selected_filter:
                filter_category_id = r["category_id"]
                break
        if filter_category_id is None:
            # fallback to all services if invalid filter
            selected_filter = "All Services"

    # -----------------------------
    # A) Overall Satisfaction (coverage count) scaled 80-100
    # -----------------------------
    if selected_filter == "All Services":
        cur.execute(
            f"""
            SELECT b.bank_code, COUNT(DISTINCT st.description) AS cnt
            FROM banks b
            LEFT JOIN service_type st ON st.bank_id = b.bank_id
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            selected_codes
        )
    else:
        cur.execute(
            f"""
            SELECT b.bank_code, COUNT(DISTINCT st.description) AS cnt
            FROM banks b
            LEFT JOIN service_type st
              ON st.bank_id = b.bank_id AND st.category_id = %s
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            [filter_category_id] + selected_codes
        )

    overall_counts = {code: 0 for code in selected_codes}
    for r in cur.fetchall():
        overall_counts[r["bank_code"]] = int(r["cnt"] or 0)

    max_overall = max(overall_counts.values()) if overall_counts else 1
    overall_satisfaction = []
    for code in selected_codes:
        cnt = overall_counts.get(code, 0)
        score = 80 + (cnt / max_overall) * 20 if max_overall else 80
        overall_satisfaction.append(round(score, 1))

    # -----------------------------
    # B) Digital Performance (fixed category)
    # -----------------------------
    digital_counts = {code: 0 for code in selected_codes}
    cur.execute(
        "SELECT category_id FROM service_categories WHERE category_name=%s LIMIT 1",
        ("Digital and Electronic Banking",)
    )
    digital_row = cur.fetchone()
    digital_cat_id = digital_row["category_id"] if digital_row else None

    if digital_cat_id:
        cur.execute(
            f"""
            SELECT b.bank_code, COUNT(DISTINCT st.description) AS cnt
            FROM banks b
            LEFT JOIN service_type st
              ON st.bank_id = b.bank_id AND st.category_id = %s
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            [digital_cat_id] + selected_codes
        )
        for r in cur.fetchall():
            digital_counts[r["bank_code"]] = int(r["cnt"] or 0)

    max_digital = max(digital_counts.values()) if digital_counts else 1
    digital_performance = []
    for code in selected_codes:
        cnt = digital_counts.get(code, 0)
        score = 4.0 + (cnt / max_digital) * 1.0 if max_digital else 4.0
        digital_performance.append(round(score, 2))

    # -----------------------------
    # C) Savings vs Loan Avg Rates
    # -----------------------------
    def avg_rate_for_category(cat_name: str):
        cur.execute("SELECT category_id FROM service_categories WHERE category_name=%s LIMIT 1", (cat_name,))
        rr = cur.fetchone()
        if not rr:
            return {code: 0 for code in selected_codes}

        cat_id = rr["category_id"]
        cur.execute(
            f"""
            SELECT b.bank_code,
                   AVG(
                     CASE
                       WHEN sr.rate_value REGEXP '^[0-9]+(\\.[0-9]+)?$'
                         THEN CAST(sr.rate_value AS DECIMAL(10,4))
                       ELSE NULL
                     END
                   ) AS avg_rate
            FROM banks b
            JOIN services s ON s.category_id = %s
            LEFT JOIN service_rates sr
              ON sr.bank_id = b.bank_id AND sr.service_id = s.service_id
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            [cat_id] + selected_codes
        )
        out = {code: 0 for code in selected_codes}
        for r in cur.fetchall():
            out[r["bank_code"]] = float(r["avg_rate"] or 0)
        return out

    savings_map = avg_rate_for_category("Deposit and Account Services")
    loan_map = avg_rate_for_category("Lending and Credit Services")
    savings_rate = [round(savings_map.get(code, 0), 4) for code in selected_codes]
    loan_rate = [round(loan_map.get(code, 0), 4) for code in selected_codes]

    # -----------------------------
    # D) Service Diversity (distinct numeric rated services)
    # ✅ now respects filter if user selects one
    # -----------------------------
    diversity_map = {code: 0 for code in selected_codes}

    if selected_filter == "All Services":
        cur.execute(
            f"""
            SELECT b.bank_code,
                   COUNT(DISTINCT sr.service_id) AS cnt
            FROM banks b
            LEFT JOIN service_rates sr
              ON sr.bank_id = b.bank_id
             AND sr.rate_value REGEXP '^[0-9]+(\\.[0-9]+)?$'
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            selected_codes
        )
        for r in cur.fetchall():
            diversity_map[r["bank_code"]] = int(r["cnt"] or 0)
    else:
        # only count rated services under selected category
        cur.execute(
            f"""
            SELECT b.bank_code,
                   COUNT(DISTINCT sr.service_id) AS cnt
            FROM banks b
            JOIN services s ON s.category_id = %s
            LEFT JOIN service_rates sr
              ON sr.bank_id = b.bank_id
             AND sr.service_id = s.service_id
             AND sr.rate_value REGEXP '^[0-9]+(\\.[0-9]+)?$'
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            [filter_category_id] + selected_codes
        )
        for r in cur.fetchall():
            diversity_map[r["bank_code"]] = int(r["cnt"] or 0)

    service_diversity = [diversity_map.get(code, 0) for code in selected_codes]

    cur.close()

    graph_data = {
        "banks": selected_codes,
        "overall_satisfaction": overall_satisfaction,
        "digital_performance": digital_performance,
        "savings_rate": savings_rate,
        "loan_rate": loan_rate,
        "service_diversity": service_diversity
    }

    return render_template(
        "page4_visual_graphs.html",
        banks_csv=",".join(selected_codes),
        selected_banks=selected_banks,
        service_types=service_types,
        selected_filter=selected_filter,
        graph_data=graph_data
    )

# # -------------------------------
# # INSIGHTS SUMMARY (Page 5)
# # -------------------------------
# @app.route("/insights-summary")
# def insights_summary():
#     # URL example: /insights-summary?banks=BPI,BDO,RCBC
#     banks_csv = request.args.get("banks", "")
#     selected_codes = [c.strip().upper() for c in banks_csv.split(",") if c.strip()]

#     if len(selected_codes) < 2:
#         return redirect(url_for("comparison"))

#     cur = mysql.connection.cursor()
#     placeholders = ",".join(["%s"] * len(selected_codes))

#     # 1) Validate + sort selected banks
#     cur.execute(
#         f"""
#         SELECT bank_id, bank_code, bank_name
#         FROM banks
#         WHERE bank_code IN ({placeholders})
#         ORDER BY bank_name
#         """,
#         selected_codes
#     )
#     selected_banks = cur.fetchall()

#     if len(selected_banks) < 2:
#         cur.close()
#         return redirect(url_for("comparison"))

#     selected_codes = [b["bank_code"] for b in selected_banks]  # re-sync sorted
#     bank_id_by_code = {b["bank_code"]: b["bank_id"] for b in selected_banks}
#     bank_name_by_code = {b["bank_code"]: b["bank_name"] for b in selected_banks}

#     # -----------------------------
#     # Helpers
#     # -----------------------------
#     def winner_highest(metric_map):
#         # metric_map: {code: number}
#         best_code = max(metric_map, key=lambda k: metric_map.get(k, float("-inf")))
#         return best_code, metric_map.get(best_code, 0)

#     def winner_lowest(metric_map):
#         # metric_map: {code: number}
#         valid = {k: v for k, v in metric_map.items() if v is not None}
#         best_code = min(valid, key=lambda k: valid.get(k, float("inf")))
#         return best_code, valid.get(best_code, 0)

#     def avg_rate_for_category(cat_name: str):
#         # returns {code: avg_numeric_rate or None}
#         cur.execute("SELECT category_id FROM service_categories WHERE category_name=%s LIMIT 1", (cat_name,))
#         rr = cur.fetchone()
#         if not rr:
#             return {code: None for code in selected_codes}

#         cat_id = rr["category_id"]
#         cur.execute(
#             f"""
#             SELECT b.bank_code,
#                    AVG(
#                      CASE
#                        WHEN sr.rate_value REGEXP '^[0-9]+(\\.[0-9]+)?$'
#                          THEN CAST(sr.rate_value AS DECIMAL(10,4))
#                        ELSE NULL
#                      END
#                    ) AS avg_rate
#             FROM banks b
#             JOIN services s ON s.category_id = %s
#             LEFT JOIN service_rates sr
#               ON sr.bank_id = b.bank_id AND sr.service_id = s.service_id
#             WHERE b.bank_code IN ({placeholders})
#             GROUP BY b.bank_code
#             """,
#             [cat_id] + selected_codes
#         )
#         out = {code: None for code in selected_codes}
#         for r in cur.fetchall():
#             out[r["bank_code"]] = float(r["avg_rate"]) if r["avg_rate"] is not None else None
#         return out

#     # -----------------------------
#     # METRICS FROM DB
#     # -----------------------------

#     # A) Overall Satisfaction (coverage score) = count distinct service_type.description
#     cur.execute(
#         f"""
#         SELECT b.bank_code, COUNT(DISTINCT st.description) AS cnt
#         FROM banks b
#         LEFT JOIN service_type st ON st.bank_id = b.bank_id
#         WHERE b.bank_code IN ({placeholders})
#         GROUP BY b.bank_code
#         """,
#         selected_codes
#     )
#     coverage_cnt = {code: 0 for code in selected_codes}
#     for r in cur.fetchall():
#         coverage_cnt[r["bank_code"]] = int(r["cnt"] or 0)

#     # scale to 80-100 like your graphs
#     max_cov = max(coverage_cnt.values()) if coverage_cnt else 1
#     overall_score = {}
#     for code in selected_codes:
#         cnt = coverage_cnt.get(code, 0)
#         overall_score[code] = round(80 + (cnt / max_cov) * 20, 1) if max_cov else 80.0

#     # B) Digital Performance = count distinct in Digital and Electronic Banking
#     cur.execute(
#         """
#         SELECT category_id
#         FROM service_categories
#         WHERE category_name = 'Digital and Electronic Banking'
#         LIMIT 1
#         """
#     )
#     dig_row = cur.fetchone()
#     dig_id = dig_row["category_id"] if dig_row else None

#     digital_cnt = {code: 0 for code in selected_codes}
#     if dig_id:
#         cur.execute(
#             f"""
#             SELECT b.bank_code, COUNT(DISTINCT st.description) AS cnt
#             FROM banks b
#             LEFT JOIN service_type st
#               ON st.bank_id = b.bank_id AND st.category_id = %s
#             WHERE b.bank_code IN ({placeholders})
#             GROUP BY b.bank_code
#             """,
#             [dig_id] + selected_codes
#         )
#         for r in cur.fetchall():
#             digital_cnt[r["bank_code"]] = int(r["cnt"] or 0)

#     max_dig = max(digital_cnt.values()) if digital_cnt else 1
#     digital_score = {}
#     for code in selected_codes:
#         cnt = digital_cnt.get(code, 0)
#         digital_score[code] = round(4.0 + (cnt / max_dig) * 1.0, 2) if max_dig else 4.0

#     # C) Savings avg and Loan avg
#     savings_avg = avg_rate_for_category("Deposit and Account Services")
#     loan_avg = avg_rate_for_category("Lending and Credit Services")

#     # D) Service Diversity = count distinct rated services (numeric rate_value)
#     cur.execute(
#         f"""
#         SELECT b.bank_code,
#                COUNT(DISTINCT sr.service_id) AS cnt
#         FROM banks b
#         LEFT JOIN service_rates sr
#           ON sr.bank_id = b.bank_id
#          AND sr.rate_value REGEXP '^[0-9]+(\\.[0-9]+)?$'
#         WHERE b.bank_code IN ({placeholders})
#         GROUP BY b.bank_code
#         """,
#         selected_codes
#     )
#     diversity_cnt = {code: 0 for code in selected_codes}
#     for r in cur.fetchall():
#         diversity_cnt[r["bank_code"]] = int(r["cnt"] or 0)

#     cur.close()





    # # -----------------------------
    # # Page 5: BUILD INSIGHTS TABLE
    # # -----------------------------
    # insights = []

    # # 1) Overall Satisfaction
    # w_code, w_val = winner_highest(overall_score)
    # insights.append({
    #     "Category": "Overall Satisfaction",
    #     "Top Bank": f"{w_code} ({bank_name_by_code.get(w_code, '')})",
    #     "Reason": f"Highest coverage score: {w_val}. Based on distinct services listed in your database."
    # })

    # # 2) Digital Performance
    # w_code, w_val = winner_highest(digital_score)
    # insights.append({
    #     "Category": "Digital Performance",
    #     "Top Bank": f"{w_code} ({bank_name_by_code.get(w_code, '')})",
    #     "Reason": f"Highest digital score: {w_val}. Based on Digital & Electronic Banking services available."
    # })

    # # 3) Best Savings Rate (highest avg)
    # # handle case: all None
    # if any(v is not None for v in savings_avg.values()):
    #     w_code, w_val = winner_highest({k: (v if v is not None else -1) for k, v in savings_avg.items()})
    #     insights.append({
    #         "Category": "Best Savings Rate",
    #         "Top Bank": f"{w_code} ({bank_name_by_code.get(w_code, '')})",
    #         "Reason": f"Highest average savings rate: {round(w_val, 4)} (from your service_rates data)."
    #     })
    # else:
    #     insights.append({
    #         "Category": "Best Savings Rate",
    #         "Top Bank": "N/A",
    #         "Reason": "No numeric savings rates found in service_rates for the selected banks."
    #     })

    # # 4) Best Loan Rate (lowest avg)
    # if any(v is not None for v in loan_avg.values()):
    #     w_code, w_val = winner_lowest({k: (v if v is not None else 999999) for k, v in loan_avg.items()})
    #     insights.append({
    #         "Category": "Best Loan Rate",
    #         "Top Bank": f"{w_code} ({bank_name_by_code.get(w_code, '')})",
    #         "Reason": f"Lowest average loan rate: {round(w_val, 4)} (from your service_rates data)."
    #     })
    # else:
    #     insights.append({
    #         "Category": "Best Loan Rate",
    #         "Top Bank": "N/A",
    #         "Reason": "No numeric loan rates found in service_rates for the selected banks."
    #     })

    # # 5) Most Diverse Services
    # w_code, w_val = winner_highest(diversity_cnt)
    # insights.append({
    #     "Category": "Most Diverse Services",
    #     "Top Bank": f"{w_code} ({bank_name_by_code.get(w_code, '')})",
    #     "Reason": f"Has the most rated services: {w_val}. (Count of distinct services with numeric rates.)"
    # })

    # return render_template(
    #     "page5_insights_summary.html",
    #     banks_csv=",".join(selected_codes),
    #     selected_banks=selected_banks,
    #     insights=insights
    # )
    
@app.route("/insights-summary")
def insights_summary():
    banks_csv = request.args.get("banks", "")
    selected_filter = request.args.get("filter", "All Services")

    selected_codes = [c.strip().upper() for c in banks_csv.split(",") if c.strip()]
    if len(selected_codes) < 2:
        return redirect(url_for("comparison"))

    cur = mysql.connection.cursor()
    placeholders = ",".join(["%s"] * len(selected_codes))

    # banks
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
    if len(selected_banks) < 2:
        cur.close()
        return redirect(url_for("comparison"))

    selected_codes = [b["bank_code"] for b in selected_banks]  # sorted
    bank_name_by_code = {b["bank_code"]: b["bank_name"] for b in selected_banks}
    placeholders2 = ",".join(["%s"] * len(selected_codes))

    # dropdown categories
    cur.execute("SELECT category_id, category_name FROM service_categories ORDER BY category_id")
    cat_rows = cur.fetchall()
    service_types = ["All Services"] + [r["category_name"] for r in cat_rows]

    if selected_filter not in service_types:
        selected_filter = "All Services"

    filter_category_id = None
    if selected_filter != "All Services":
        for r in cat_rows:
            if r["category_name"] == selected_filter:
                filter_category_id = r["category_id"]
                break
        if filter_category_id is None:
            selected_filter = "All Services"

    # -----------------------------
    # HELPERS
    # -----------------------------
    def winner_highest(score_map):
        best_code, best_val = None, None
        for k, v in score_map.items():
            if v is None:
                continue
            if best_val is None or v > best_val:
                best_code, best_val = k, v
        return best_code, best_val

    def winner_lowest(score_map):
        best_code, best_val = None, None
        for k, v in score_map.items():
            if v is None:
                continue
            if best_val is None or v < best_val:
                best_code, best_val = k, v
        return best_code, best_val

    # -----------------------------
    # METRICS (aligned w/ Visual Graphs)
    # -----------------------------

    # 1) Overall Satisfaction (coverage) — respects filter
    if selected_filter == "All Services":
        cur.execute(
            f"""
            SELECT b.bank_code, COUNT(DISTINCT st.description) AS cnt
            FROM banks b
            LEFT JOIN service_type st ON st.bank_id = b.bank_id
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            selected_codes
        )
    else:
        cur.execute(
            f"""
            SELECT b.bank_code, COUNT(DISTINCT st.description) AS cnt
            FROM banks b
            LEFT JOIN service_type st
              ON st.bank_id = b.bank_id AND st.category_id = %s
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            [filter_category_id] + selected_codes
        )

    coverage_cnt = {code: 0 for code in selected_codes}
    for r in cur.fetchall():
        coverage_cnt[r["bank_code"]] = int(r["cnt"] or 0)

    max_cov = max(coverage_cnt.values()) if coverage_cnt else 1
    overall_score = {}
    for code in selected_codes:
        cnt = coverage_cnt.get(code, 0)
        overall_score[code] = round(80 + (cnt / max_cov) * 20, 1) if max_cov else 80.0

    # 2) Digital Performance (fixed digital category)
    cur.execute(
        "SELECT category_id FROM service_categories WHERE category_name=%s LIMIT 1",
        ("Digital and Electronic Banking",)
    )
    digital_row = cur.fetchone()
    digital_cat_id = digital_row["category_id"] if digital_row else None

    digital_cnt = {code: 0 for code in selected_codes}
    if digital_cat_id:
        cur.execute(
            f"""
            SELECT b.bank_code, COUNT(DISTINCT st.description) AS cnt
            FROM banks b
            LEFT JOIN service_type st
              ON st.bank_id = b.bank_id AND st.category_id = %s
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            [digital_cat_id] + selected_codes
        )
        for r in cur.fetchall():
            digital_cnt[r["bank_code"]] = int(r["cnt"] or 0)

    max_dig = max(digital_cnt.values()) if digital_cnt else 1
    digital_score = {}
    for code in selected_codes:
        cnt = digital_cnt.get(code, 0)
        digital_score[code] = round(4.0 + (cnt / max_dig) * 1.0, 2) if max_dig else 4.0

    # 3/4) Savings Avg + Loan Avg
    # Optional: if filter != All Services, we compute avg only for that category (better consistency)
    def avg_rate_for_category_id(cat_id):
        cur.execute(
            f"""
            SELECT b.bank_code,
                   AVG(
                     CASE
                       WHEN sr.rate_value REGEXP '^[0-9]+(\\.[0-9]+)?$'
                         THEN CAST(sr.rate_value AS DECIMAL(10,4))
                       ELSE NULL
                     END
                   ) AS avg_rate
            FROM banks b
            JOIN services s ON s.category_id = %s
            LEFT JOIN service_rates sr
              ON sr.bank_id = b.bank_id AND sr.service_id = s.service_id
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            [cat_id] + selected_codes
        )
        out = {code: None for code in selected_codes}
        for r in cur.fetchall():
            out[r["bank_code"]] = float(r["avg_rate"]) if r["avg_rate"] is not None else None
        return out

    if selected_filter == "All Services":
        # keep your original meaning: Savings = Deposit, Loan = Lending
        cur.execute("SELECT category_id FROM service_categories WHERE category_name=%s LIMIT 1", ("Deposit and Account Services",))
        dep = cur.fetchone()
        cur.execute("SELECT category_id FROM service_categories WHERE category_name=%s LIMIT 1", ("Lending and Credit Services",))
        lend = cur.fetchone()

        savings_avg = avg_rate_for_category_id(dep["category_id"]) if dep else {code: None for code in selected_codes}
        loan_avg = avg_rate_for_category_id(lend["category_id"]) if lend else {code: None for code in selected_codes}
    else:
        # when filtered, use that category for both "Best Rate" metrics
        savings_avg = avg_rate_for_category_id(filter_category_id)
        loan_avg = avg_rate_for_category_id(filter_category_id)

    # 5) Diversity (numeric rated services) — respects filter
    diversity_cnt = {code: 0 for code in selected_codes}
    if selected_filter == "All Services":
        cur.execute(
            f"""
            SELECT b.bank_code, COUNT(DISTINCT sr.service_id) AS cnt
            FROM banks b
            LEFT JOIN service_rates sr
              ON sr.bank_id = b.bank_id
             AND sr.rate_value REGEXP '^[0-9]+(\\.[0-9]+)?$'
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            selected_codes
        )
    else:
        cur.execute(
            f"""
            SELECT b.bank_code, COUNT(DISTINCT sr.service_id) AS cnt
            FROM banks b
            JOIN services s ON s.category_id = %s
            LEFT JOIN service_rates sr
              ON sr.bank_id = b.bank_id
             AND sr.service_id = s.service_id
             AND sr.rate_value REGEXP '^[0-9]+(\\.[0-9]+)?$'
            WHERE b.bank_code IN ({placeholders2})
            GROUP BY b.bank_code
            """,
            [filter_category_id] + selected_codes
        )
    for r in cur.fetchall():
        diversity_cnt[r["bank_code"]] = int(r["cnt"] or 0)

    cur.close()

    # -----------------------------
    # Page 5: BUILD INSIGHTS TABLE (UPDATED text includes filter)
    # -----------------------------
    insights = []

    # 1) Overall Satisfaction
    w_code, w_val = winner_highest(overall_score)
    insights.append({
        "Category": "Overall Satisfaction",
        "Top Bank": f"{w_code} ({bank_name_by_code.get(w_code, '')})" if w_code else "N/A",
        "Reason": f"Highest coverage score: {w_val}. Based on distinct services in your database"
                  + (f" under '{selected_filter}'." if selected_filter != "All Services" else ".")
    })

    # 2) Digital Performance
    w_code, w_val = winner_highest(digital_score)
    insights.append({
        "Category": "Digital Performance",
        "Top Bank": f"{w_code} ({bank_name_by_code.get(w_code, '')})" if w_code else "N/A",
        "Reason": f"Highest digital score: {w_val}. Based on Digital & Electronic Banking services available."
    })

    # 3) Best Savings Rate (highest avg)
    if any(v is not None for v in savings_avg.values()):
        w_code, w_val = winner_highest({k: (v if v is not None else -1) for k, v in savings_avg.items()})
        insights.append({
            "Category": "Best Savings Rate" if selected_filter == "All Services" else f"Best Rate (Highest) - {selected_filter}",
            "Top Bank": f"{w_code} ({bank_name_by_code.get(w_code, '')})",
            "Reason": f"Highest average rate: {round(w_val, 4)} (from service_rates)."
        })
    else:
        insights.append({
            "Category": "Best Savings Rate" if selected_filter == "All Services" else f"Best Rate (Highest) - {selected_filter}",
            "Top Bank": "N/A",
            "Reason": "No numeric rates found in service_rates for the selected banks."
        })

    # 4) Best Loan Rate (lowest avg)
    if any(v is not None for v in loan_avg.values()):
        w_code, w_val = winner_lowest({k: (v if v is not None else 999999) for k, v in loan_avg.items()})
        insights.append({
            "Category": "Best Loan Rate" if selected_filter == "All Services" else f"Best Rate (Lowest) - {selected_filter}",
            "Top Bank": f"{w_code} ({bank_name_by_code.get(w_code, '')})",
            "Reason": f"Lowest average rate: {round(w_val, 4)} (from service_rates)."
        })
    else:
        insights.append({
            "Category": "Best Loan Rate" if selected_filter == "All Services" else f"Best Rate (Lowest) - {selected_filter}",
            "Top Bank": "N/A",
            "Reason": "No numeric rates found in service_rates for the selected banks."
        })

    # 5) Most Diverse Services
    w_code, w_val = winner_highest(diversity_cnt)
    insights.append({
        "Category": "Most Diverse Services",
        "Top Bank": f"{w_code} ({bank_name_by_code.get(w_code, '')})" if w_code else "N/A",
        "Reason": f"Has the most rated services: {w_val}."
                  + (f" (Filtered: {selected_filter})" if selected_filter != "All Services" else
                     " (Count of distinct services with numeric rates.)")
    })

    return render_template(
        "page5_insights_summary.html",
        banks_csv=",".join(selected_codes),
        selected_banks=selected_banks,
        insights=insights,
        service_types=service_types,
        selected_filter=selected_filter
    )





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
