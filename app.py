from flask import Flask
from flask import request
import json

app = Flask(__name__)

import numpy as np

def cube(xpos,ypos,zpos,dx,dy,dz,data):

  #check validity of box

  if xpos + dx > 1 or ypos + dy > 1 or zpos + dz > 1:
    return 0, 0

  else:

    xsort = []
    for x in data:
      if x[0] > xpos and x[0] < xpos + dx:
        xsort.append(x)

    xysort = []
    for y in xsort:
      if y[1] > ypos and y[1] < ypos + dy :
        xysort.append(y)

    xyzsort = []
    for z in xysort:
      if z[2] > zpos and z[2] < zpos + dz:
        xyzsort.append(z)

    return 1, np.array(xyzsort)

#data holds all position data as tuples [[x,y,z], ...]

@app.route("/")

def hello():
  if request.args.get('xpos', ''):
    xpos = float(request.args.get('xpos', ''))
    ypos = float(request.args.get('ypos', ''))
    zpos = float(request.args.get('zpos', ''))

    dx = float(request.args.get('dx', ''))
    dy = float(request.args.get('dy', ''))
    dz = float(request.args.get('dz', ''))

    print xpos
    print ypos
    print zpos
    print dx
    print dy
    print dz

    xpos_data = np.load('data/x.npy')
    ypos_data = np.load('data/y.npy')
    zpos_data = np.load('data/z.npy')

    # mass = np.load('data/stellar_masses.npy')
    # SFR = np.load('data/SFRs.npy')

    #normalise data
    xpos_data = xpos_data/400000
    ypos_data = ypos_data/400000
    zpos_data = zpos_data/400000

    rpos = zip(xpos_data,ypos_data,zpos_data) 

    success,data = cube(xpos,ypos,zpos,dx,dy,dz,rpos)
    return json.dumps(data.tolist())
    # return "<h1>GalaxyQuest Result</h1>"

  else:
    return "<h1>Welcome to GalaxyQuest</h1> <h3>Use:<h3><ul><li>http://galaxyquest.herokuapp.com?xpos=0&ypos=0&zpos=0&dx=0.1&dy=0.1&dz=0.1</li></ul>"    

if __name__ == "__main__":
    app.run(debug=True)

