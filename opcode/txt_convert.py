import json
import os

# JSON dosyalarının bulunduğu dizin
input_folder = "uploads/Features_files"
# Opcodes verilerini yazmak için çıkış dizini
output_folder = "outputs_txt"

# Çıkış dizini yoksa oluştur
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# JSON dosyalarını al
json_files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
total_files = len(json_files)  # Toplam JSON dosyası sayısı

# Opcodes verisini yazma
for idx, json_file in enumerate(json_files, start=1):
    json_path = os.path.join(input_folder, json_file)
    
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        # 'Opcodes' verisini al
        opcodes = data.get("Static_analysis", {}).get("Opcodes", {})
        
        if opcodes:
            # Çıkış txt dosyasının adı
            base_name = os.path.splitext(json_file)[0]
            # "-analysis" varsa kaldır
            if base_name.endswith("-analysis"):
                base_name = base_name[:-9]
            output_txt = os.path.join(output_folder, f"{base_name}.txt")
            
            with open(output_txt, 'w', encoding='utf-8') as txt_file:
                for opcode, count in opcodes.items():
                    txt_file.write(f"{opcode}: {count}\n")
        
        print(f"{idx}/{total_files} - {json_file} dosyasının Opcodes verisi txt dosyasına yazıldı.")