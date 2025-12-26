"""
TomTom Reverse Geocoding - Find Address from Coordinates
"""

import requests
import time
from pandas import DataFrame
import os

# ============================================
# CONFIGURATION
# ============================================
MY_API_KEY = os.getenv("TOMTOM_KEY")
DEFAULT_LIMIT = 1


def findAddress(lat, lng, key=None) -> DataFrame | None:
    """
    Find address for given coordinates (latitude and longitude)
    using TomTom Reverse Geocoding API.

    Parameters
    ----------
    lat : tuple of floats
        Latitude coordinates.

    lng : tuple of floats
        Longitude coordinates.

    key : str, optional
        TomTom API key. If None, uses MY_API_KEY.

    Returns
    -------
    pandas.DataFrame or None
        DataFrame with columns:
            - address     : formatted address (string or None if query failed)
            - status_code : HTTP status code from API request (int or None)

        Returns None if lat and lng do not have the same length.
    """

    # TYPE CHECK FIRST
    if not isinstance(lat, tuple) or not isinstance(lng, tuple):
        return None

    # LENGTH CHECK
    if len(lat) != len(lng):
        return None

    # Use provided key or default key
    if key is None:
        key = MY_API_KEY

    # API endpoint
    base_url = "https://api.tomtom.com/search/2/reverseGeocode"

    # Storage for results
    addresses = []
    status_codes = []

    # Process each coordinate pair
    for latitude, longitude in zip(lat, lng):
        formatted_address = None
        status_code = None
        response = None

        try:
            # Construct API query with format: latitude,longitude
            query_url = f"{base_url}/{latitude},{longitude}.json"
            params = {
                "key": key,
                "language": "en-US",
                "limit": DEFAULT_LIMIT,
                "ext": "json"
            }

            # Retry loop with exponential backoff
            max_attempts = 5
            for attempt in range(max_attempts):
                try:
                    response = requests.get(query_url, params=params, timeout=10)
                    status_code = response.status_code

                    # Success (200) or permanent error (not 429) - stop retrying
                    if status_code != 429:
                        break

                    # Rate limited (429) - exponential backoff
                    if attempt < max_attempts - 1:
                        wait_time = 2 ** attempt
                        time.sleep(wait_time)

                except (requests.exceptions.Timeout, requests.exceptions.RequestException):
                    # Network error - retry with sleep
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                    continue

            # Parse response only if successful
            if response is not None and status_code == 200:
                try:
                    data = response.json()
                    address_list = data.get("addresses", [])

                    if address_list:
                        address_result = address_list[0]
                        addr_obj = address_result.get("address", {})
                        formatted_address = addr_obj.get("freeformAddress", None)

                except Exception:
                    pass

        except Exception:
            pass

        addresses.append(formatted_address)
        status_codes.append(status_code)

    # Construct DataFrame efficiently from lists
    df = DataFrame({
        "address": addresses,
        "status_code": status_codes
    })

    return df