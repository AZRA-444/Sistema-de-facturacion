from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Credenciales de Supabase
URL = "https://etfdwjbgrbxfuoltpgqa.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV0ZmR3amJncmJ4ZnVvbHRwZ3FhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4Mjc5ODQ0NCwiZXhwIjoyMDk4Mzc0NDQ0fQ.KWagsCbHPN-HfUI7fvteZPTjqn81G376V4K-sIZSzW4"

@app.route('/api/guardar_factura', methods=['POST'])
def guardar_factura():
    try:
        factura_data = request.json
        
        # Guardar directamente en la base de datos de Supabase
        headers_supabase = {
            "apikey": KEY,
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        res_db = requests.post(f"{URL}/rest/v1/ventas", json=factura_data, headers=headers_supabase)
        
        # Validar si Supabase aceptó los datos
        if res_db.status_code not in [200, 201]:
            return jsonify({"status": "error", "message": f"Error DB: {res_db.text}"}), 400

        # Respuesta de éxito simplificada
        return jsonify({
            "status": "success", 
            "message": "Factura registrada exitosamente."
        }), 200
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Servidor de Facturación corriendo")