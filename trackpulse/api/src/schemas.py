from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Timing Related Schemas
class Interval(BaseModel):
  timestamp: datetime
  date: datetime
  driver_number: int
  gap_to_leader: float
  interval: float
  meeting_key: int
  session_key: int

class Lap(BaseModel):
  timestamp: datetime
  date_start: datetime
  driver_number: int
  duration_sector_1: Optional[float]
  duration_sector_2: Optional[float]
  duration_sector_3: Optional[float]
  i1_speed: Optional[int]
  i2_speed: Optional[int]
  is_pit_out_lap: bool
  lap_duration: Optional[float]
  lap_number: int
  meeting_key: int
  session_key: int
  st_speed: Optional[int]

class Position(BaseModel):
  timestamp: datetime
  date: datetime
  driver_number: int
  meeting_key: int
  position: int
  session_key: int

# Telemetry Related Schemas
class CarData(BaseModel):
  timestamp: datetime
  date: datetime
  driver_number: int
  brake: int
  drs: int
  meeting_key: int
  n_gear: int
  rpm: int
  session_key: int
  speed: int
  throttle: int

class Location(BaseModel):
  timestamp: datetime
  date: datetime
  driver_number: int
  meeting_key: int
  session_key: int
  x: int
  y: int
  z: int

# Session Related Schemas
class Meeting(BaseModel):
  timestamp: datetime
  circuit_key: int
  circuit_short_name: str
  country_code: str
  country_key: int
  country_name: str
  date_start: datetime
  gmt_offset: str
  location: str
  meeting_key: int
  meeting_name: str
  meeting_official_name: str
  year: int

class Session(BaseModel):
  timestamp: datetime
  circuit_key: int
  circuit_short_name: str
  country_code: str
  country_key: int
  country_name: str
  date_end: datetime
  date_start: datetime
  gmt_offset: str
  location: str
  meeting_key: int
  session_key: int
  session_name: str
  session_type: str
  year: int

# Driver Related Schemas
class Driver(BaseModel):
  timestamp: datetime
  date: datetime
  broadcast_name: str
  country_code: str
  driver_number: int
  first_name: str
  full_name: str
  headshot_url: str
  last_name: str
  meeting_key: int
  name_acronym: str
  session_key: int
  team_colour: str
  team_name: str

class TeamRadio(BaseModel):
  timestamp: datetime
  date: datetime
  driver_number: int
  meeting_key: int
  recording_url: str
  session_key: int

class Stint(BaseModel):
  timestamp: datetime
  compound: str
  driver_number: int
  lap_end: int
  lap_start: int
  meeting_key: int
  session_key: int
  stint_number: int
  tyre_age_at_start: int

class Pit(BaseModel):
  timestamp: datetime
  date: datetime
  driver_number: int
  lap_number: int
  meeting_key: int
  pit_duration: float
  session_key: int

# Weather Schema
class Weather(BaseModel):
  timestamp: datetime
  air_temperature: float
  date: datetime
  humidity: int
  meeting_key: int
  pressure: float
  rainfall: int
  session_key: int
  track_temperature: float
  wind_direction: int
  wind_speed: float

# Race Control Related Schemas
class RaceControl(BaseModel):
  timestamp: datetime
  category: str
  date: datetime
  driver_number: Optional[int]
  flag: str
  lap_number: Optional[int]
  meeting_key: int
  message: str
  scope: str
  sector: Optional[int]
  session_key: int

class RequestLog(BaseModel):
  timestamp: datetime
  endpoint: str
  num_records: int 