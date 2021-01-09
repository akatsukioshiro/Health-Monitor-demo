import urllib.request
import json
from datetime import datetime

def ping_esp32():
	with open("DB_registerred_devices.json","r") as rd:
		data_rd=json.loads(str(rd.read()).replace("'","\""))
	
	for ip in data_rd["devices"]:
		esp32_url="http://"+ip


		try:
			data = urllib.request.urlopen(esp32_url).read()
			if isinstance(data,bytes) == True:
				data=str(data,"utf-8")
			data=data.replace("'","\"")
			data=json.loads(data)
			try:
				with open("DB_database.json","r") as f:
					db=json.loads(f.read())
			except json.decoder.JSONDecodeError as e:
				print("Database Corrupted, taking backup, starting fresh")
				with open("DB_database.json","r") as f:
					timestamp=datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
					with open("database.json_"+timestamp,"w+") as nf:
						nf.write(f.read())
				with open("DB_database.json","w+") as g:
					g.write("{}")

				with open("DB_database.json","r") as t:
					db=json.loads(t.read())

			data["client_id"]=ip	

			wnames=[]
			for wn in data["wifi_names"]:
				if wn.strip() == "":
					continue
				wnames.append(wn)

			data["wifi_names"]=wnames

			wids=[]
			for wi in data["wifi_ids"]:
				if wi.strip() == "":
					continue
				wids.append(wi)

			data["wifi_ids"]=wids

		
			db[datetime.now().strftime("%Y-%m-%d %H:%M:%S")]=data

			pretty=json.dumps(db, sort_keys=True, indent=4)

			with open("DB_database.json","w+") as f:
				f.write(pretty)

			print(data)
		except urllib.error.URLError:
			print(ip+" - Not Transmitting Anymore")
