#!/usr/bin/env python3
"""
Script simple para compartir el servidor Django en la red local
"""
import os
import subprocess
import sys
import time

def get_local_ip():
    """Obtener la IP local"""
    try:
        # Para macOS
        result = subprocess.run(['ipconfig', 'getifaddr', 'en0'], 
                              capture_output=True, text=True)
        ip = result.stdout.strip()
        if ip:
            return ip
    except:
        pass
    
    try:
        # Alternativa para Linux/macOS
        result = subprocess.run(['hostname', '-I'], 
                              capture_output=True, text=True)
        ips = result.stdout.strip().split()
        if ips:
            return ips[0]
    except:
        pass
    
    return "127.0.0.1"

def main():
    local_ip = get_local_ip()
    
    print("=" * 60)
    print("🌐 MI COMPARADOR - SERVIDOR COMPARTIDO")
    print("=" * 60)
    print(f"�� IP local: {local_ip}")
    print(f"🚀 Servidor: http://{local_ip}:8000")
    print(f"📱 Accesible desde cualquier dispositivo en tu red WiFi")
    print("=" * 60)
    print("Para detener: Presiona Ctrl+C en la terminal del servidor")
    print("=" * 60)
    
    # Verificar si Django está corriendo
    try:
        response = os.system("curl -s http://localhost:8000 > /dev/null")
        if response != 0:
            print("❌ El servidor Django no está corriendo")
            print("Ejecuta: python manage.py runserver 0.0.0.0:8000")
            return
    except:
        pass
    
    print("✅ Servidor Django detectado")
    print("🎯 Ahora puedes compartir estas URLs:")
    print(f"   • http://{local_ip}:8000/")
    print(f"   • http://{local_ip}:8000/admin/")
    print(f"   • http://{local_ip}:8000/vuelos/buscar/")
    print(f"   • http://{local_ip}:8000/hoteles/buscar/")

if __name__ == "__main__":
    main()
