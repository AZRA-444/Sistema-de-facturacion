from http.server import BaseHTTPRequestHandler
import json
import os
import requests

# Traemos las credenciales desde las variables de entorno de Vercel
URL_SUPABASE = os.environ.get("SUPABASE_URL", "")
KEY_SUPABASE = os.environ.get("SUPABASE_SECRET_KEY", "")

class handler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """🌟 MANEJO DE CORS: Permite al navegador del cajero comunicarse con Vercel"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            # Parseamos la factura que viene desde el frontend
            factura_data = json.loads(post_data.decode('utf-8'))
            
            # Configuración de cabeceras requeridas por la API REST de Supabase
            headers_supabase = {
                "apikey": KEY_SUPABASE,
                "Authorization": f"Bearer {KEY_SUPABASE}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"  # Hace la petición más rápida al no pedir datos de vuelta
            }
            
            # 1. Hacemos el POST directo a la tabla 'ventas' por HTTP
            url_api = f"{URL_SUPABASE}/rest/v1/ventas"
            res_db = requests.post(url_api, json=factura_data, headers=headers_supabase)
            
            # Validamos si Supabase aceptó los datos (200 o 201 es éxito)
            if res_db.status_code not in [200, 201]:
                raise Exception(f"Error de Supabase ({res_db.status_code}): {res_db.text}")
            
            # 2. Respondemos con éxito al frontend del cajero
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') 
            self.end_headers()
            
            respuesta = {
                "status": "success", 
                "message": "Venta guardada exitosamente via API REST"
            }
            self.wfile.write(json.dumps(respuesta).encode('utf-8'))
            
        except Exception as e:
            # Si algo falla, devolvemos el error limpio
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_respuesta = {
                "status": "error", 
                "message": str(e)
            }
            self.wfile.write(json.dumps(error_respuesta).encode('utf-8'))
