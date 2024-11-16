import sys
import os

# Agregar la ruta raíz del proyecto para que Python encuentre los módulos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.app import app

if __name__ == '__main__':
    app.run(debug=True)
