from flask import Flask, request, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_d.html')

@app.route('/upload', methods=['POST'])
def upload():
    # if 'file1' not in request.files or 'file2' not in request.files:
    #     return "Please select two files to upload."

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '':
        return render_template('index_d.html', alert_message="Please select at least 1 file to upload.")
    
    df1 = pd.read_excel(file1)
    df1 = df1.drop_duplicates(subset='email')

    if file2.filename != '':
        df2 = pd.read_excel(file2)
        # Remove rows in df1 where the email exists in df2
        df1 = df1[~df1['email'].isin(df2['email'])]

    # Save the modified DataFrame to a new Excel file
    output_file = 'output.xlsx'
    df1.to_excel(output_file, index=False)

    # Return the modified Excel file for download
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
