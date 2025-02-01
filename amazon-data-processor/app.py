from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/process', methods=['POST'])
def process_files():
    # Add your file processing logic here
    return "Files processed successfully!"

if __name__ == '__main__':
    app.run(debug=True)
