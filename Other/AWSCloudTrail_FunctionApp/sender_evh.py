import json
import logging
from azure.eventhub import EventData

# Build event data attached to each event
def build_event_data(event: dict):
    body = json.dumps(event, default=str)

    event_data = EventData(body)

    event_data.properties = {
        "source": "cloudtrail",
        "event_type": event.get("eventName", "unknown"),
        "region": event.get("awsRegion", "unknown"),
        "account_id": event.get("recipientAccountId", "unknown"),
        "ingestion_format": "json",
        "pipeline": "cloudtrail-to-adx"
    }

    return event_data

# Function to send the actual logs to the Event Hub using the EPC
def send_to_event_hub(events, producer):
    if not events:
        logging.info("No events to send.")
        return True

    try:
        batch = producer.create_batch()

        for event in events:
            event_data = build_event_data(event)

            try:
                batch.add(event_data)
            except ValueError:
                producer.send_batch(batch)
                batch = producer.create_batch()
                batch.add(event_data)

        if len(batch) > 0:
            producer.send_batch(batch)

        logging.info(f"Sent {len(events)} events to Event Hub.")
        return True

    except Exception as ex:
        logging.error(f"Failed to send events: {ex}")
        return False
