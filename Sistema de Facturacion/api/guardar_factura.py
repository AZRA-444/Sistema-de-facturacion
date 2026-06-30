from http.server import BaseHTTPRequestHandler
import json
import os
from supabase import create_client, Client

# Inicializamos Supabase usando las variables de entorno seguras de Vercel
url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_SECRET_KEY", "") # ¡Aquí sí usamos la Secret Key sin peligro!
supabase: Client = create_client(url, key)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Parseamos la factura que viene del frontend
            factura_data = json.loads(post_data.decode('utf-8'))
            
            # Insertamos directo en la tabla 'ventas' pasándole el diccionario
            response = supabase.table("ventas").insert(factura_data).execute()
            
            # Si todo sale bien, respondemos con éxito
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Venta guardada"}).encode('utf-8'))
            
        except Exception as e:
            # Si algo falla (ej. ID duplicado o error de Supabase), devolvemos el error limpio
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))