"""
Módulo de análisis semántico para sueños
Proporciona análisis de sentimientos, extracción de entidades y patrones semánticos
"""

import re
import json
from collections import Counter, defaultdict
from datetime import datetime
import pandas as pd
import numpy as np

# Importaciones para NLP
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import SnowballStemmer
    from nltk.tag import pos_tag
    from textblob import TextBlob
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except ImportError:
    print("Instalando dependencias de NLP...")
    import subprocess
    subprocess.check_call(["pip", "install", "nltk", "textblob", "vaderSentiment"])
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import SnowballStemmer
    from nltk.tag import pos_tag
    from textblob import TextBlob
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class DreamAnalyzer:
    def __init__(self):
        """Inicializa el analizador de sueños"""
        self.stemmer = SnowballStemmer('spanish')
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Descargar recursos de NLTK si no están disponibles
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
        
        # Palabras de parada en español
        self.stop_words = set(stopwords.words('spanish'))
        
        # Diccionarios semánticos específicos para sueños
        self.dream_categories = {
            'lugares': ['casa', 'calle', 'montaña', 'mar', 'bosque', 'ciudad', 'campo', 'playa', 'montaña', 'río', 'lago', 'edificio', 'escuela', 'trabajo', 'hospital', 'iglesia', 'tienda', 'restaurante'],
            'personas': ['familia', 'amigo', 'padre', 'madre', 'hermano', 'hermana', 'abuelo', 'abuela', 'novio', 'novia', 'esposo', 'esposa', 'hijo', 'hija', 'profesor', 'doctor', 'policía', 'extraño', 'conocido'],
            'emociones': ['miedo', 'alegría', 'tristeza', 'ira', 'sorpresa', 'paz', 'ansiedad', 'calma', 'nervios', 'felicidad', 'angustia', 'tranquilidad', 'preocupación', 'esperanza', 'desesperación'],
            'acciones': ['correr', 'volar', 'caer', 'nadar', 'caminar', 'gritar', 'llorar', 'reír', 'pelear', 'huir', 'perseguir', 'buscar', 'encontrar', 'perder', 'ganar', 'soñar', 'despertar'],
            'objetos': ['coche', 'avión', 'barco', 'casa', 'puerta', 'ventana', 'espejo', 'llave', 'dinero', 'joyas', 'libro', 'teléfono', 'reloj', 'ropa', 'zapatos', 'comida', 'agua', 'fuego'],
            'colores': ['rojo', 'azul', 'verde', 'amarillo', 'negro', 'blanco', 'gris', 'morado', 'rosa', 'naranja', 'marrón', 'dorado', 'plateado'],
            'animales': ['perro', 'gato', 'pájaro', 'pez', 'caballo', 'vaca', 'cerdo', 'serpiente', 'araña', 'mariposa', 'león', 'tigre', 'elefante', 'oso', 'lobo', 'conejo']
        }
        
        # Patrones de sueños comunes
        self.dream_patterns = {
            'caida': r'\b(caer|caída|precipicio|vacío|hundirse)\b',
            'vuelo': r'\b(volar|vuelo|aire|altura|alas|cielo)\b',
            'persecucion': r'\b(perseguir|huir|correr|escapar|persecución)\b',
            'agua': r'\b(agua|mar|océano|lluvia|inundación|nadar)\b',
            'muerte': r'\b(muerte|morir|muerto|cementerio|funeral)\b',
            'nudez': r'\b(desnudo|ropa|vestido|desnudez)\b',
            'examen': r'\b(examen|prueba|estudiar|escuela|universidad)\b',
            'dientes': r'\b(dientes|muelas|caer|perder)\b'
        }

    def analyze_dream(self, dream_text, dream_type=None, emotion=None, age=None, region=None):
        """
        Analiza un sueño completo y devuelve un diccionario con todos los análisis
        """
        if not dream_text or len(dream_text.strip()) < 10:
            return {"error": "El texto del sueño es demasiado corto para analizar"}
        
        # Limpiar texto
        cleaned_text = self._clean_text(dream_text)
        
        # Análisis básico
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'dream_type': dream_type,
            'emotion': emotion,
            'age': age,
            'region': region,
            'text_length': len(dream_text),
            'word_count': len(cleaned_text.split()),
            'sentence_count': len(sent_tokenize(dream_text))
        }
        
        # Análisis de sentimientos
        analysis['sentiment'] = self._analyze_sentiment(cleaned_text)
        
        # Análisis semántico
        analysis['semantic'] = self._analyze_semantic_content(cleaned_text)
        
        # Extracción de entidades
        analysis['entities'] = self._extract_entities(cleaned_text)
        
        # Patrones de sueños
        analysis['patterns'] = self._detect_dream_patterns(cleaned_text)
        
        # Palabras clave
        analysis['keywords'] = self._extract_keywords(cleaned_text)
        
        # Análisis emocional avanzado
        analysis['emotional_analysis'] = self._analyze_emotions(cleaned_text)
        
        # Puntuación de intensidad del sueño
        analysis['dream_intensity'] = self._calculate_dream_intensity(analysis)
        
        return analysis

    def _clean_text(self, text):
        """Limpia y normaliza el texto"""
        # Convertir a minúsculas
        text = text.lower()
        
        # Remover caracteres especiales pero mantener acentos
        text = re.sub(r'[^\w\sáéíóúüñ]', ' ', text)
        
        # Remover espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

    def _analyze_sentiment(self, text):
        """Analiza el sentimiento del texto"""
        blob = TextBlob(text)
        vader_scores = self.sentiment_analyzer.polarity_scores(text)
        
        return {
            'polarity': blob.sentiment.polarity,  # -1 a 1
            'subjectivity': blob.sentiment.subjectivity,  # 0 a 1
            'vader_compound': vader_scores['compound'],
            'vader_positive': vader_scores['pos'],
            'vader_negative': vader_scores['neg'],
            'vader_neutral': vader_scores['neu'],
            'sentiment_label': self._get_sentiment_label(vader_scores['compound'])
        }

    def _get_sentiment_label(self, compound_score):
        """Convierte el score compuesto en una etiqueta"""
        if compound_score >= 0.05:
            return 'positivo'
        elif compound_score <= -0.05:
            return 'negativo'
        else:
            return 'neutral'

    def _analyze_semantic_content(self, text):
        """Analiza el contenido semántico del sueño"""
        words = word_tokenize(text)
        semantic_content = {}
        
        for category, keywords in self.dream_categories.items():
            found_words = []
            for word in words:
                if word in keywords:
                    found_words.append(word)
            semantic_content[category] = {
                'words': found_words,
                'count': len(found_words),
                'percentage': len(found_words) / len(words) * 100 if words else 0
            }
        
        return semantic_content

    def _extract_entities(self, text):
        """Extrae entidades nombradas del texto"""
        blob = TextBlob(text)
        words = word_tokenize(text)
        pos_tags = pos_tag(words)
        
        entities = {
            'nouns': [],
            'verbs': [],
            'adjectives': [],
            'proper_nouns': []
        }
        
        for word, pos in pos_tags:
            if pos.startswith('NN'):  # Sustantivos
                entities['nouns'].append(word)
            elif pos.startswith('VB'):  # Verbos
                entities['verbs'].append(word)
            elif pos.startswith('JJ'):  # Adjetivos
                entities['adjectives'].append(word)
            elif pos.startswith('NNP'):  # Nombres propios
                entities['proper_nouns'].append(word)
        
        # Contar frecuencias
        for entity_type in entities:
            entities[entity_type] = dict(Counter(entities[entity_type]))
        
        return entities

    def _detect_dream_patterns(self, text):
        """Detecta patrones comunes en sueños"""
        patterns_found = {}
        
        for pattern_name, pattern_regex in self.dream_patterns.items():
            matches = re.findall(pattern_regex, text, re.IGNORECASE)
            patterns_found[pattern_name] = {
                'found': len(matches) > 0,
                'matches': matches,
                'count': len(matches)
            }
        
        return patterns_found

    def _extract_keywords(self, text):
        """Extrae palabras clave del sueño"""
        words = word_tokenize(text)
        
        # Filtrar palabras de parada y palabras muy cortas
        filtered_words = [word for word in words 
                         if word not in self.stop_words 
                         and len(word) > 2 
                         and word.isalpha()]
        
        # Contar frecuencias
        word_freq = Counter(filtered_words)
        
        # Obtener las 20 palabras más frecuentes
        top_keywords = dict(word_freq.most_common(20))
        
        return top_keywords

    def _analyze_emotions(self, text):
        """Análisis emocional avanzado"""
        emotion_words = {
            'miedo': ['miedo', 'terror', 'pánico', 'angustia', 'ansiedad', 'preocupación'],
            'alegria': ['alegría', 'felicidad', 'gozo', 'diversión', 'risa', 'sonrisa'],
            'tristeza': ['tristeza', 'melancolía', 'llanto', 'pena', 'dolor', 'sufrimiento'],
            'ira': ['ira', 'rabia', 'enojo', 'furia', 'molestia', 'irritación'],
            'sorpresa': ['sorpresa', 'asombro', 'sorprendido', 'increíble', 'inesperado'],
            'paz': ['paz', 'tranquilidad', 'calma', 'serenidad', 'relajación', 'armonía']
        }
        
        emotions_detected = {}
        words = word_tokenize(text)
        
        for emotion, emotion_words_list in emotion_words.items():
            count = sum(1 for word in words if word in emotion_words_list)
            emotions_detected[emotion] = {
                'count': count,
                'intensity': count / len(words) * 100 if words else 0
            }
        
        return emotions_detected

    def _calculate_dream_intensity(self, analysis):
        """Calcula la intensidad del sueño basada en varios factores"""
        intensity_score = 0
        
        # Factor de longitud
        if analysis['word_count'] > 100:
            intensity_score += 20
        elif analysis['word_count'] > 50:
            intensity_score += 10
        
        # Factor de sentimiento extremo
        sentiment_score = abs(analysis['sentiment']['polarity'])
        intensity_score += sentiment_score * 30
        
        # Factor de patrones de sueño
        patterns_found = sum(1 for pattern in analysis['patterns'].values() if pattern['found'])
        intensity_score += patterns_found * 10
        
        # Factor de emociones intensas
        max_emotion_intensity = max(
            emotion['intensity'] for emotion in analysis['emotional_analysis'].values()
        ) if analysis['emotional_analysis'] else 0
        intensity_score += max_emotion_intensity * 0.5
        
        # Normalizar entre 0 y 100
        intensity_score = min(intensity_score, 100)
        
        return {
            'score': round(intensity_score, 1),
            'level': self._get_intensity_level(intensity_score)
        }

    def _get_intensity_level(self, score):
        """Convierte el score de intensidad en un nivel"""
        if score >= 80:
            return 'muy alta'
        elif score >= 60:
            return 'alta'
        elif score >= 40:
            return 'moderada'
        elif score >= 20:
            return 'baja'
        else:
            return 'muy baja'

    def generate_dream_report(self, analysis):
        """Genera un reporte legible del análisis del sueño"""
        report = {
            'resumen': self._generate_summary(analysis),
            'insights': self._generate_insights(analysis),
            'recomendaciones': self._generate_recommendations(analysis)
        }
        return report

    def _generate_summary(self, analysis):
        """Genera un resumen del sueño"""
        summary = f"""
        Este sueño tiene una intensidad {analysis['dream_intensity']['level']} 
        ({analysis['dream_intensity']['score']}/100) y un sentimiento 
        {analysis['sentiment']['sentiment_label']}.
        
        Contiene {analysis['word_count']} palabras distribuidas en 
        {analysis['sentence_count']} oraciones.
        """
        
        # Agregar patrones encontrados
        patterns_found = [name for name, data in analysis['patterns'].items() if data['found']]
        if patterns_found:
            summary += f"\n\nPatrones detectados: {', '.join(patterns_found)}"
        
        return summary.strip()

    def _generate_insights(self, analysis):
        """Genera insights sobre el sueño"""
        insights = []
        
        # Insight sobre sentimiento
        sentiment = analysis['sentiment']['sentiment_label']
        if sentiment == 'positivo':
            insights.append("El sueño muestra emociones positivas, sugiriendo bienestar emocional.")
        elif sentiment == 'negativo':
            insights.append("El sueño contiene emociones negativas, posiblemente reflejando ansiedades o preocupaciones.")
        
        # Insight sobre patrones
        patterns_found = [name for name, data in analysis['patterns'].items() if data['found']]
        if 'vuelo' in patterns_found:
            insights.append("El patrón de vuelo sugiere una búsqueda de libertad o escape.")
        if 'persecucion' in patterns_found:
            insights.append("El patrón de persecución puede indicar sentimientos de presión o amenaza.")
        
        return insights

    def _generate_recommendations(self, analysis):
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        if analysis['sentiment']['sentiment_label'] == 'negativo':
            recommendations.append("Considera técnicas de relajación antes de dormir.")
        
        if analysis['dream_intensity']['score'] > 70:
            recommendations.append("Este sueño de alta intensidad puede beneficiarse de técnicas de interpretación de sueños.")
        
        patterns_found = [name for name, data in analysis['patterns'].items() if data['found']]
        if 'muerte' in patterns_found:
            recommendations.append("Los sueños sobre muerte suelen representar cambios o transformaciones.")
        
        return recommendations

# Función de utilidad para usar el analizador
def analyze_dream_text(dream_text, **kwargs):
    """Función de conveniencia para analizar un sueño"""
    analyzer = DreamAnalyzer()
    return analyzer.analyze_dream(dream_text, **kwargs)
