from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.post('/predict')
def Output_page():
    return render_template('output.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)