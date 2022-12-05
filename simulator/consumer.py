# Import from Python:
import asyncio, requests, json, warnings

# Import from datetime:
from datetime import datetime

warnings.filterwarnings("ignore", category=DeprecationWarning)

def delete_by_id(url):

    # Calling to API to delete data by id in Redis stream:
    try:
        rq = requests.delete(url)
        return rq.text

    except Exception as e:
        print(str(e))
        return e


async def check_amperage(server_url, timelapse):

    # Storing the initial timelapse in another variable to use in the future to wait few more seconds when consumer doesn't find data in Redis stream:
    initial_timelapse = timelapse

    # Printing general consumer information:
    print("")
    print("PRESSER AMPERAGE SIMULATION - <CONSUMER>")
    print("Timelapse: " + str(timelapse) + " Seconds")
    print("Start date and time: " + str(datetime.now()))
    print("")

    while True:
        try:
            # Setting timeout for async. fuction:
            await asyncio.sleep(timelapse)
        
            # Calling to API to get the oldest data in Redis stream:
            path = "/simulator/showdata/first"
            rq = requests.get(server_url + path)
            first_data = json.loads(rq._content)

            if(isinstance(first_data, list)):

                # Getting the data id in Redis stream:
                first_data_id = first_data[0][0]

                # Getting the simulation values in Redis stream:
                first_data_values = first_data[0][1]
                amp = float(first_data_values["amp"])
                timestamp = float(first_data_values["timestamp"])
                date_time = datetime.fromtimestamp(timestamp)
                
                # Setting alarm for device amperage:
                if(amp > 50):
                    # High amperage alarm when amperage > 50 amp
                    msg = "¡WARNING! High amperage in the device (> 50 amp)"

                else:
                    # Normal operation when amperage < 50 amp
                    msg = "Device operating normally (<50 amp)"

                # Printing the results:
                print("Date & Time [YYYY-MM-DD hh:mm:ss]: " + str(date_time))
                print("Amperage [amp]: " + str(amp) )
                print("Message: " + msg)
                print("")

                # Deleting event from Redis stream after reading it:
                path = "/simulator/deletedata/"
                delete_by_id(server_url + path + first_data_id)

                # Resetting the timelapse if it has been changed by not finding data in the Redis stream:
                timelapse = initial_timelapse
            else:
                pass

        except Exception as e:
            # Consumer didn't find data in Redis stream: Increasing timelapse temporarily:
            timelapse = 3
            print(e)
            print("")
            print("SIMULATION FINISHED. PLEASE TYPE CTRL+C TO STOP THE EXECUTION.")
            print("")

def consumer():

    # Setting server url: LOCALHOST
    server_url = "http://127.0.0.1:8000" 

    # Setting the time lapse for the consumer:
    timelapse = 0.01

    # Creating loop event:
    loop = asyncio.get_event_loop()

    try:
        asyncio.ensure_future(check_amperage(server_url, timelapse))
        loop.run_forever()

    except KeyboardInterrupt:
        pass

    finally:
        loop.close()


if __name__ == "__main__":

    # Running Consumer:
    consumer()