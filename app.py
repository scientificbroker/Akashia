from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'submissions.csv')
FIELDNAMES = ['timestamp', 'name', 'email', 'region', 'message']


def ensure_csv():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


@app.route('/', methods=['GET', 'POST'])
def index():
    ensure_csv()
    if request.method == 'POST':
        data = {
            'timestamp': datetime.utcnow().isoformat(),
            'name': request.form.get('name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'region': request.form.get('region', '').strip(),
            'message': request.form.get('message', '').strip(),
        }
        with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writerow(data)
        return redirect(url_for('success'))
    return render_template('index.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/submissions')
def submissions():
    ensure_csv()
    rows = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return render_template('submissions.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
