
def clean():

	data="""{
    	"devices": []
	}
	"""

	with open("DB_registerred_devices.json","w+") as f:
		f.write(data)

clean()
