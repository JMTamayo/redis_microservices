# Import from Python:
import asyncio, time, warnings, requests

# Import from datetime:
from datetime import datetime

# Import from random:
from random import random

# Import from others:
from producer import save_result

warnings.filterwarnings("ignore", category=DeprecationWarning)

async def getData(timelapse):

    # Setting server url: LOCALHOST
    server_url = "http://127.0.0.1:8000"

    # Setting min. and max. values for press amperage:
    min_presser_amp = 10
    max_presser_amp = 100

    # Setting device amperage sensor id:
    id = "PRESS1AMP"

    # Printing general simulation information:
    print("")
    print("PRESSER AMPERAGE SIMULATION")
    print("Device Id: " + id)
    print("Timelapse: " + str(timelapse) + " Seconds")
    print("Start date and time: " + str(datetime.now()))
    print("")

    
    try:
        # Deleting previous information in Redis stream:
        path = "/simulator/deletedata/all"
        rq = requests.delete(server_url + path)

        if(rq.status_code == 200):
            # Calling to API to delete previous information in Redis stream:
            print("Database restarted successfully. Runing Simulation")
            print("")

            while True: # Continuing with the simulation after deleting previous information in Redis stream:
                
                # Setting timeout for async. fuction:
                await asyncio.sleep(timelapse)

                # Setting the device amperage value:
                amp = min_presser_amp + random()*(max_presser_amp - min_presser_amp)

                # Setting the timestamp value:
                timestamp = time.time()

                # Storing simulation results as a dictionary:
                result = {
                    "id": id,
                    "amp": amp,
                    "timestamp": timestamp
                }

                # Calling to API to store data in Redis stream:
                path = "/simulator/savedata"
                save_result(result, server_url + path)


        else:
            # Request was not successful: Printing the results:
            print("Server Connection Status Code: " + rq.status_code)
            print("")
            print("SIMULATION FINISHED. PLEASE TYPE CTRL+C TO STOP THE EXECUTION.")        


    except Exception as e:
        # Connection was not successful: Printing the results:
        print(e)
        print("Server Connection Status Code: " + rq.status_code)
        print("")
        print("SIMULATION FINISHED. PLEASE TYPE CTRL+C TO STOP THE EXECUTION.")
        
    
def simulator():

    # Setting the time lapse for the simulation:
    timelapse = 3

    # Creating loop event:
    loop = asyncio.get_event_loop()

    try:
        asyncio.ensure_future(getData(timelapse))
        loop.run_forever()

    except KeyboardInterrupt:
        pass
    
    finally:
        loop.close()


if __name__ == "__main__":

    # Running Simulator and Producer:
    simulator()
