# Compatible with python 3.6 and 3.7 version
import sys
import os.path
from iotconnect import IoTConnectSDK
import json
import time
import raspi
from datetime import datetime

def callbackMessage(msg):
    if msg:
        print("\n--- Command Message Received ---")
        print(str(msg['ack']))
        print(str(msg['ackId']))
        print(str(msg['command']))
        print(str(msg['uniqueId']))

def callbackTwinMessage(msg):
    if msg:
        print("\n--- Twin Message Received ---")
        print(json.dumps(msg))
        if msg.get("desired"):
            if msg["desired"]["light"] == "ON":
                turn_on()
            if msg["desired"]["light"] == "OFF":
                raspi.turn_off()
        if msg.get("light"):
            if msg["light"] == "ON":
                raspi.turn_on()
            if msg["light"] == "OFF":
                raspi.turn_off()

def main(argv):
    try:
        env = "PROD"
        if(argv[1] is not None):
            env = argv[1]
        
        uniqueId = input("Enter device serial number : ").rstrip()
        cpId = input("Enter CPID : ").rstrip()
        
        with IoTConnectSDK(cpId, uniqueId, callbackMessage, callbackTwinMessage, env) as sdk:
            try:
                raspi.setup()
                input_val = 'y'
                while input_val == 'y':
                    devices = sdk.GetAttributes()
                    if len(devices) > 0:
                        dataArray = []
                        for device in devices:
                            if device["tg"] == "":
                                print("\n[Device Id :: %s]" % device["id"])
                            else:
                                print("\n## TAG :: %s [Device Id :: %s]" % (device["tg"], device["id"]))
                            aObj = {}
                            for attribute in device["attr"]:
                                if attribute["p"] == "":
                                    for prop in attribute["d"]:
                                        val = input(
                                            "Enter " + prop["ln"] + " : ").rstrip()
                                        if val != "":
                                            aObj[prop["ln"]] = val
                                else:
                                    print("Enter " + attribute["p"] + " :")
                                    aObj[attribute["p"]] = {}
                                    for prop in attribute["d"]:
                                        val = input(
                                            "  Enter " + prop["ln"] + " : ").rstrip()
                                        if val != "":
                                            aObj[attribute["p"]][prop["ln"]] = val
                            if len(aObj.items()) > 0:
                                dObj = {
                                    "uniqueId": device["id"],
                                    "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                                    "data": aObj
                                }
                                dataArray.append(dObj)
                        
                        if len(dataArray) > 0:
                            sdk.SendData(dataArray)
                        input_val = input("\nWould you like to send data again ? (Y/N) : ")
                        input_val = input_val.lower().rstrip()
                    else:
                        input_val = "exit"
            except KeyboardInterrupt:
                raspi.destroy()
                sys.exit(0)
    except Exception as ex:
        raspi.destroy()
        print(ex.message)
        sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
