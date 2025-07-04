from flask import Flask, render_template
from dotenv import load_dotenv
from bot.routes import bot_bp

def create_app():
    # Cargar variables del .env
    load_dotenv()

    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Registrar blueprint del bot
    app.register_blueprint(bot_bp, url_prefix="/api")

    # Ruta principal (página de la clínica)
    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
