from flask import Flask, render_template

app = Flask(__name__)

# Dummy user data to simulate fetching from a database
user_data = {
    'profile_picture': 'path/to/princess_picture.jpg', # You'll need to set up static file serving for this
    'full_name': 'Princess Marcelle T. Ambrocio',
    'email_address': 'princessambrocio887@gmail.com',
    'contact_number': '0939 249 3901',
    'address': 'Sobol Asingan, Pangasinan',
    'customer_type': 'Existing Bank Client'
}

@app.route('/profile')
def profile():
    # Pass the user data to the HTML template
    return render_template('profile.html', user=user_data)

if __name__ == '__main__':
    # Set debug=True for development
    app.run(debug=True)