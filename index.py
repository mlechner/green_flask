from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Marcos flask testing'

@app.route('/areas/get', methods=['GET'])
def areas_get():
    return 'Areas returned:'

@app.route('/area/get/<int:id>', methods=['GET'])
def area_get(id):
    return 'Area %d returned.' % id

@app.route('/area/add', methods=['GET', 'POST'])
def area_add():
    if request.method == 'POST':
        return 'New area added using POST.'
    else:
        return 'New area added using GET.'

@app.route('/area/edit/<int:id>', methods=['GET', 'POST'])
def area_edit(id):
    return 'Area %d edited:' % id

if __name__ == '__main__':
    app.run(host='0.0.0.0')
