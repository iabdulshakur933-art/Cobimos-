import os, requests, base64
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__, template_folder='templates', static_folder='static')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')

@app.route('/')
def home():
    return render_template('public_index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/app')
def app_page():
    return render_template('app.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    if not STABILITY_API_KEY:
        return jsonify({'error':'STABILITY_API_KEY not configured'}), 500
    data = request.json or {}
    prompt = data.get('prompt','chrome cyber dragon head, metallic chrome, blue purple glow, 3D, ultra detailed, transparent background')
    samples = int(data.get('samples',1))
    url = 'https://api.stability.ai/v2beta/stable-image/generate'
    headers = {'Authorization': f'Bearer {STABILITY_API_KEY}'}
    payload = {'text_prompts':[{'text':prompt}], 'cfg_scale':7, 'steps':30, 'samples':samples}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    imgs = []
    for art in r.json().get('artifacts', []):
        b64 = art.get('base64')
        if b64:
            imgs.append('data:image/png;base64,'+b64)
    return jsonify({'images': imgs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',8080)))
