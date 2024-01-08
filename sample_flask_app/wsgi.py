from gevent.pywsgi import WSGIServer
from flask_cors import CORS
from app import create_app
from gevent import monkey
monkey.patch_all()
app = create_app()
CORS(app)

if __name__ == "__main__":
    http_server = WSGIServer(("0.0.0.0", 5001), app)
    http_server.serve_forever()
    # app.run(host="0.0.0.0",port=5001)
