from urllib.request import urlopen
import json
from rich import print

from src.schemas import *

# Map OpenF1 endpoints to schema models
ENDPOINT_SCHEMA_MAP = {
  '/car_data': CarData,
  '/drivers': Driver, 
  '/intervals': Interval,
  '/laps': Lap,
  '/locations': Location,
  '/meetings': Meeting,
  '/pits': Pit,
  '/positions': Position,
  '/racecontrol': RaceControl,
  '/sessions': Session,
  '/stints': Stint,
  '/team_radio': TeamRadio,
  '/weather': Weather
}

def fetch(endpoint: str, **params) -> list:
  """
  Fetches data from OpenF1 API for a given endpoint and parameters
  Args:
    endpoint: API endpoint path (e.g. '/sessions')
    params: Query parameters as keyword arguments
  Returns:
    List of records matching the schema for that endpoint
  """
  base = 'https://api.openf1.org/v1'
  query = '&'.join(f'{k}={v}' for k,v in params.items())
  url = f'{base}{endpoint}?{query}'
  
  response = urlopen(url)
  data = json.loads(response.read())
  
  # Convert raw data to schema objects if endpoint has mapping
  if endpoint in ENDPOINT_SCHEMA_MAP:
    return [ENDPOINT_SCHEMA_MAP[endpoint](**record) for record in data]
  return data

