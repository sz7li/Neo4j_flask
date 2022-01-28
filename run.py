from gevent.pywsgi import WSGIServer
from flask_app import app

if __name__ == '__main__':  
    print("Hosting flask ...")
    app.run(host="localhost", port=8000, threaded=True)
    