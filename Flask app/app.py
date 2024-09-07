from flask import Flask
from flask import request
from flask import jsonify


# Create an instance of the Flask class
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    return "Hello, World!"

@app.route('/greet/<name>')
def greet(name):
    return f"Hello, {name}!"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form['data']  # Get data from form
    return f"You submitted: {data}"

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello, this is your data!"})


if __name__ == '__main__':
    # Run the app on a development server
    app.run(debug=True)
