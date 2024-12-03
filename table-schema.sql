-- request_logs
CREATE TABLE request_logs (
    timestamp TIMESTAMP,
    endpoint STRING,
    num_records INT
) timestamp(timestamp) partition by DAY;


-- Car data table
CREATE TABLE car_data (
    timestamp TIMESTAMP,
    date TIMESTAMP,
    driver_number INT,
    brake INT,
    drs INT,
    meeting_key INT,
    n_gear INT,
    rpm INT,
    session_key INT,
    speed INT,
    throttle INT
) timestamp(timestamp) partition by DAY;

-- Drivers table
CREATE TABLE drivers (
    timestamp TIMESTAMP,
    date TIMESTAMP,
    broadcast_name STRING,
    country_code STRING,
    driver_number INT,
    first_name STRING,
    full_name STRING,
    headshot_url STRING,
    last_name STRING,
    meeting_key INT,
    name_acronym STRING,
    session_key INT,
    team_colour STRING,
    team_name STRING
) timestamp(timestamp) partition by DAY;

-- Intervals table
CREATE TABLE intervals (
    timestamp TIMESTAMP,
    date TIMESTAMP,
    driver_number INT,
    gap_to_leader DOUBLE,
    interval DOUBLE,
    meeting_key INT,
    session_key INT
) timestamp(timestamp) partition by DAY;

-- Laps table
CREATE TABLE laps (
    timestamp TIMESTAMP,
    date_start TIMESTAMP,
    driver_number INT,
    duration_sector_1 DOUBLE,
    duration_sector_2 DOUBLE,
    duration_sector_3 DOUBLE,
    i1_speed INT,
    i2_speed INT,
    is_pit_out_lap BOOLEAN,
    lap_duration DOUBLE,
    lap_number INT,
    meeting_key INT,
    session_key INT,
    st_speed INT
) timestamp(timestamp) partition by DAY;

-- Location table
CREATE TABLE location (
    timestamp TIMESTAMP,
    date TIMESTAMP,
    driver_number INT,
    meeting_key INT,
    session_key INT,
    x INT,
    y INT,
    z INT
) timestamp(timestamp) partition by DAY;

-- Meetings table
CREATE TABLE meetings (
    timestamp TIMESTAMP,
    circuit_key INT,
    circuit_short_name STRING,
    country_code STRING,
    country_key INT,
    country_name STRING,
    date_start TIMESTAMP,
    gmt_offset STRING,
    location STRING,
    meeting_key INT,
    meeting_name STRING,
    meeting_official_name STRING,
    year INT
) timestamp(timestamp) partition by DAY;

-- Pit table
CREATE TABLE pit (
    timestamp TIMESTAMP,
    date TIMESTAMP,
    driver_number INT,
    lap_number INT,
    meeting_key INT,
    pit_duration DOUBLE,
    session_key INT
) timestamp(timestamp) partition by DAY;

-- Position table
CREATE TABLE position (
    timestamp TIMESTAMP,
    date TIMESTAMP,
    driver_number INT,
    meeting_key INT,
    position INT,
    session_key INT
) timestamp(timestamp) partition by DAY;

-- Race control table
CREATE TABLE race_control (
    timestamp TIMESTAMP,
    category STRING,
    date TIMESTAMP,
    driver_number INT,
    flag STRING,
    lap_number INT,
    meeting_key INT,
    message STRING,
    scope STRING,
    sector INT,
    session_key INT
) timestamp(timestamp) partition by DAY;

-- Sessions table
CREATE TABLE sessions (
    timestamp TIMESTAMP,
    circuit_key INT,
    circuit_short_name STRING,
    country_code STRING,
    country_key INT,
    country_name STRING,
    date_end TIMESTAMP,
    date_start TIMESTAMP,
    gmt_offset STRING,
    location STRING,
    meeting_key INT,
    session_key INT,
    session_name STRING,
    session_type STRING,
    year INT
) timestamp(timestamp) partition by DAY;

-- Stints table
CREATE TABLE stints (
    timestamp TIMESTAMP,
    compound STRING,
    driver_number INT,
    lap_end INT,
    lap_start INT,
    meeting_key INT,
    session_key INT,
    stint_number INT,
    tyre_age_at_start INT
) timestamp(timestamp) partition by DAY;

-- Team radio table
CREATE TABLE team_radio (
    timestamp TIMESTAMP,
    date TIMESTAMP,
    driver_number INT,
    meeting_key INT,
    recording_url STRING,
    session_key INT
) timestamp(timestamp) partition by DAY;

-- Weather table
CREATE TABLE weather (
    timestamp TIMESTAMP,
    air_temperature DOUBLE,
    date TIMESTAMP,
    humidity INT,
    meeting_key INT,
    pressure DOUBLE,
    rainfall INT,
    session_key INT,
    track_temperature DOUBLE,
    wind_direction INT,
    wind_speed DOUBLE
) timestamp(timestamp) partition by DAY;
