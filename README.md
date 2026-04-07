# 🔍 Android Kötücül Uygulamaların Opcode Özellikleri Kullanılarak Tespit Edilmesi

Bu proje, Android uygulamalarının **opcode (işlem kodu)** özelliklerini kullanarak *kötücül (malware) uygulamaları* tespit etmek için tasarlanmıştır.  
Static analiz yaklaşımıyla APK’lardan opcode çıkartılır ve makine öğrenmesi ile sınıflandırılır.

---

## 📌 Proje Özeti

Bu çalışmanın amaçları:

- 🛠 Android APK’larını decompile ederek opcode çıkarımı  
- 📊 Opcode özellikleri ile malware tespiti  
- 🤖 Statik analiz temelli model oluşturma  
- 🔐 Malware’a karşı daha etkin güvenlik çözümü üretmek

---

## 🧠 Kullanılan Teknolojiler

- Python  
- Flask (web arayüzü)  
- pandas, scikit-learn, xgboost, joblib  
- Opcode çıkarımı ve analiz  

---

## 🚀 Başlarken

Aşağıdaki adımlarla projeyi yerel ortamda çalıştırabilirsin:

```bash
# Repo'yu klonla
git clone https://github.com/enesuludag0/Android-Kotucul-Uygulamalari-Opcode-Ozellikleri-Kullanilarak-Tespiti.git

# Proje dizinine gir
cd opcode

# Gerekli paketleri yükle
pip install -r requirements.txt

# Projeyi çalıştır
python app.py
```

---

## 📄 Proje İşleyişi

1️⃣ APK dosyası decompile edilir.
2️⃣ Opcode’lar çıkarılır.
3️⃣ Özellikler vektör haline getirilir.
4️⃣ Model eğitimi ve sınıflandırma algoritması (xg boost) çalışır.
5️⃣ Sonuçlar web sitesinde gösterilir.

## 📱 Ekran Görüntüleri

<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/bcdebc7d-3e79-475d-9f70-61245915c37b" />
<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/ff633e56-acb7-401c-b6e2-f54c78a238d0" />
