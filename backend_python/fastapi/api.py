from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from db.client import QuestDBClient
from datetime import datetime
from typing import Dict

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB client
db = QuestDBClient()

@app.get("/latest/{table_name}")
async def get_latest_data(table_name: str) -> Dict:
    """Get latest row from specified table"""
    try:
        # Query latest record using timestamp column
        result = db.query(f"""
            SELECT * FROM {table_name} 
            WHERE timestamp = (
                SELECT MAX(timestamp) 
                FROM {table_name}
            )
            LIMIT 1
        """)
        
        if result.empty:
            raise HTTPException(status_code=404, detail=f"No data found in table {table_name}")
            
        # Convert DataFrame row to dict and handle datetime serialization
        latest_row = result.iloc[0].to_dict()
        for k,v in latest_row.items():
            if isinstance(v, datetime):
                latest_row[k] = v.isoformat()
                
        return latest_row
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

