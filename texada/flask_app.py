from flask import Flask
texada_api = Flask("texada_api")

@texada_api.route("/")
def root():
	return "<h1>Welcome to Xintong's project!/</h1>"


if __name__ == '__main__':
    texada_api.run()
