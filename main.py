import os
from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import timedelta, datetime
import random
import uuid
import time

SEATTLE_COORDINATES ={ "latitude" : 47.6061, "longitude" : 122.3328 }
CUPERTINO_COORDINATES ={ "latitude" : 37.3230, "longitude" : 122.0322 }

#Calculating the movement from seattle to cupertino, so Cupertino - Seattle
LATITUDE_INCREMENT = (CUPERTINO_COORDINATES['latitude'] - SEATTLE_COORDINATES['latitude'])
LONGITUDE_INCREMENT = (CUPERTINO_COORDINATES['longitude'] - SEATTLE_COORDINATES['longitude'])

#Environment Variables for configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_data')

random.seed(42)
start_time = datetime.now()
start_location = SEATTLE_COORDINATES.copy()

def get_next_time():
    global start_time
    
    start_time += timedelta(seconds=random.randint(30,60)) # Update Frequency
    return start_time


def generate_gps_data(device_id, timestamp, vehicle_type='private'):
    return{
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'speed': random.uniform(0, 40), #Km/h
        'direction': 'South-East',
        'vehicle_type': vehicle_type
        
    }

def generate_traffic_camera_data(device_id, timestamp, location, camera_id):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'camera_id': camera_id,
        'location': location,
        'timestamp': timestamp,
        'snapshot': 'Base64EncodedString' # Convert actual image or img url in S3 bucket by using base 64 encoding. Here I don't have a realtime IoT device.
        
        
    }
    

def generate_weather_data(device_id, timestamp, location):
    return{
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'location': location,
        'timestamp': timestamp,
        'temperature': random.uniform(-5, 25),
        'weatherCondition': random.choice(['Sunny', 'Cloudy', 'Rainy', "Snow"]),
        'precipitation': random.uniform(0, 25), #deg celcious
        'windSpeed': random.uniform(0, 100),
        'humidity': random.randint(0,100), # percentage
        'airQualityIndex': random.uniform(0, 50) #AQI value
        
    }
    

def generate_emergency_incident_data(device_id, timestamp, location):
    return{
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'location': location,
        'timestamp': timestamp,
        'incidentId': uuid.uuid4(),
        'type': random.choice(['Accident', 'Fire', 'Medical', 'Police', 'None']),
        'status': random.choice(['Active', 'Resolved']), #Issue resolved or active
        'description': 'Description of the incident'
    }

def simulate_vehicle_movement():
    global start_location
    
    #Move towards Cupertino
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT
    
    #Add randomness to simulate actual road travel by tweaking the long and lat a little bit
    start_location['latitude'] += random.uniform(-0.0005, 0.0005)
    start_location['longitude'] += random.uniform(-0.0005, 0.0005)
    
    return start_location

def generate_vehicle_data(device_id):
    location = simulate_vehicle_movement()
    
    return{
        'id': uuid.uuid4(), #Universally Unique Identifier
        'deviceId': device_id,
        'timestamp': get_next_time().isoformat(),
        'location': (location['latitude'], location['longitude']),
        'speed': random.uniform(10,40),
        'direction': 'South-East',
        'make': 'Tesla',
        'model': 'P100D',
        'year': '2024',
        'fuelType': 'electric'        
    }

def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
        

def produce_data_to_kafka(producer, topic, data):
    producer.produce(
        topic, 
        key=str(data['id']),
        value=json.dumps(data, default=json_serializer).encode('utf-8'), # Serialize the data
        on_delivery=delivery_report
    )
    
    producer.flush()

def simulate_journey(producer, device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        gps_data = generate_gps_data(device_id, vehicle_data['timestamp']) # We could get all the info at a time
        traffic_camera_data = generate_traffic_camera_data(device_id, vehicle_data['timestamp'], vehicle_data['location'], 'GoProCam123')
        weather_data = generate_weather_data(device_id, vehicle_data['timestamp'], vehicle_data['location'])
        emergency_incident_data = generate_emergency_incident_data(device_id, vehicle_data['timestamp'], vehicle_data['location'])
        
        if (vehicle_data['location'][0] >= CUPERTINO_COORDINATES['latitude']
            and vehicle_data['location'][1] <= CUPERTINO_COORDINATES['longitude']):
            #Means the vehicle reached Cupertino
            print("Vehicle Reached Cupertino! Simulation Ending....")
            break
        
        produce_data_to_kafka(producer, VEHICLE_TOPIC, vehicle_data)
        produce_data_to_kafka(producer, GPS_TOPIC, gps_data)
        produce_data_to_kafka(producer, TRAFFIC_TOPIC, traffic_camera_data)
        produce_data_to_kafka(producer, WEATHER_TOPIC, weather_data)
        produce_data_to_kafka(producer, EMERGENCY_TOPIC, emergency_incident_data)
        
        time.sleep(5)



if __name__ == "__main__":
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'Kafka error: {err}')
    }

    producer = SerializingProducer(producer_config)
    
    try:
        simulate_journey(producer, 'Vehicle-TVR-007')
        
    except KeyboardInterrupt:
        print('SImulation ended by the user')
    
    except Exception as e:
        print(f'Unexpected Error occurred: {e}')
        
        
        
        

