@app.route("/comparison", methods=["GET", "POST"])
def comparison():
    cur = mysql.connection.cursor()
    cur.execute("SELECT bank_code, bank_name FROM banks ORDER BY bank_name")
    all_banks = cur.fetchall()
    
    # Fetch available services
    cur.execute("SELECT code, name FROM services ORDER BY name")
    all_services = cur.fetchall()
    
    cur.close()

    if request.method == "POST":
        selected_service = request.form.get("selected_service")
        selected_codes = request.form.getlist("selected_banks")

        # If no service or not enough banks are selected
        if not selected_service or len(selected_codes) < 2:
            return render_template("page1_select_banks.html", all_banks=all_banks, all_services=all_services)

        # Prepare data for redirection
        banks_csv = ",".join(selected_codes)
        return redirect(url_for("detailed_table_banks", banks=banks_csv, service=selected_service))

    return render_template("page1_select_banks.html", all_banks=all_banks, all_services=all_services)


@app.route("/compare/<banks>")
def detailed_table_banks(banks):
    selected_codes = [c.strip().upper() for c in banks.split(",") if c.strip()]
    selected_service = request.args.get("service")  # Get the selected service

    if len(selected_codes) < 2:
        return redirect(url_for("comparison"))

    # Fetch service details based on selected service
    cur = mysql.connection.cursor()
    
    # Get the details of selected service
    cur.execute("SELECT * FROM services WHERE code = %s", (selected_service,))
    selected_service_details = cur.fetchone()

    # Fetch banks and filter them based on selected service
    placeholders = ",".join(["%s"] * len(selected_codes))
    cur.execute(f"""
        SELECT bank_code, bank_name
        FROM banks
        WHERE bank_code IN ({placeholders})
        ORDER BY bank_name
    """, selected_codes)

    selected_banks = cur.fetchall()
    cur.close()

    # Use `selected_service` for further filtering or display on the page
    return render_template(
        "page2_detailed_table.html",
        active_view="Detailed Table",
        selected_service=selected_service_details,
        selected_banks=selected_banks
    )
