""" hello.py """
import traceback

from flask import Flask, jsonify

from database import Database

app = Flask(__name__)

@app.route('/')
def hello():
    print 'Came here'
    # db_mgr = Database()
    try:
        db_mgr = Database()
        return jsonify({
            'hello': 'world'
        })
    except:
        traceback.print_exc()
    finally:
        db_mgr.connection_close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
