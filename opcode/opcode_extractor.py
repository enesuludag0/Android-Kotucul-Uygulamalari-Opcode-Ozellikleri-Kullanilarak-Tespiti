import os
import subprocess

def extract_opcode_features(upload_folder):
    """
    AndroPyTool ile APK'dan opcode çıkartma işlemini gerçekleştirir.
    """
    try:
        # AndroPyTool Docker komutunu çalıştır
        result = subprocess.run(
            ['docker', 'run', '--volume', f'{os.path.abspath(upload_folder)}:/apks', 'alexmyg/andropytool', '-s', '/apks/'],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            return {"success": False, "error": "AndroPyTool işlemi sırasında hata oluştu.", "details": result.stderr}
        
        # txt_convert.py dosyasını çalıştır
        extractor_result = subprocess.run(
            ['python', 'txt_convert.py'],  # txt_convert.py'yi çalıştır
            capture_output=True, text=True
        )
        
        if extractor_result.returncode != 0:
            return {"success": False, "error": "txt_convert.py çalıştırılamadı.", "details": extractor_result.stderr}
        
        return {"success": True, "message": "Opcode extraction completed successfully.", "details": extractor_result.stdout}

    except Exception as e:
        return {"success": False, "error": "AndroPyTool çalıştırılamadı.", "details": str(e)}