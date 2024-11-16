from flask import Flask, request, jsonify, g
from typing import List

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def check_stats():
    try:
        return jsonify("ok"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
