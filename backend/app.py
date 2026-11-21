from flask import Flask, request, jsonify
import jwt
import sqlite3
import datetime
import qrcode
import io
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
SECRET_KEY = "tactical_airgap_key_001" # In production, secure this locally
@app.route('/')
def home():
    return "Project Abhedya: Tactical Backend is Active and Offline."
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                (item_id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                (request_id INTEGER PRIMARY KEY, soldier_id TEXT, item_id INTEGER, status TEXT)''')
    c.execute("INSERT OR IGNORE INTO inventory (item_id, name, quantity) VALUES (1, 'INSAS Rifle', 50)")
    conn.commit()
    conn.close()

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json
    
    # 1. Cryptographically sign the approval into a JWT token
    payload = {
        'soldier_id': data.get('soldier_id'),
        'item_id': data.get('item_id'),
        'officer_id': data.get('officer_id'),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    # 2. Generate QR Code containing the signed token
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(token)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    # 3. Convert to base64 for the frontend UI to display
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return jsonify({'token': token, 'qr_image': qr_base64})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)