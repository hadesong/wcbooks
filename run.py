from app_package import app


host = app.config['HOST']
port = app.config['PORT']
debug = app.config['DEBUG']

if __name__ == '__main__':
	app.run(host=host ,port=port , debug=debug)