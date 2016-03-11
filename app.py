from flask import Flask
from flask import request
import json
from random import random

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

def histogramGen(dx,dy,dz,cutoff,data):
	
	ii = 0
	
	success_tot = 0
	count_tot = 0

	box_data = []
	
	while ii < cutoff:
	
		success, box = cube(random(),random(),random(),dx,dy,dz,data)
		count = np.size(box)/3
	
		success_tot += success
		count_tot += count
	
		if success == 1:
			box_data.append(count)
	
		ii += 1
	
	#histogram of galaxy density
	hist, bin = np.histogram(box_data,bins=cutoff/5,range=(0,np.max(box_data)))
	
	#poisson distribution
	mu = np.mean(box_data)
	#pois = np.random.poisson(mu,cutoff*10)
	
	#might want to swap out box_data for hist? not sure depends on how
	#you're plotting it
	return box_data, hist, bin

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

    elif request.args.get('dx', ''):
        dx = float(request.args.get('dx', ''))
        dy = float(request.args.get('dy', ''))
        dz = float(request.args.get('dz', ''))

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

        box_data, hist, bin = histogramGen(dx,dy,dz,500,rpos)
        #return json.dumps([hist.tolist(),bin.tolist()])
        return '<!doctype html><html><head><title>Bar Chart</title><script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/1.0.2/Chart.min.js"></script></head><body><h1>Galaxy Density</h1><p>'+json.dumps([hist.tolist(),bin.tolist()])+'</p><div style="width: 100%"><canvas id="canvas" height="450" width="1000"></canvas></div><script>var randomScalingFactor = function(){ return Math.round(Math.random()*100)};var barChartData = {labels : '+json.dumps(bin.tolist())+',datasets : [{fillColor : "rgba(220,220,220,0.5)",strokeColor : "rgba(220,220,220,0.8)",highlightFill: "rgba(220,220,220,0.75)",highlightStroke: "rgba(220,220,220,1)",data : '+json.dumps(hist.tolist())+'}]};window.onload = function(){var ctx = document.getElementById("canvas").getContext("2d");window.myBar = new Chart(ctx).Bar(barChartData, {responsive : true });}</script></body></html>'

    else:
        return "<h1>Welcome to GalaxyQuest</h1> <h3>Use:<h3><ul><li>http://galaxyquest.herokuapp.com?xpos=0&ypos=0&zpos=0&dx=0.1&dy=0.1&dz=0.1</li></ul>"    

if __name__ == "__main__":
    app.run(debug=True)

