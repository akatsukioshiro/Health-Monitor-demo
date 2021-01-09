from flask import Flask, jsonify, request, Response
import subprocess
import json
import IMP_json_collector as jc
from time import sleep
app = Flask(__name__)

STATE=False

@app.route("/begin_loop",methods=['GET'])
def begin_loop():
	global STATE
	STATE=False
	if request.method == 'GET':
		if request.args.get("device") == "esp32":
			
			with open("DB_registerred_devices.json","r") as rd:
				data_rd=json.loads(rd.read().replace("'","\""))
			
			if request.remote_addr in data_rd["devices"] and STATE == False:
				STATE = True
			elif request.remote_addr not in data_rd["devices"] and STATE == False:
				STATE = True
				with open("DB_registerred_devices.json","w") as rd:
					data_rd["devices"].append(str(request.remote_addr).strip())
					pretty=json.dumps(data_rd, sort_keys=True, indent=4)
					rd.write(pretty)
					
			while STATE:
				jc.ping_esp32()
				sleep(5)

@app.route("/test",methods=['GET'])
def test():		
	return "All Good - Testing"

@app.route("/",methods=['GET'])
def home():
	if request.method == "GET":
		with open("WEBSITE_data.html","r") as f:
			data=f.read().replace("CURR_IP","192.168.1.10")
		return data


@app.route("/database",methods=['GET'])
def database():
	database="{}"
	with open("DB_database.json","r") as data:
		database=str(data.read()).replace("'","\"")
	resp = Response(database)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

if __name__ == '__main__':
  print("Client Hits URL: "+"http://192.168.1.10:5001/begin_loop?device=esp32")
  app.run(host='192.168.1.10', port=5001)