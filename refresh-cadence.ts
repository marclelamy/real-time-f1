const cadence = {
    "car_data": {
        "refresh_rate": "0.5 seconds",
        "seconds_between_updates": 0.5,
        "confirmed": true,
        "endpoint": "/v1/car_data"
    },
    "drivers": {
        "refresh_rate": "once per session",
        "seconds_between_updates": null,
        "confirmed": false,
        "notes": "Driver info rarely changes during session, but good to check for replacements",
        "endpoint": "/v1/drivers"
    },
    "intervals": {
        "refresh_rate": "4 seconds",
        "seconds_between_updates": 4,
        "confirmed": true,
        "notes": "Race only",
        "endpoint": "/v1/intervals"
    },
    "laps": {
        "refresh_rate": "5 seconds",
        "seconds_between_updates": 5,
        "confirmed": false,
        "notes": "New lap data available as sectors complete",
        "endpoint": "/v1/laps"
    },
    "location": {
        "refresh_rate": "1 second",
        "seconds_between_updates": 1,
        "confirmed": true,
        "endpoint": "/v1/location"
    },
    "meetings": {
        "refresh_rate": "once per session",
        "seconds_between_updates": null,
        "confirmed": false,
        "notes": "Static data, rarely changes",
        "endpoint": "/v1/meetings"
    },
    "pit": {
        "refresh_rate": "5 seconds",
        "seconds_between_updates": 5,
        "confirmed": false,
        "notes": "Critical timing during pit stops",
        "endpoint": "/v1/pit"
    },
    "position": {
        "refresh_rate": "2 seconds",
        "seconds_between_updates": 2,
        "confirmed": false,
        "notes": "Position changes can be frequent",
        "endpoint": "/v1/position"
    },
    "race_control": {
        "refresh_rate": "5 seconds",
        "seconds_between_updates": 5,
        "confirmed": false,
        "notes": "Safety critical messages need quick updates",
        "endpoint": "/v1/race_control"
    },
    "sessions": {
        "refresh_rate": "once per session",
        "seconds_between_updates": null,
        "confirmed": false,
        "notes": "Session data mostly static",
        "endpoint": "/v1/sessions"
    },
    "stints": {
        "refresh_rate": "5 seconds",
        "seconds_between_updates": 5,
        "confirmed": false,
        "notes": "Updates with pit stops and tire changes",
        "endpoint": "/v1/stints"
    },
    "team_radio": {
        "refresh_rate": "5 seconds",
        "seconds_between_updates": 5,
        "confirmed": false,
        "notes": "Real-time communications need quick updates",
        "endpoint": "/v1/team_radio"
    },
    "weather": {
        "refresh_rate": "60 seconds",
        "seconds_between_updates": 60,
        "confirmed": true,
        "endpoint": "/v1/weather"
    }
}