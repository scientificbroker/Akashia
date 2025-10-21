from flask import Flask, render_template, request, redirect, url_for, abort, Response, jsonify
import csv
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from dream_analyzer import DreamAnalyzer, analyze_dream_text

load_dotenv()

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# allow overriding CSV path for tests or env
CSV_PATH = os.environ.get('AKASHIA_CSV_PATH', os.path.join(BASE_DIR, 'submissions.csv'))
FIELDNAMES = ['timestamp', 'name', 'email', 'age', 'region', 'dream_type', 'emotion', 'message', 'analysis']
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
        # Recopilar datos del formulario
        data = {
            'timestamp': datetime.utcnow().isoformat(),
            'name': request.form.get('name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'age': request.form.get('age', '').strip(),
            'region': request.form.get('region', '').strip(),
            'dream_type': request.form.get('dream_type', '').strip(),
            'emotion': request.form.get('emotion', '').strip(),
            'message': request.form.get('message', '').strip(),
        }
        
        # Validación básica
        if not data['name'] or not data['email']:
            return render_template('index.html', error='Nombre y correo son obligatorios')
        if len(data['name']) > 200:
            return render_template('index.html', error='Nombre demasiado largo')
        if len(data['message']) > 5000:
            return render_template('index.html', error='Mensaje demasiado largo')
        if len(data['message']) < 50:
            return render_template('index.html', error='Por favor, describe tu sueño con al menos 50 caracteres para un mejor análisis')

        # Realizar análisis semántico
        try:
            analyzer = DreamAnalyzer()
            analysis = analyzer.analyze_dream(
                dream_text=data['message'],
                dream_type=data['dream_type'],
                emotion=data['emotion'],
                age=data['age'],
                region=data['region']
            )
            
            # Generar reporte
            report = analyzer.generate_dream_report(analysis)
            analysis['report'] = report
            
            # Convertir análisis a JSON string para almacenar
            data['analysis'] = json.dumps(analysis, ensure_ascii=False)
            
        except Exception as e:
            print(f"Error en análisis: {e}")
            data['analysis'] = json.dumps({'error': 'Error en el análisis semántico'})

        # Guardar en CSV
        with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writerow(data)
        
        return redirect(url_for('dream_analysis', dream_id=len(open(CSV_PATH, 'r', encoding='utf-8').readlines())-1))
    
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


@app.route('/dream-analysis/<int:dream_id>')
def dream_analysis(dream_id):
    """Muestra el análisis detallado de un sueño específico"""
    ensure_csv()
    rows = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    
    if dream_id >= len(rows):
        abort(404)
    
    dream_data = rows[dream_id]
    
    # Parsear análisis si existe
    analysis = None
    if dream_data.get('analysis'):
        try:
            analysis = json.loads(dream_data['analysis'])
        except:
            analysis = {'error': 'Error al parsear el análisis'}
    
    return render_template('dream_analysis.html', dream=dream_data, analysis=analysis)


@app.route('/analysis')
def analysis():
    """Página principal de análisis semántico"""
    ensure_csv()
    rows = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    
    # Estadísticas generales
    stats = {
        'total_dreams': len(rows),
        'dream_types': {},
        'emotions': {},
        'regions': {},
        'sentiment_distribution': {'positivo': 0, 'negativo': 0, 'neutral': 0},
        'avg_intensity': 0,
        'common_patterns': {}
    }
    
    total_intensity = 0
    intensity_count = 0
    
    for row in rows:
        # Contar tipos de sueños
        dream_type = row.get('dream_type', 'no especificado')
        stats['dream_types'][dream_type] = stats['dream_types'].get(dream_type, 0) + 1
        
        # Contar emociones
        emotion = row.get('emotion', 'no especificado')
        stats['emotions'][emotion] = stats['emotions'].get(emotion, 0) + 1
        
        # Contar regiones
        region = row.get('region', 'no especificado')
        stats['regions'][region] = stats['regions'].get(region, 0) + 1
        
        # Análisis de sentimientos
        if row.get('analysis'):
            try:
                analysis = json.loads(row['analysis'])
                if 'sentiment' in analysis:
                    sentiment_label = analysis['sentiment'].get('sentiment_label', 'neutral')
                    stats['sentiment_distribution'][sentiment_label] += 1
                
                if 'dream_intensity' in analysis:
                    intensity_score = analysis['dream_intensity'].get('score', 0)
                    total_intensity += intensity_score
                    intensity_count += 1
                
                # Patrones comunes
                if 'patterns' in analysis:
                    for pattern_name, pattern_data in analysis['patterns'].items():
                        if pattern_data.get('found'):
                            stats['common_patterns'][pattern_name] = stats['common_patterns'].get(pattern_name, 0) + 1
            except:
                continue
    
    if intensity_count > 0:
        stats['avg_intensity'] = round(total_intensity / intensity_count, 1)
    
    return render_template('analysis.html', stats=stats, dreams=rows[-10:])  # Últimos 10 sueños


@app.route('/dashboard')
def dashboard():
    """Dashboard con visualizaciones avanzadas"""
    ensure_csv()
    rows = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    
    return render_template('dashboard.html', dreams=rows)


if __name__ == '__main__':
    # Configuración para producción
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
