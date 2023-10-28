import asyncio
import time
import paho.mqtt.client as mqtt

# Constants for device names
PROP1 = "60:55:F9:7B:5F:2C"
PROP2 = "60:55:F9:7B:98:14" # FOG MACHINE
PROP3 = "60:55:F9:7B:63:88"
PROP4 = "60:55:F9:7B:82:30"
PROP5 = "60:55:F9:7B:60:BC"
PROP6 = "60:55:F9:7B:7F:98" # CAULDRON AIR PUMP

SENSOR_THRESHOLD = 1000

# Dictionary to store lists for each device
queues = {
    PROP1: [],
    PROP2: [],
    PROP3: [],
    PROP4: [],
    PROP5: [],
    PROP6: []
}

# Define MQTT parameters
mqtt_broker = "192.168.86.2"
client = mqtt.Client("server")
client.connect(mqtt_broker)

# Function to publish MQTT events
def publish_event(topic, message):
    client.publish(topic, message)
    print(f"Published event: {message} to topic {topic}")

# Function to handle MQTT messages
def on_message(client, userdata, message):
    device_id = message.topic.split("/")[1]  # Extract device ID from the topic
    if device_id in queues:
        queues[device_id].append(message)

# Set up MQTT subscription with updated topic names
for device_id in queues:
    client.subscribe(f"device/{device_id}/sensor")  # Updated topic for subscription
client.on_message = on_message


async def process_queue_PROP1():
    while True:
        await asyncio.sleep(0.3)
        if queues[PROP1]:
            payloads = [int(message.payload.decode()) for message in queues[PROP1]]  # Extract payloads as integers
            max_payload = max(payloads)  # Find the maximum payload value
            print(f"Max payload is: {max_payload}")

            # if max_payload > SENSOR_THRESHOLD:
            if max_payload % 2 == 0: # if max_payload is even
                publish_event(f"device/{PROP1}/actuator", "X2")  # Publish event when the maximum threshold is exceeded

        queues[PROP1] = []  # Clear the list
        await asyncio.sleep(4)  # Adjust the delay as needed
        
# FOG MACHINE AND CAULDRON AIR PUMP
async def process_queue_PROP2():
    while True:
        await asyncio.sleep(0.3)
        if queues[PROP2]:
            payloads = [int(message.payload.decode()) for message in queues[PROP2]]  # Extract payloads as integers
            max_payload = max(payloads)  # Find the maximum payload value
            print(f"Max payload is: {max_payload}")

            if max_payload > SENSOR_THRESHOLD:
                publish_event(f"device/{PROP2}/actuator", "X8")  # Publish event when the maximum threshold is exceeded
                await asyncio.sleep(3)  # Delay after running the fog machine
                publish_event(f"device/{PROP6}/actuator", "X1") # Run the air pump
                await asyncio.sleep(2)
                publish_event(f"device/{PROP6}/actuator", "X1") # Run the air pump
                await asyncio.sleep(2)
                publish_event(f"device/{PROP6}/actuator", "X6") # Run the air pump
                await asyncio.sleep(120)  # Delay at least 2 minutes before running the fog machine again
        queues[PROP2] = []  # Clear the list
        #TODO: keep a count of the number of times the fog machine has been run. Stop after 50.





async def process_queue_PROP3():
    while True:
        await asyncio.sleep(0.3)
        if queues[PROP3]:
            for message in queues[PROP3]:
                topic = message.topic
                payload = message.payload.decode()
                print(f"Processing {PROP3} - Received from queue message: {payload} from topic {topic}")
                # Custom processing for PROP3
                await asyncio.sleep(4)
            queues[PROP3] = []


async def process_queue_PROP4():
    while True:
        await asyncio.sleep(0.3)
        if queues[PROP4]:
            for message in queues[PROP4]:
                topic = message.topic
                payload = message.payload.decode()
                print(f"Processing {PROP4} - Received from queue message: {payload} from topic {topic}")
                # Custom processing for PROP4
                await asyncio.sleep(5)
            queues[PROP4] = []


async def process_queue_PROP5():
    while True:
        await asyncio.sleep(0.3)
        if queues[PROP5]:
            for message in queues[PROP5]:
                topic = message.topic
                payload = message.payload.decode()
                print(f"Processing {PROP5} - Received from queue message: {payload} from topic {topic}")
                # Custom processing for PROP5
                await asyncio.sleep(5)
            queues[PROP5] = []


async def process_queue_PROP6():
    while True:
        await asyncio.sleep(0.3)
        if queues[PROP6]:
            for message in queues[PROP6]:
                topic = message.topic
                payload = message.payload.decode()
                print(f"Processing {PROP6} - Received from queue message: {payload} from topic {topic}")
                # Custom processing for PROP6
                await asyncio.sleep(5)
            queues[PROP6] = []

# Define the event loop
async def event_loop():
    while True:
        # All this main loop does is print the current time every .5 seconds
        await asyncio.sleep(0.5)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + f".{int(time.time() * 1000) % 1000:03d}"
        print(current_time)


# Start the event loop
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(event_loop())
    loop.create_task(process_queue_PROP1())
    loop.create_task(process_queue_PROP2())
    loop.create_task(process_queue_PROP3())
    loop.create_task(process_queue_PROP4())
    loop.create_task(process_queue_PROP5())
    loop.create_task(process_queue_PROP6())
    client.loop_start()
    loop.run_forever()
