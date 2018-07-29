from flask import Flask

from teachtime.routes import routes
from teachtime.config import Config

def create_app(config=Config):
	# Flask initialisation and config
	app = Flask(__name__)
	app.config.from_object(config)

	# TeachTime blueprints
	app.register_blueprint(routes)

	return app

if __name__ == '__main__':
	app = create_app()
	app.run(debug=True)
