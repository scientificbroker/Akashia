from flask import Flask, render_template, request, redirect, url_for, abort, Response, jsonify
import csv
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# allow overriding CSV path for tests or env
CSV_PATH = os.environ.get('AKASHIA_CSV_PATH', os.path.join(BASE_DIR, 'submissions.csv'))
FIELDNAMES = ['timestamp', 'name', 'email', 'region', 'message']
# admin password (set in env or .env file)
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'changeme')


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
        # simple server-side validation
        if not data['name'] or not data['email']:
            return render_template('index.html', error='Nombre y correo son obligatorios')
        if len(data['name']) > 200:
            return render_template('index.html', error='Nombre demasiado largo')
        if len(data['message']) > 5000:
            return render_template('index.html', error='Mensaje demasiado largo')

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
    if not check_admin():
        abort(403)
    rows = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return render_template('submissions.html', rows=rows)


def check_admin():
    # allow admin via header or query param
    header = request.headers.get('X-AKASHIA-ADMIN')
    q = request.args.get('admin')
    if header and header == ADMIN_PASSWORD:
        return True
    if q and q == ADMIN_PASSWORD:
        return True
    return False


@app.route('/export.csv')
def export_csv():
    ensure_csv()
    if not check_admin():
        abort(403)
    def generate():
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            for line in f:
                yield line
    return Response(generate(), mimetype='text/csv')


@app.route('/export.json')
def export_json():
    ensure_csv()
    if not check_admin():
        abort(403)
    rows = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return jsonify(rows)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
