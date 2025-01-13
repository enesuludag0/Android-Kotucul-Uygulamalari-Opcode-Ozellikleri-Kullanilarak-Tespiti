import os
import pandas as pd
import shutil
import joblib
from flask import Flask, render_template, request, jsonify
from opcode_extractor import extract_opcode_features
from train_model import data

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs_txt'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Yükleme ve çıktı klasörlerinin oluşturulması
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Model ve scaler yolları
MODEL_PATH = "model.pkl"
SCALER_PATH = "scaler.pkl"

# Modeli ve scaler'ı yükleme
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# .txt dosyasını okuyan fonksiyon
def read_opcode_txt(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        data = {}
        for line in file:
            opcode, count = line.strip().split(':')
            data[opcode.strip()] = int(count.strip())
    return data

# Modeldeki sütunlara göre opcode verilerini hizalayan fonksiyon
def align_features(opcode_features, model_columns):
    return {col: opcode_features.get(col, 0) for col in model_columns}  # Eksik olan değerler için 0 kullan

# Ana sayfa (APK yükleme formu) yönlendirme fonksiyonu
@app.route("/")
def index():
    return render_template("apk_load.html")

# Yüklenen dosyayı işleyen fonksiyon
@app.route('/upload', methods=['POST'])
def upload_file():
    # uploads klasöründeki tüm dosyaları temizle
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)  # Alt klasörü ve içeriğini sil

    # Yükleme kısmında dosya olup olmadığını kontrol et
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400  # Dosya kısmı eksikse hata döndür
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400  # Dosya seçilmediyse hata döndür

    # Dosyanın kaydedileceği yolu belirle
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # Opcode çıkarma fonksiyonunu çağır ve sonucu al
    result = extract_opcode_features(app.config['UPLOAD_FOLDER'])
    if not result["success"]:
        return jsonify(result)  # Eğer opcode çıkarma başarısızsa hata döndür

    # Çıkarılan opcode özelliklerini txt dosyasından oku
    txt_file = os.path.join(app.config['OUTPUT_FOLDER'], f"{os.path.splitext(file.filename)[0]}.txt")
    opcode_features = read_opcode_txt(txt_file)

    # Modelde kullanılan özellik sütunlarını al
    model_columns = list(data.drop(columns=["file_name", "label"]).columns)
    
    # Opcode verilerini modelin beklentilerine göre hizala
    aligned_features = align_features(opcode_features, model_columns)

    # Özellikleri ölçeklendir ve modelin tahminini yap
    apk_features_df = pd.DataFrame([aligned_features])  # Özellikleri DataFrame olarak oluştur
    apk_features_scaled = scaler.transform(apk_features_df)  # Sütun isimleriyle uyumlu hale getir
    prediction = model.predict(apk_features_scaled)
    prediction_proba = model.predict_proba(apk_features_scaled)[:, 1]

    results = {
        'prediction': 'Malware' if prediction[0] == 1 else 'Benign',
        'probability': round(float(prediction_proba[0]), 4)
    }

    return render_template("apk_analysis_result.html", results=results)

if __name__ == '__main__':
    app.run()