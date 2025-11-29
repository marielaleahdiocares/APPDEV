from flask import Flask, render_template

app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    # In a real app, you would pass database data here.
    # For now, we render the static layout.
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Running on port 5001 to avoid conflict if you have the other app running