import sys
import os
import logging
import json

from azure.eventhub import EventHubProducerClient
from azure.identity import DefaultAzureCredential

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from collector import collect_aws_cloudtrail
from state_manager import read_last_state, update_last_state
from sender_evh import send_to_event_hub

# Environment variables
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME", "cloudtrail-events")
EVENT_HUB_NAMESPACE = os.getenv("EVENT_HUB_NAMESPACE")

# Authenticate with system assigned managed identity
credential = DefaultAzureCredential()

# Function to create Event Hub Producer Client to send to Azure Event Hubs
def create_producer():
    return EventHubProducerClient(
        fully_qualified_namespace=EVENT_HUB_NAMESPACE,
        eventhub_name=EVENT_HUB_NAME,
        credential=credential
    )

# Main function (timer trigger)
def main(myTimer):
    producer = None

    try:
        # Create EPC
        producer = create_producer()

        if myTimer.past_due:
            logging.info("Timer is past due!")

        # Retrieve and load state
        try:
            state = read_last_state()
        except Exception as e:
            logging.error(f"State load error: {e}")
            state = None

        # Collect events
        events = []
        new_state = None

        try:
            result = collect_aws_cloudtrail(state)

            if result:
                events, new_state = result
                logging.info(f"Fetched {len(events)} events")

        except Exception as e:
            logging.error(f"Collector error: {e}")

        # Send pipeline
        sent_evh = False

        if events:
            sent_evh = send_to_event_hub(events, producer)

        # State update ONLY if success
        if sent_evh and new_state:
            update_last_state(new_state)
            logging.info("State updated successfully")

        logging.info("Function execution complete")

    finally:
        if producer:
            try:
                producer.close()
                logging.info("EventHub producer closed safely")
            except Exception as e:
                logging.error(f"Error closing producer: {e}")
