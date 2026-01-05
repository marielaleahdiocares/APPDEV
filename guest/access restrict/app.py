from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "1234"

# ----------------------------
# Helpers
# ----------------------------
def is_logged_in():
    return session.get("user_id") is not None

def is_guest():
    # Treat not-logged-in as guest
    return not is_logged_in() or session.get("role") == "guest"

# ----------------------------
# Routes
# ----------------------------
@app.route("/")
def guest_dashboard():
    # demo: always guest
    session["role"] = "guest"
    session.pop("user_id", None)
    return render_template("guest_dashboard.html")


@app.route("/restricted")
def restricted():
    # ✅ Server-side protection (IMPORTANT)
    if is_guest():
        flash("Access restricted. Please register first.", "error")
        return redirect(url_for("guest_dashboard"))

    return "<h1>Restricted content ✅</h1><p>You are logged in.</p>"


@app.route("/register", methods=["POST"])
def register():
    # Demo register: replace with DB + password hashing
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    next_url = request.form.get("next", "").strip()

    if not name or not email or not password:
        flash("Please fill out all fields.", "error")
        return redirect(url_for("guest_dashboard"))

    # pretend user created
    session["user_id"] = 1
    session["role"] = "user"
    session["name"] = name

    flash("Registered successfully!", "success")

    # redirect to what they tried to open
    if next_url:
        return redirect(next_url)
    return redirect(url_for("restricted"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("guest_dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
