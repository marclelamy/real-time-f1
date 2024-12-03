from datetime import datetime, timedelta, timezone
import json
import time
from db.client import QuestDBClient
from data_fetcher.fetch import F1DataFetcher, EndpointType

# Base start time for fetching data
START_TIME = datetime.strptime("2024-12-01 16:10:00 UTC", "%Y-%m-%d %H:%M:%S %Z")
IS_REAL_TIME = False
DELETE_DATA_ON_START = True
NUMBER_OF_SECONDS_TO_FETCH = 10


def main():
    db = QuestDBClient()
    fetcher = F1DataFetcher(db, START_TIME, IS_REAL_TIME)
    if DELETE_DATA_ON_START:
        if input("Are you sure you want to delete all data? (y/n): ") == "y":
            db.delete_data(recreate_schema=True)
    
    # Get latest session info
    latest_session = fetcher.fetch(EndpointType.SESSIONS, {
        "session_key": "latest",
    })

    if latest_session:
        session = latest_session[0]
        session_key = session["session_key"]
        
        while True:
            try:
                # Check and make requests for each endpoint based on cadence
                loop_enpoint_type_start_time = time.time()
                for endpoint_type in [EndpointType.CAR_DATA]:#EndpointType:
                    start_time = time.time()
                    # print(f'Checking if enough time has passed since last request for {endpoint_type.endpoint}')
                    is_allowed_to_request = fetcher.enough_time_has_passed_since_last_request(endpoint_type)
                    while not is_allowed_to_request:
                        time.sleep(0.05)
                        is_allowed_to_request = fetcher.enough_time_has_passed_since_last_request(endpoint_type)

                    # if is_allowed_to_request:
                    window_end = fetcher.current_time + timedelta(seconds=NUMBER_OF_SECONDS_TO_FETCH)
                    # print(f'Fetching data for {endpoint_type.endpoint} from {fetcher.current_time} to {window_end}')
                    
                    # Only add session_key param for endpoints that accept it
                    params = {}
                    if "session_key" in endpoint_type.config["params"]:
                        params["session_key"] = session_key
                    
                    # print(f'Fetching data for {endpoint_type} with params: {params}')
                    data = fetcher.fetch(
                        endpoint_type,
                        params,
                        fetcher.current_time.isoformat(),
                        window_end.isoformat()
                    )
                    # print(f'Fetched data: {len(data)}')
                    if data:
                        db.insert_dataframe(data, endpoint_type.endpoint)
                        fetcher.log_request(endpoint_type, len(data))
                    # print(f'Logged request for {endpoint_type.endpoint}')

                    # print(f'Fetching data for {endpoint_type.endpoint} with params: {params} length: {len(data)} time: {time.time() - start_time}')
                
                # Advance simulation time by smallest cadence (0.5 seconds)
                fetcher.advance_time(NUMBER_OF_SECONDS_TO_FETCH)
                # print(f'Advanced time to {fetcher.current_time}')
                
            except Exception as e:
                print(f"Error fetching data: {e}")
                break

if __name__ == "__main__":
    main()