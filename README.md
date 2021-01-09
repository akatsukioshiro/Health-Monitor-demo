# Health-Monitor-demo
ESP32 with temperatue sensor that constantly updates Flask main server with temperature etc. This main server displays this in webpage. Expected to work as proper health monitoring tool.

# Features
1. Flask Server
2. Arduino program for ESP32
3. Connects to GMAIL

# Working
1. Flask acts as main server.
2. ESP32 acts as agents.
3. These ESP32s utilize arduino's C code, currentlu borrowed from online sources(unclear/forgotten, sorry...)
4. These ESP32 codes have been modified to meet the ends for now.
5. Once perfect, I'll be shifting to micropython to do the same.
6. Multiple ESPs can be supported, all data will be stored in json in background.
7. A DB could be better choice, will be there in next release.
8. Based on Wifi signal, we are expected to see if 2 people (each carrying one ESP32) breach safety proximity.
9. If either is detected/has been documenetd with Fever/spreadable ailment, the later will receive mail(not implemented yet)

Work in progress.

README file also in progress.
