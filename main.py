
import time
import ujson

import onewire
import ds18x20
# Complete project details at https://RandomNerdTutorials.com/micropython-programming-with-esp32-and-esp8266/

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'heatbooster/AlhierHB/fan-speed': #and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  
  
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def create_ha_device():
    discoveryTopic = 'homeassistant/device/' +device + '/config'
    print (discoveryTopic)
    doc = {"dev": {
        "ids": "e465b851d7c4",
        "name": "DS18B20",
        "mf": "Alhier",
        "mdl" : "thermometer",
        "sw": "0.1",
        "sn": "e465b851d7c4",
        "hw": "0.1",
      },
      "o": {
        "name":"bla2mqtt",
        "sw": "2.1",
        "url": "https://bla2mqtt.example.com/support",
      },
        "cmps": {
            unique_device_0 : {
              "p": "sensor",
              "device_class":"temperature",
              "name": "temp_0",
              "unit_of_measurement":"Celsius",
              "state_topic": state_topic_0,
              "unique_id":unique_device_0,
             },
            unique_device_1: {
             "p": "sensor",
              "device_class":"temperature",
              "name": "temp_1",
              "unit_of_measurement":"Celsius",
              "state_topic": state_topic_1,
              "unique_id":unique_device_1,
             },
#            unique_device_2: {
#             "p": "sensor",
#              "device_class":"temperature",
#              "name": "temp_2",
#              "unit_of_measurement":"Celsius",
#              "state_topic": state_topic_2,
#              "unique_id":unique_device_2,
#             },
        },
    }
    buffer = ujson.dumps(doc)
    print('buffer: ',buffer)
    client.publish(discoveryTopic,buffer)
    
# max number of temperature sensors on a DS18B20 is 3
# 2 are connected 
device ='DS18B20'
name_device_0 ='DS18B20_0'
name_device_1 ='DS18B20_1'
name_device_2 ='DS18B20_2'
id_device_0 = name_device_0 
id_device_1 = name_device_1
id_device_2 = name_device_2
#unique_device = device + '_' + mac_address.replace(':','')
unique_device_0 = name_device_0 + '_' + mac_address.replace(':','')
unique_device_1 = name_device_1 + '_' + mac_address.replace(':','')
unique_device_2 = name_device_2 + '_' + mac_address.replace(':','')
state_topic_0 = unique_device_0 + "/state"
state_topic_1 = unique_device_1 + "/state"
state_topic_2 = unique_device_2 + "/state"

state_topic =[unique_device_0 + "/state",unique_device_1 + "/state",unique_device_2 + "/state"]




#off during testing
client = connect_and_subscribe()
create_ha_device()





#client.publish(state_topic_0, "10.00")
#client.publish(state_topic_1, "20.00")
#client.publish(state_topic_2, "-")
#time.sleep(1)




ds_pin = machine.Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found DS devices: ', roms)
print (len(roms))
t=[0,1,2]
stringt=[0,0,0]
while True:
  ds_sensor.convert_temp()
  time.sleep_ms(750)
  for i in range (0,len(roms)):
      t[i]= ds_sensor.read_temp(roms[i])
      stringt[i] = '%.2f' %  (t[i])
      print(i,stringt[i])
   
      print (state_topic[i], stringt[i])
      client.publish(state_topic[i], stringt[i])

    
  time.sleep(5)



