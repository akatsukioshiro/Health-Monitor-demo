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
    from jinja2 import Template
    import json
except Exception as e:
    logging.critical(str(e))


def update(ipaddress,port,w_id,w_pass,ap_id,ap_pass,i_mail):
    try:
        with open("./templates/arduino_esp32_agent.template","r") as f:
            arduino=f.read()
        with open("./arduino_esp32_agent/arduino_esp32_agent.ino","w") as f:
            f.write(Template(arduino).render(ipaddress=ipaddress,port=port,ap_id=ap_id,ap_pass=ap_pass,wifi_id=w_id,wifi_pass=w_pass,identity_email=i_mail))
    except Exception as e:
        logging.critical(str(e))
try:
    with open("CONFIG_configuration.json","r") as f:
        data = json.loads(f.read().replace("'","\""))
except FileNotFoundError as e:
    logging.critical(str(e))
    print(e)
    print("Exiting ...")
    exit()
try:
    ipaddress=data["flask_server_ip"]
    port=data["flask_server_port"]
    ap_id=data["AP_ssid_esp32"]
    ap_pass=data["AP_pass_esp32"]
    w_id=data["wifi_ssid_esp32"]
    w_pass=data["wifi_pass_esp32"]
    i_mail=data["agent_identification_email"]
    update(ipaddress,port,w_id,w_pass,ap_id,ap_pass,i_mail)
except KeyError as e:
    logging.error(str(e))
    print(str(e))
    print("configuration file has issues.")

