import os
import logging
import json
from datetime import datetime
from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.identity import DefaultAzureCredential

# Environment variables
TABLE_NAME = os.getenv("TABLE_NAME", "state")
PARTITION_KEY = os.getenv("PARTITION_KEY", "cloudtrail")
ROW_KEY = os.getenv("ROW_KEY", "collector")
STATE_FIELD = os.getenv("STATE_FIELD", "lastState")
STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME")

# Table client
def _get_table_service_client():
    if not STORAGE_ACCOUNT_NAME:
        raise ValueError("STORAGE_ACCOUNT_NAME environment variable is not set.")

    endpoint = f"https://{STORAGE_ACCOUNT_NAME}.table.core.windows.net"
    credential = DefaultAzureCredential()

    logging.info("Authenticating to Azure Table Storage using Managed Identity.")
    return TableServiceClient(endpoint=endpoint, credential=credential)


def _get_table_client():
    service_client = _get_table_service_client()

    try:
        service_client.create_table_if_not_exists(TABLE_NAME)
        logging.info(f"Ensured table '{TABLE_NAME}' exists.")
    except Exception as e:
        logging.error(f"Error ensuring table exists: {e}")
        raise

    return service_client.get_table_client(table_name=TABLE_NAME)

# Entity setup
def _ensure_entity_exists(table_client):
    entity = {
        "PartitionKey": PARTITION_KEY,
        "RowKey": ROW_KEY,
        STATE_FIELD: None
    }

    try:
        table_client.create_entity(entity=entity)
        logging.info("State entity initialized.")
    except ResourceExistsError:
        logging.debug("State entity already exists.")


def initialize_table():
    table_client = _get_table_client()
    _ensure_entity_exists(table_client)
    logging.info("Table and state entity initialized successfully.")


# State format
# Stored JSON shape:
# {
#   "next_token": str | None,
#   "start_time": ISO string | None
# }

# Function to create entity and merge with new state
def update_last_state(state):
    table_client = _get_table_client()

    next_token, start_time = state if state else (None, None)

    if isinstance(start_time, datetime):
        start_time = start_time.isoformat()
    elif start_time is not None:
        start_time = str(start_time)

    payload = {
        "next_token": next_token,
        "start_time": start_time
    }

    entity = {
        "PartitionKey": PARTITION_KEY,
        "RowKey": ROW_KEY,
        STATE_FIELD: json.dumps(payload)
    }

    try:
        table_client.upsert_entity(entity=entity)
        logging.info("lastState updated successfully.")
    except Exception as e:
        logging.error(f"Error updating lastState: {e}")
        raise

# Function to retrieve entity and read last state
def read_last_state():
    table_client = _get_table_client()

    try:
        entity = table_client.get_entity(
            partition_key=PARTITION_KEY,
            row_key=ROW_KEY
        )

        raw_value = entity.get(STATE_FIELD)

        if not raw_value:
            return None

        payload = json.loads(raw_value)

        next_token = payload.get("next_token")
        start_time = payload.get("start_time")

        if start_time:
            start_time = datetime.fromisoformat(start_time)

        return [next_token, start_time]

    except ResourceNotFoundError:
        logging.warning("State entity not found. Creating default entity.")
        _ensure_entity_exists(table_client)
        return None

    except Exception as e:
        logging.error(f"Error reading lastState: {e}")
        raise
