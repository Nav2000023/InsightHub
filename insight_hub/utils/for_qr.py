import qrcode
import os
from core.settings import MEDIA_ROOT

def generate_dashboard_qr(full_url, dash_id):
    media_path = os.path.join(MEDIA_ROOT, 'qr_codes')
    os.makedirs(media_path, exist_ok=True)
    file_path = os.path.join(media_path, f"dashboard_{dash_id}.png")
    if os.path.exists(file_path):
        print("FOUND")
        pass
    else:
        img = qrcode.make(full_url)
        img.save(file_path) 
 
    return f"qr_codes/dashboard_{dash_id}.png"    