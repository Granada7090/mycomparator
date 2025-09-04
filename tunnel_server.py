from flask import Flask, redirect
import threading
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Esta será tu URL temporal
TEMPORARY_URL = None
URL_EXPIRY = None

@app.route('/')
def home():
    return redirect('http://172.20.10.2:8000')

@app.route('/travelpayouts/webhook', methods=['POST'])
def travelpayouts_webhook():
    """Webhook para TravelPayouts"""
    # Aquí procesarías los datos de TravelPayouts
    return {"status": "success", "message": "Webhook received"}

def get_public_ip():
    """Obtener IP pública"""
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except:
        return "No se pudo obtener IP pública"

def start_tunnel():
    global TEMPORARY_URL, URL_EXPIRY
    
    public_ip = get_public_ip()
    if public_ip != "No se pudo obtener IP pública":
        TEMPORARY_URL = f"http://{public_ip}:5000"
        URL_EXPIRY = datetime.now() + timedelta(hours=24)
        
        print("=" * 60)
        print("🌐 TUNEL TEMPORAL PARA TRAVELPAYOUTS")
        print("=" * 60)
        print(f"📍 Tu IP pública: {public_ip}")
        print(f"🔗 URL temporal: {TEMPORARY_URL}")
        print(f"⏰ Válida por: 24 horas")
        print(f"🌍 Webhook: {TEMPORARY_URL}/travelpayouts/webhook")
        print("=" * 60)
        print("⚠️  Esta URL es temporal y cambiará si reinicias")
        print("=" * 60)
    else:
        print("❌ No se pudo obtener IP pública")

if __name__ == '__main__':
    # Iniciar en un hilo separado
    tunnel_thread = threading.Thread(target=start_tunnel)
    tunnel_thread.start()
    
    # Ejecutar Flask en puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=False)
