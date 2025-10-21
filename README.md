# 🌙 Akashia - Banco de Sueños para Análisis Semántico

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![NLP](https://img.shields.io/badge/NLP-NLTK%20%7C%20spaCy%20%7C%20TextBlob-orange.svg)](https://nltk.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Akashia** es una plataforma web avanzada que permite a los soñantes registrar sus sueños y obtener análisis semánticos profundos utilizando técnicas de Procesamiento de Lenguaje Natural (NLP). La aplicación analiza patrones emocionales, detecta símbolos comunes y genera insights psicológicos únicos basados en el contenido de los sueños.

## 🎯 Características Principales

### 📝 Registro Inteligente de Sueños
- **Formulario avanzado** con campos específicos para análisis semántico
- **Validación inteligente** que asegura calidad de datos para mejor análisis
- **Interfaz moderna** con diseño responsive y experiencia de usuario optimizada
- **Categorización automática** por tipo de sueño, emoción y región geográfica

### 🧠 Análisis Semántico Avanzado
- **Análisis de sentimientos** con múltiples algoritmos (TextBlob, VADER)
- **Detección de patrones** de sueños comunes (vuelo, caída, persecución, etc.)
- **Extracción de entidades** (lugares, personas, objetos, emociones)
- **Cálculo de intensidad** del sueño basado en múltiples factores
- **Generación automática** de reportes e insights psicológicos

### 📊 Visualizaciones Interactivas
- **Dashboard en tiempo real** con estadísticas globales
- **Gráficos dinámicos** usando Plotly para análisis visual
- **Análisis comparativo** entre regiones y demografías
- **Evolución temporal** de patrones de sueños

## 🚀 Demo de Funcionalidad

### 1. Registro de Sueño

```html
<!-- Formulario principal -->
<form method="post" id="dreamForm">
  <div class="form-group">
    <label for="name">Nombre completo:</label>
    <input type="text" name="name" required>
  </div>
  
  <div class="form-group">
    <label for="dream_type">Tipo de sueño:</label>
    <select name="dream_type">
      <option value="normal">Sueño normal</option>
      <option value="lucido">Sueño lúcido</option>
      <option value="pesadilla">Pesadilla</option>
      <option value="recurrente">Sueño recurrente</option>
      <option value="profetico">Sueño profético/premonitorio</option>
    </select>
  </div>
  
  <div class="form-group">
    <label for="emotion">Emoción principal:</label>
    <select name="emotion">
      <option value="alegria">Alegría</option>
      <option value="miedo">Miedo</option>
      <option value="tristeza">Tristeza</option>
      <option value="paz">Paz/Tranquilidad</option>
    </select>
  </div>
  
  <div class="form-group">
    <label for="message">Describe tu sueño:</label>
    <textarea name="message" rows="8" maxlength="5000" 
              placeholder="Describe tu sueño con el mayor detalle posible..."></textarea>
  </div>
  
  <button type="submit" class="submit-btn">🌙 Registrar Sueño</button>
</form>
```

### 2. Análisis Semántico Automático

```python
# Ejemplo de análisis automático
def analyze_dream(dream_text, dream_type, emotion, age, region):
    analyzer = DreamAnalyzer()
    
    analysis = analyzer.analyze_dream(
        dream_text=dream_text,
        dream_type=dream_type,
        emotion=emotion,
        age=age,
        region=region
    )
    
    return {
        'sentiment': {
            'polarity': 0.3,  # -1 a 1
            'subjectivity': 0.7,  # 0 a 1
            'sentiment_label': 'positivo'
        },
        'patterns': {
            'vuelo': {'found': True, 'count': 2},
            'caida': {'found': True, 'count': 1},
            'persecucion': {'found': False, 'count': 0}
        },
        'entities': {
            'nouns': {'ciudad': 3, 'casa': 2, 'persona': 1},
            'verbs': {'volar': 2, 'caer': 1, 'correr': 1},
            'adjectives': {'grande': 1, 'hermosa': 1}
        },
        'dream_intensity': {
            'score': 75.5,
            'level': 'alta'
        },
        'keywords': {
            'volar': 2, 'ciudad': 3, 'miedo': 1, 'libertad': 1
        }
    }
```

### 3. Resultado del Análisis

```json
{
  "timestamp": "2025-01-20T15:30:00Z",
  "dream_type": "lucido",
  "emotion": "miedo",
  "sentiment": {
    "polarity": 0.2,
    "subjectivity": 0.8,
    "sentiment_label": "positivo",
    "vader_compound": 0.15
  },
  "patterns": {
    "vuelo": {"found": true, "count": 2},
    "caida": {"found": true, "count": 1},
    "persecucion": {"found": false, "count": 0}
  },
  "semantic": {
    "lugares": {"words": ["ciudad", "casa"], "count": 2, "percentage": 15.4},
    "emociones": {"words": ["miedo", "alegría"], "count": 2, "percentage": 7.7},
    "acciones": {"words": ["volar", "caer"], "count": 2, "percentage": 15.4}
  },
  "dream_intensity": {
    "score": 75.5,
    "level": "alta"
  },
  "report": {
    "resumen": "Este sueño tiene una intensidad alta (75.5/100) y un sentimiento positivo. Contiene 130 palabras distribuidas en 8 oraciones. Patrones detectados: vuelo, caída",
    "insights": [
      "El patrón de vuelo sugiere una búsqueda de libertad o escape.",
      "El sueño muestra emociones positivas, sugiriendo bienestar emocional."
    ],
    "recomendaciones": [
      "Este sueño de alta intensidad puede beneficiarse de técnicas de interpretación de sueños.",
      "Los sueños sobre vuelo suelen representar aspiraciones y libertad."
    ]
  }
}
```

## 📊 Dashboard y Visualizaciones

### Estadísticas Globales
```python
# Ejemplo de estadísticas generadas
stats = {
    'total_dreams': 1247,
    'avg_intensity': 68.3,
    'sentiment_distribution': {
        'positivo': 456,
        'negativo': 234,
        'neutral': 557
    },
    'common_patterns': {
        'vuelo': 89,
        'persecucion': 67,
        'caida': 45,
        'agua': 34
    },
    'dream_types': {
        'normal': 567,
        'lucido': 234,
        'pesadilla': 123,
        'recurrente': 89
    }
}
```

### Gráficos Interactivos
- **Distribución de sentimientos** por región
- **Evolución temporal** de patrones de sueños
- **Análisis demográfico** por edad y género
- **Mapa de calor** de emociones por tipo de sueño

## 🛠️ Instalación y Configuración

### Requisitos del Sistema
- Python 3.8+
- pip (gestor de paquetes de Python)
- Git

### Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/scientificbroker/Akashia.git
cd Akashia

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
```

### Configuración Avanzada

```bash
# Instalar modelo de spaCy para español
python -m spacy download es_core_news_sm

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

## 🔧 Tecnologías Utilizadas

### Backend
- **Flask 2.0+** - Framework web ligero y flexible
- **Python 3.8+** - Lenguaje de programación principal

### Procesamiento de Lenguaje Natural
- **NLTK 3.8+** - Biblioteca principal para NLP
- **spaCy 3.4+** - Procesamiento avanzado de texto
- **TextBlob 0.17+** - Análisis de sentimientos
- **VADER Sentiment** - Análisis emocional específico

### Visualización de Datos
- **Plotly 5.15+** - Gráficos interactivos
- **Matplotlib 3.6+** - Visualizaciones estáticas
- **Seaborn 0.12+** - Gráficos estadísticos

### Procesamiento de Datos
- **Pandas 1.5+** - Manipulación de datos
- **NumPy 1.24+** - Computación numérica
- **scikit-learn 1.2+** - Machine learning

## 📱 Estructura del Proyecto

```
Akashia/
├── app.py                 # Aplicación principal Flask
├── dream_analyzer.py      # Módulo de análisis semántico
├── requirements.txt       # Dependencias del proyecto
├── submissions.csv       # Base de datos de sueños
├── templates/            # Plantillas HTML
│   ├── index.html        # Formulario principal
│   ├── analysis.html     # Página de análisis
│   ├── dashboard.html    # Dashboard avanzado
│   ├── dream_analysis.html # Análisis detallado
│   └── submissions.html  # Lista de sueños
├── static/               # Archivos estáticos (CSS, JS)
├── tests/                # Pruebas unitarias
├── .github/              # Configuración de GitHub Actions
└── README.md             # Este archivo
```

## 🎮 Uso de la Aplicación

### 1. Registro de Sueños
1. Accede a `http://localhost:5000`
2. Completa el formulario con tus datos
3. Describe tu sueño con al menos 50 caracteres
4. Selecciona el tipo de sueño y emoción principal
5. Haz clic en "Registrar Sueño"

### 2. Visualización de Análisis
1. Ve a `/analysis` para ver estadísticas generales
2. Haz clic en "Ver análisis completo" en cualquier sueño
3. Explora el dashboard en `/dashboard` para visualizaciones avanzadas

### 3. Exportación de Datos
- **CSV**: `/export.csv` (requiere autenticación admin)
- **JSON**: `/export.json` (requiere autenticación admin)

## 🔍 Ejemplos de Análisis

### Sueño de Vuelo
**Entrada**: "Soñé que volaba sobre una ciudad muy grande. Me sentía libre y feliz, pero de repente empecé a caer y sentí mucho miedo..."

**Análisis**:
- **Sentimiento**: Positivo (0.3 polaridad)
- **Patrones**: Vuelo ✓, Caída ✓
- **Intensidad**: Alta (75/100)
- **Insights**: "El patrón de vuelo sugiere búsqueda de libertad", "La caída puede indicar pérdida de control"

### Pesadilla Recurrente
**Entrada**: "Siempre sueño que me persiguen por un bosque oscuro. No puedo correr rápido y siento que me van a atrapar..."

**Análisis**:
- **Sentimiento**: Negativo (-0.4 polaridad)
- **Patrones**: Persecución ✓, Agua ✗
- **Intensidad**: Muy Alta (85/100)
- **Insights**: "El patrón de persecución indica sentimientos de presión", "Sueño recurrente sugiere ansiedades persistentes"

## 🌍 Análisis Regional

Akashia permite analizar patrones de sueños por región geográfica:

```python
# Ejemplo de análisis regional
regional_analysis = {
    'España': {
        'total_dreams': 234,
        'common_patterns': ['vuelo', 'agua', 'familia'],
        'avg_intensity': 65.2,
        'sentiment': 'positivo'
    },
    'México': {
        'total_dreams': 189,
        'common_patterns': ['persecucion', 'muerte', 'agua'],
        'avg_intensity': 72.1,
        'sentiment': 'neutral'
    },
    'Argentina': {
        'total_dreams': 156,
        'common_patterns': ['vuelo', 'dinero', 'trabajo'],
        'avg_intensity': 58.7,
        'sentiment': 'positivo'
    }
}
```

## 🚀 Despliegue en Producción

### GitHub Actions + Render
```yaml
# .github/workflows/deploy.yml
name: Deploy to Render
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_WEBHOOK }}
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Equipo

- **scientificbroker** - Desarrollador principal
- **Contribuidores** - Comunidad de desarrolladores

## 📞 Contacto

- **GitHub**: [@scientificbroker](https://github.com/scientificbroker)
- **Proyecto**: [Akashia](https://github.com/scientificbroker/Akashia)
- **Issues**: [Reportar problemas](https://github.com/scientificbroker/Akashia/issues)

## 🙏 Agradecimientos

- Comunidad de desarrolladores de Python
- Contribuidores de las librerías de NLP utilizadas
- Usuarios que han compartido sus sueños para mejorar el análisis

---

**Akashia** - Donde los sueños encuentran su significado semántico 🌙✨