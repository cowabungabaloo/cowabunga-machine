from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check_code', methods=['POST'])
def check_code():
    data = request.json
    code = data.get('code')
    
    try:
        response = requests.post(
            'https://app.sophia.org/billing/subscription/check_code',
            json={'code': code, 'plan': 'monthly_membership'},
            timeout=10
        )
        
        if response.status_code != 200:
            return jsonify({'status': 'error', 'message': 'API request failed'}), 500
        
        result = response.json()
        
        if 'error' in result and result['error']:
            return jsonify({'status': 'used', 'data': result})
        else:
            return jsonify({'status': 'available', 'data': result})
            
    except requests.exceptions.RequestException as e:
        print(f"Error checking code {code}: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
