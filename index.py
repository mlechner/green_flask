from flask import Flask
from flask import request
from flask import render_template
from sqlalchemy import *
from sqlalchemy.orm import *
import geojson
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from geoalchemy import *
from geoalchemy.spatialite import SQLiteComparator
from pysqlite2 import dbapi2 as sqlite

app = Flask(__name__)

engine = create_engine('sqlite:////tmp/green_flask.db', module=sqlite, echo=True)
connection = engine.raw_connection().connnection
connection.enable_load_extension(True)
metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.execute("select load_extension('/usr/local/lib/libspatialite.so')")
Base = declarative_base(metadata=metadata)

class Area(Base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=True)
    geom = GeometryColumn(MultiPolygon(2))
    
GeometryDDL(Area,__table__)

@app.route('/')
def hello_world():
    return 'Marcos flask testing'

@app.route('/areas', methods=['GET'])
def areas_get():
    return geojson.dumps(polycoll)

@app.route('/area/get/<int:id>', methods=['GET'])
def area_get(id):
    return 'Area %d returned.' % id

@app.route('/area/add', methods=['GET', 'POST'])
def area_add():
    r = request
    if request.method == 'POST':
        mypoly = geojson.loads(r.data)
        print mypoly
        for feature in mypoly.features:
            polycoll.features.append(feature)
        polystr = geojson.dumps(polycoll)
        return polystr
    else:
        return 'New area added using GET.'

@app.route('/area/edit/<int:id>', methods=['GET', 'POST'])
def area_edit(id):
    return 'Area %d edited:' % id

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == '__main__':
    metadata.create_all()
    app.run(host='0.0.0.0')
