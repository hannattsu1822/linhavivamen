from flask import Flask
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Substituímos Flask-MySQLdb por conexão direta com PyMySQL
mysql = pymysql

def create_app():
    # Configuração de caminhos
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    app = Flask(__name__,
               template_folder=os.path.join(base_dir, 'templates'),
               static_folder=os.path.join(base_dir, 'static'))
    
    # Configurações
    app.config.update({
        'SECRET_KEY': os.getenv('SECRET_KEY') or 'fallback_secret_key',
        # Configurações do MySQL usando PyMySQL
        'MYSQL_HOST': 'yamanote.proxy.rlwy.net',
        'MYSQL_USER': 'root',
        'MYSQL_PASSWORD': 'YapHJHzRdhESbzsQdtdqvbvNRcSpeNpw',
        'MYSQL_DB': 'railway',
        'MYSQL_PORT': 51790,
        'MYSQL_CURSORCLASS': 'DictCursor',
        'MYSQL_CONNECT_TIMEOUT': 10,  # Adicionado timeout
        'UPLOAD_FOLDER': os.path.join(base_dir, 'uploads'),
        'MAX_CONTENT_LENGTH': 16 * 1024 * 1024  # 16MB
    })

    # Cria pasta de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Conexão com o banco de dados
    @app.before_request
    def before_request():
        app.mysql_conn = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            port=app.config['MYSQL_PORT'],
            cursorclass=pymysql.cursors.DictCursor
        )

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(app, 'mysql_conn'):
            app.mysql_conn.close()
    
    from . import routes, auth
    app.register_blueprint(routes.main_bp)
    app.register_blueprint(auth.auth_bp)
    
    return app
