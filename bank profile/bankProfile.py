from flask import Flask, render_template

app = Flask(__name__)

@app.route('/bank-profile')
def bank_profile():
    return render_template('bankDetails.html')

if __name__ == '__main__':
    app.run(debug=True, port=5004)