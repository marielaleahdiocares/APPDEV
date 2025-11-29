from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_dashboard():
    return render_template('main_dashboard.html')

if __name__ == '__main__':
    # Running on port 5003
    app.run(debug=True, port=5003)