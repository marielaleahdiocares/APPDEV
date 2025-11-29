from flask import Flask, render_template

app = Flask(__name__)

@app.route('/guest-dashboard')
def guest_dashboard():
    return render_template('guest_dashboard.html')

if __name__ == '__main__':
    # Running on port 5005
    app.run(debug=True, port=5005)