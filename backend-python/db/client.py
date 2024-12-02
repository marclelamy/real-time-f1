from questdb.ingress import Sender, TimestampNanos
import pandas as pd
from sqlalchemy import create_engine
import datetime

class QuestDBClient:
    def __init__(self, host='localhost', port=9000, username='admin', password='quest'):
        # ILP connection string for writes
        self.write_conf = f"http::addr={host}:{port};username={username};password={password};"
        # PostgreSQL connection for reads
        self.read_url = f"postgresql://{username}:{password}@{host}:8812/qdb"
        self.engine = create_engine(self.read_url)

    def insert_dataframe(self, data: list, table_name: str, timestamp_column=None):
        """Insert a list of JSON records into QuestDB by converting them to individual rows"""
        try:
            # First ensure table exists
            with self.engine.connect() as conn:
                # Create table if it doesn't exist, with WAL enabled
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    timestamp TIMESTAMP,
                    PRIMARY KEY(timestamp)
                );
                """
                conn.execute(create_table_query)

            with Sender.from_conf(self.write_conf) as sender:
                # Insert each record from the JSON array
                for record in data:
                    # Split fields into symbols (strings) and numeric columns
                    symbols = {}
                    columns = {}
                    
                    for k, v in record.items():
                        if isinstance(v, str):
                            # Try to parse string as datetime if it looks like ISO format
                            try:
                                if 'T' in v and ('+' in v or 'Z' in v or '-' in v):
                                    columns[k] = datetime.datetime.fromisoformat(v.replace('Z', '+00:00'))
                                else:
                                    symbols[k] = v
                            except ValueError:
                                symbols[k] = v
                        elif isinstance(v, (int, float)):
                            columns[k] = v
                        elif isinstance(v, (datetime.datetime, datetime.date)):
                            columns[k] = v
                    
                    sender.row(
                        table_name,
                        symbols=symbols,
                        columns=columns,
                        at=timestamp_column or TimestampNanos.now()
                    )
                sender.flush()
            return True
        except Exception as e:
            print(f"Data insert error: {e}")
            return False

    def query(self, query: str) -> pd.DataFrame:
        """Query data from QuestDB"""
        try:
            with self.engine.connect() as conn:
                # First ensure table exists with WAL enabled
                # create_table_query = f"""
                # CREATE TABLE IF NOT EXISTS {query.split(' ')[3].split('(')[0]} (
                #     timestamp TIMESTAMP,
                #     PRIMARY KEY(timestamp)
                # );
                # """
                # conn.execute(create_table_query)
                return pd.read_sql(query, conn)
        except Exception as e:
            print(f"Query error: {e}")
            return pd.DataFrame()