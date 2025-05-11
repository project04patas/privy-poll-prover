# rofl-service/app.py
import httpx
import json
import os
import time

print("PrivyPoll Prover ROFL Service Instance: Initializing...")

# Path to the Appd socket inside the container (mounted via compose.yaml)
APPD_SOCKET_PATH = "/run/rofl-appd.sock" 
# URL to use with the UDS transport for Appd (localhost is conventional for UDS)
APPD_BASE_URL = "http://localhost" # Appd listens on localhost via the socket

def get_rofl_app_id_from_appd():
    """Queries the Appd service to get this ROFL application's ID."""
    app_id_endpoint = "/rofl/v1/app/id" # As per Oasis slides
    full_url = APPD_BASE_URL + app_id_endpoint
    
    print(f"ROFL_PY: Attempting to connect to Appd via UDS: {APPD_SOCKET_PATH} for URL: {full_url}")
    
    try:
        # Create an HTTPTransport for Unix Domain Sockets
        transport = httpx.HTTPTransport(uds=APPD_SOCKET_PATH)
        # Create a client using that transport
        client = httpx.Client(transport=transport)

        print(f"ROFL_PY: Sending GET request to Appd: {app_id_endpoint}")
        response = client.get(full_url, timeout=30) # Make GET request to http://localhost/rofl/v1/app/id
        
        print(f"ROFL_PY: Appd response status: {response.status_code}")
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        app_id_data = response.json()
        my_app_id = app_id_data.get('app_id') # Slides show 'app_id', previous docs showed 'id'. Let's assume 'app_id'.
        
        print(f"SUCCESS - ROFL_PY: My App ID from Appd: {my_app_id}")
        return my_app_id

    except httpx.RequestError as exc:
        print(f"ERROR - ROFL_PY: HTTP RequestError calling Appd {app_id_endpoint}: {exc}")
    except httpx.HTTPStatusError as exc:
        print(f"ERROR - ROFL_PY: HTTP StatusError calling Appd {app_id_endpoint}: {exc.response.status_code} - {exc.response.text}")
    except json.JSONDecodeError as exc:
        print(f"ERROR - ROFL_PY: JSONDecodeError parsing Appd response for {app_id_endpoint}: {exc}")
        print(f"ROFL_PY: Appd raw response text: {response.text}")
    except Exception as e:
        print(f"ERROR - ROFL_PY: Unexpected error calling Appd {app_id_endpoint}: {type(e).__name__} - {e}")
    return None

# Main execution block
if __name__ == "__main__":
    print("ROFL_PY: Service script started. Waiting a few seconds for environment stability...")
    time.sleep(10) # Give some time for ROFL runtime and Appd to be fully up
    
    rofl_app_id_from_appd = get_rofl_app_id_from_appd()

    if rofl_app_id_from_appd:
        print(f"ROFL_PY: Successfully fetched App ID from Appd. My ROFL App ID is: {rofl_app_id_from_appd}. Idling.")
    else:
        print("ROFL_PY: Failed to fetch App ID from Appd. Please check errors. Idling.")
        
    # Keep the container alive for ROFL runtime & log inspection
    print("ROFL_PY: Entering idle loop. Press Ctrl+C in Docker logs to stop (if attached).")
    try:
        while True:
            time.sleep(3600) # Sleep for an hour
            print("ROFL_PY: Idling...")
    except KeyboardInterrupt:
        print("ROFL_PY: Service (app.py) received KeyboardInterrupt, shutting down.")
