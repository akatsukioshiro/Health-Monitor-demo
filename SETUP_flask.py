import logging
try:
    logging.basicConfig(filename='LOG_runtime.log', filemode='a', format='%(levelname)s - %(asctime)s - %(message)s', level=logging.INFO)
except FileNotFoundError:
    with open("runtime.log","w+") as f:
        f.write("")
    logging.basicConfig(filename='LOG_runtime.log', filemode='a', format='%(levelname)s - %(asctime)s - %(message)s', level=logging.INFO)
except Exception as e:
    print(e)

try:
    import socket
    from jinja2 import Template
    import argparse
except Exception as e:
    logging.critical(str(e))


parser = argparse.ArgumentParser()

parser.add_argument('-ip', dest = 'ip_address', action = 'store', help = 'collect ipaddress') 
parser.add_argument('-get', dest = 'ip', action = 'store', help = 'show ipaddress') 
parser.add_argument('-port', dest = 'port', action = 'store', help = 'collect port') 

args = parser.parse_args()

def update(ipaddress,port):
    try:
        with open("./templates/APP_flask_server.template","r") as f:
            flask=f.read()
        with open("APP_flask_server.py","w") as f:
            f.write(Template(flask).render(ipaddress=ipaddress,port=port))
    except Exception as e:
        logging.critical(str(e))

if args.ip=="ip":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        print("Getting IP...")
    except OSError as e:
        print("\n"+str(e)+". Possibly WiFi not connected.\n")
        logging.warning(str(e)+". Possibly WiFi not connected.\n")
        print("Exiting ...")
        exit()
    ipaddress=str(s.getsockname()[0]).strip()
    print(ipaddress)
    logging.info("Show current IP: "+ipaddress)
    exit()

if args.ip_address!=None and args.port!=None:
    
    ipaddress=str(args.ip_address).strip()
    port=str(args.port).strip()
    print("Manualy set ip to: "+str(args.ip_address))
    print("Manualy set port to: "+str(args.port))
    logging.info("Manualy set Flask Server ip to: "+str(args.ip_address))
    logging.info("Manualy set Flask Server port to: "+str(args.port))
    update(ipaddress,port)
    
elif args.ip_address==None and args.port!=None:
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        print("Auto set ip to: "+str(s.getsockname()[0]).strip())
        print("Manualy set port to: "+str(args.port))
        logging.info("Auto set Flask Server ip to: "+str(s.getsockname()[0]).strip())
        logging.info("Manualy set Flask Server port to: "+str(args.port))
    except OSError as e:
        print("Auto Set failed.")
        print("\n"+str(e)+". Possibly WiFi not connected.\n")
        logging.warning(str(e)+". Possibly WiFi not connected.\n")
        print("Exiting ...")
        exit()
    ipaddress=str(s.getsockname()[0]).strip()
    port=str(args.port).strip()
    update(ipaddress,port)

else:
    if args.port==None:
        print("Please enter port. Usage: py/python.exe/python3 SETUP_flask.py -port 5001")
        logging.warning("Please enter port.")



