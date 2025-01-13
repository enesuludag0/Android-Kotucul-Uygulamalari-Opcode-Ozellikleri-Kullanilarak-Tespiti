import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import joblib

# Veri setini yükle
file_path = 'opcode.csv'

# Veriyi CSV dosyasından yükleme
data = pd.read_csv(file_path)

# 'file_name' sütununun temizlenmesi
data_cleaned = data.drop("file_name", axis=1)

# Etiketlerin 0 (benign) ve 1 (malware) olarak dönüştürülmesi
data_cleaned["label"] = data_cleaned["label"].map({"benign": 0, "malware": 1})

# Özellikler (X) ve etiketler (y) ayrılması
X = data_cleaned.drop("label", axis=1)
y = data_cleaned["label"]

# Eğitim ve test setlerine ayır (%80 eğitim, %20 test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Model ve scaler dosyalarını kontrol et
model_path = "model.pkl"
scaler_path = "scaler.pkl"

if os.path.exists(model_path) and os.path.exists(scaler_path):
    print(f"{model_path} ve {scaler_path} mevcut.")
    # Mevcut model ve scaler'ı yükle
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
else:
    # Özellikleri ölçeklendir
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

    # Modeli tanımla ve eğit
    model = XGBClassifier(
        random_state=42,
        eval_metric='logloss',
        learning_rate=0.05,    # Küçük öğrenme oranı
        n_estimators=2500,     # Ağaç sayısını artır
        max_depth=8,          # Derinliği artır
        subsample=0.9,         # Veri alt kümesi büyüklüğünü artır
        colsample_bytree=0.9,   # Özelliklerin alt kümesi büyüklüğünü artır
    )
    model.fit(X_train_scaled, y_train)

    # Modeli ve scaler'ı dosyaya kaydet
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Model ({model_path}) ve scaler ({scaler_path}) dosyaları kaydedildi.")

# Test verisiyle doğrulama yap
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)
accuracy = model.score(X_test_scaled, y_test)
print(f"Accuracy: {accuracy:.4f}")


# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from xgboost import XGBClassifier
# import joblib

# # Veri setini yükle
# file_path = 'opcode.csv'

# # Veriyi CSV dosyasından yükleme
# data = pd.read_csv(file_path)
    
# # 'file_name' sütununun temizlenmesi
# data_cleaned = data.drop("file_name", axis=1)
    
# # Etiketlerin 0 (benign) ve 1 (malware) olarak dönüştürülmesi
# data_cleaned["label"] = data_cleaned["label"].map({"benign": 0, "malware": 1})

# # Özellikler (X) ve etiketler (y) ayrılması
# X = data_cleaned.drop("label", axis=1)
# y = data_cleaned["label"]

# # Eğitim ve test setlerine ayır (%80 eğitim, %20 test)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# # Özellikleri ölçeklendir
# scaler = StandardScaler()
# X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
# X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

# # Modeli tanımla ve eğit
# model = XGBClassifier(
#     random_state=42,
#     eval_metric='logloss',
#     learning_rate=0.05,    # Küçük öğrenme oranı
#     n_estimators=2500,     # Ağaç sayısını artır
#     max_depth=8,          # Derinliği artır
#     subsample=0.9,         # Veri alt kümesi büyüklüğünü artır
#     colsample_bytree=0.9,   # Özelliklerin alt kümesi büyüklüğünü artır
# )
# model.fit(X_train_scaled, y_train)

# # Modeli ve scaler'ı dosyaya kaydet
# joblib.dump(model, "model.pkl")
# joblib.dump(scaler, "scaler.pkl")
# print(f"Model (model.pkl) ve scaler (scaler.pkl) dosyaları kaydedildi.")

# accuracy = model.score(X_test_scaled, y_test)
# print(f"Accuracy: {accuracy:.4f}")