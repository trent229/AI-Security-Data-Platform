"""Simulate security devices sending events to the platform."""

import argparse
import json
import random
import time
from urllib.error import URLError
from urllib.request import Request, urlopen


DEFAULT_API_URL = "http://127.0.0.1:8000/events"

EVENT_TEMPLATES = [
    {
        "device_id": "pan-tilt-camera-01",
        "event_type": "motion_detected",
        "severity": "medium",
        "description": "Movement detected in the camera field of view",
    },
    {
        "device_id": "entry-camera-01",
        "event_type": "person_detected",
        "severity": "high",
        "description": "Person detected near the monitored entrance",
    },
    {
        "device_id": "door-sensor-01",
        "event_type": "door_opened",
        "severity": "low",
        "description": "Monitored door changed to the open state",
    },
    {
        "device_id": "environment-sensor-01",
        "event_type": "temperature_alert",
        "severity": "high",
        "description": "Temperature exceeded the configured threshold",
    },
]


def generate_event() -> dict:
    """Create one simulated security event."""
    event = random.choice(EVENT_TEMPLATES).copy()
    event["confidence"] = round(random.uniform(0.70, 0.99), 2)
    return event


def send_event(api_url: str, event: dict) -> tuple[int, dict]:
    """Send an event to the platform and return its response."""
    request = Request(
        api_url,
        data=json.dumps(event).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=5) as response:
        response_data = json.loads(response.read().decode("utf-8"))
        return response.status, response_data


def parse_arguments() -> argparse.Namespace:
    """Read simulator options from the command line."""
    parser = argparse.ArgumentParser(
        description="Send simulated device events to the security platform."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of events to send.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Seconds to wait between events.",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_API_URL,
        help="Security platform event endpoint.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the device simulator."""
    arguments = parse_arguments()

    print(f"Sending {arguments.count} events to {arguments.url}")

    for event_number in range(1, arguments.count + 1):
        event = generate_event()

        try:
            status_code, stored_event = send_event(arguments.url, event)
        except URLError as error:
            print(f"Connection failed: {error}")
            print("Confirm that the API server is running.")
            break

        print(
            f"[{event_number}/{arguments.count}] "
            f"{status_code} | "
            f"ID {stored_event['id']} | "
            f"{stored_event['device_id']} | "
            f"{stored_event['event_type']}"
        )

        if event_number < arguments.count:
            time.sleep(arguments.interval)


if __name__ == "__main__":
    main()