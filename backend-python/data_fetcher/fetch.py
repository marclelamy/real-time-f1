from enum import Enum
import requests
from typing import Dict, List
from datetime import datetime, timedelta, timezone
import time

class EndpointType(Enum):
    CAR_DATA = ("car_data", {
        "params": ["driver_number", "session_key", "speed", "rpm", "drs", "n_gear", "throttle", "brake"],
        "date_field": "date",
        "cadence": 1
    })
    DRIVERS = ("drivers", {
        "params": ["driver_number", "session_key", "meeting_key", "team_name", "country_code"],
        "date_field": None,  # Drivers endpoint doesn't use date filtering
        "cadence": None  # No regular refresh needed
    })
    INTERVALS = ("intervals", {
        "params": ["session_key", "driver_number", "interval", "gap_to_leader"],
        "date_field": "date",
        "cadence": 4
    })
    LAPS = ("laps", {
        "params": ["session_key", "driver_number", "lap_number", "is_pit_out_lap"],
        "date_field": "date_start",
        "cadence": 5
    })
    LOCATION = ("location", {
        "params": ["session_key", "driver_number", "x", "y", "z"],
        "date_field": "date",
        "cadence": 1
    })
    MEETINGS = ("meetings", {
        "params": ["year", "country_name", "meeting_key", "circuit_key"],
        "date_field": "date_start",
        "cadence": None  # No regular refresh needed
    })
    PIT = ("pit", {
        "params": ["session_key", "driver_number", "lap_number", "pit_duration"],
        "date_field": "date",
        "cadence": 5
    })
    POSITION = ("position", {
        "params": ["meeting_key", "driver_number", "position"],
        "date_field": "date",
        "cadence": 2
    })
    RACE_CONTROL = ("race_control", {
        "params": ["flag", "driver_number", "category", "scope", "sector"],
        "date_field": "date",
        "cadence": 5
    })
    SESSIONS = ("sessions", {
        "params": ["country_name", "session_name", "year", "session_key"],
        "date_field": "date_start",  # Sessions use date_start/date_end
        "cadence": None  # No regular refresh needed
    })
    STINTS = ("stints", {
        "params": ["session_key", "driver_number", "compound", "tyre_age_at_start"],
        "date_field": None,  # Stints don't use date filtering
        "cadence": 5
    })
    TEAM_RADIO = ("team_radio", {
        "params": ["session_key", "driver_number"],
        "date_field": "date",
        "cadence": 5
    })
    WEATHER = ("weather", {
        "params": ["meeting_key", "wind_direction", "track_temperature", "air_temperature"],
        "date_field": "date",
        "cadence": 60
    })

    def __init__(self, endpoint: str, config: Dict):
        self.endpoint = endpoint
        self.config = config

class F1DataFetcher:
    def __init__(self, db, start_time: datetime, is_real_time: bool):
        self.base_url = "https://api.openf1.org/v1"
        self.session = requests.Session()
        self.db = db
        self.current_time = start_time
        self.is_real_time = is_real_time

    def enough_time_has_passed_since_last_request(self, endpoint: EndpointType) -> bool:
        # print(f'assessing if enough time has passed since last request for {endpoint.endpoint}')
        # Get last request time from DB
        last_requests = self.db.query(
            f"SELECT MAX(timestamp) as last_time FROM request_logs WHERE endpoint = '{endpoint.endpoint}'"
        )
        # print(f'\n\n\nLast requests: {last_requests}')
        if last_requests.empty or last_requests['last_time'].iloc[0] is None:
            return True
            
        last_time = last_requests['last_time'].iloc[0]
        # print(f'Last time: {last_time}')
        cadence = endpoint.config.get("cadence")
        # print(f'Cadence: {cadence}')
        
        if cadence is None:  # Endpoints without cadence are requested once per session
            return False
        
        # print(f'Last time: {last_time}')
        # print(f'Current time: {datetime.now(timezone.utc)}')
        time_since_last = (datetime.now(timezone.utc).replace(tzinfo=None) - last_time).total_seconds()
        # if time_since_last >= cadence:
        #     print(f'Current time: {datetime.now(timezone.utc)}')
        #     print(f'Last time: {last_time}')
        #     print(f'Time since last: {time_since_last}')
        #     print(f'Time since last: {time_since_last} >= {cadence}')
        # print(f'{time_since_last >= cadence}\tCurrent time: {datetime.now(timezone.utc)}\tlast time: {last_time}\ttime since last: {time_since_last}\tcadence: {cadence}')
        return time_since_last >= cadence

    def log_request(self, endpoint: EndpointType, num_records: int):
        self.db.insert_dataframe(
            [{
                "endpoint": endpoint.endpoint,
                "num_records": num_records,
                "timestamp": datetime.now(timezone.utc)
            }],
            "request_logs"
        )
        
    def advance_time(self, seconds: float):
        self.current_time += timedelta(seconds=seconds)

    def fetch(self, endpoint: EndpointType, params: Dict = None, date_start: str = None, date_end: str = None) -> List[Dict]:
        try:
            if params is None:
                params = {}
            
            # Validate params against endpoint's allowed params
            endpoint_config = endpoint.config
            allowed_params = endpoint_config["params"]
            invalid_params = [p for p in params if p not in allowed_params]
            if invalid_params:
                raise ValueError(f"Invalid parameters for endpoint {endpoint.endpoint}: {invalid_params}. Allowed parameters are: {allowed_params}")
            
            # Add date parameters according to endpoint's date field configuration
            date_field = endpoint_config["date_field"]
            if date_field and endpoint_config["cadence"] is not None:
                # Get the last date from the DB if we're fetching real-time data to use as starting point
                if self.is_real_time:
                    # Get the latest date from the endpoint's table
                    date_col = "date" if date_field == "date" else "date_start"
                    last_date_query = f"SELECT MAX({date_col}) as last_date FROM {endpoint.endpoint}"
                    last_date_df = self.db.query(last_date_query)
                    
                    if not last_date_df.empty and last_date_df['last_date'].iloc[0] is not None:
                        last_date = last_date_df['last_date'].iloc[0]
                        # Add 1 second to last date
                        start_date = (last_date + timedelta(seconds=1)).isoformat()
                        
                        if date_field == "date":
                            params['date>='] = start_date
                        elif date_field == "date_start":
                            params['date_start>='] = start_date
                else:
                    if date_field == "date":
                        if date_start:
                            params['date>='] = date_start
                        if date_end:
                            params['date<='] = date_end
                    elif date_field == "date_start":
                        if date_start:
                            params['date_start>='] = date_start
                        if date_end:
                            params['date_end<='] = date_end
            
            print(f'Fetching data for {self.base_url}/{endpoint.endpoint} with params: {params}')
            response = self.session.get(
                f"{self.base_url}/{endpoint.endpoint}",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            time_info = f" between {date_start[11:19]} and {date_end[11:19]}" if date_start and date_end else ""
            return response.json()
        except requests.HTTPError as e:
            if e.response.status_code == 429:
                raise Exception("Too many requests. Please wait before trying again.")
            raise
        except requests.RequestException as e:
            raise
