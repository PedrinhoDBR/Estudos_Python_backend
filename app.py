from app import create_app
from flask_cors import CORS
import os

app = create_app()
CORS(app)

app.secret_key = os.environ.get('SECRET_KEY', 'default_key')

if __name__ == '__main__':
    app.run(debug=True)
