import boto3
import logging
import os
import time
from datetime import datetime, timedelta, timezone

# Function to initiate collection of AWS CloudTrail logs
def collect_aws_cloudtrail(state):
    aws_access_key = os.getenv("AWS_ACCESS_KEY")
    aws_secret_key = os.getenv("AWS_SECRET_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    max_results = int(os.getenv("MAX_RESULTS", 50))
    look_back_range = int(os.getenv("LOOK_BACK_RANGE_DAYS", 30))

    if not all([aws_access_key, aws_secret_key]):
        raise ValueError("Missing AWS credentials")

    logging.info(f"Connecting to AWS CloudTrail in region {aws_region}")

    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )

    cloudtrail = session.client("cloudtrail")

    # Normalize state
    if not state:
        start_time = datetime.now(timezone.utc) - timedelta(days=look_back_range)
        next_token = None
        logging.info(f"No state provided. Starting from {start_time}")
    else:
        next_token = state[0]

        start_time = state[1]
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)

    all_events = []

    # Fetch loop
    while True:
        params = {
            "StartTime": start_time,
            "MaxResults": max_results
        }

        if next_token:
            params["NextToken"] = next_token
            time.sleep(5)

        try:
            response = cloudtrail.lookup_events(**params)
            events = response.get("Events", [])

            all_events.extend(events)
            logging.info(f"Fetched {len(events)}, total: {len(all_events)}")

            if len(all_events) >= 200:
                logging.info("Reached event limit, stopping fetch loop.")
                break

            next_token = response.get("NextToken")

        except cloudtrail.exceptions.ClientError as e:
            logging.error(f"AWS CloudTrail ClientError: {e}")
            break

        except Exception as e:
            logging.error(f"Unexpected error fetching CloudTrail logs: {e}")
            break

        if not next_token:
            break

    # Format new state
    new_state = [
        next_token,
        start_time.isoformat() if isinstance(start_time, datetime) else start_time
    ]

    if all_events:
        return all_events, new_state

    logging.info("No CloudTrail events found.")
    return None
