import os

import pandas as pd
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_d.html')

def read_file(file):
    _, file_extension = os.path.splitext(file.filename)
    if file_extension == '.xlsx':
        return pd.read_excel(file)
    elif file_extension == '.csv':
        return pd.read_csv(file)
    elif file_extension == '.txt':
        return pd.read_csv(file, delimiter='\t')
    else:
        return None

def save_file(df, filename):
    _, file_extension = os.path.splitext(filename)
    if file_extension == '.xlsx':
        df.to_excel(filename, index=False)
    elif file_extension == '.csv':
        df.to_csv(filename, index=False)
    elif file_extension == '.txt':
        df.to_csv(filename, index=False, sep='\t')

@app.route('/upload', methods=['POST'])
def upload():
    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '':
        return render_template('index_d.html', alert_message="Please select at least 1 file to upload.")

    df1 = read_file(file1)
    df1 = df1.drop_duplicates(subset='email')

    if file2.filename != '':
        df2 = read_file(file2)
        # Remove rows in df1 where the email exists in df2
        df1 = df1[~df1['email'].isin(df2['email'])]

    output_filename = 'output' + os.path.splitext(file1.filename)[1]
    save_file(df1, output_filename)

    # Return the modified file for download
    return send_file(output_filename, as_attachment=True)

if __name__ == '__main__':
    app.run()
