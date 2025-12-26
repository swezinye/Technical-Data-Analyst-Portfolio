"""
TomTom API Project - Geocoding and Reverse Geocoding
"""

import requests
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import time
from typing import Tuple, Optional, Any, List
import os
from dotenv import load_dotenv

# ============================================
# CONFIGURATION - ADD YOUR API KEY HERE
# ============================================
# NOTE: Replace the placeholder with your actual key.

load_dotenv()

MY_API_KEY = os.getenv("TOMTOM_KEY")
DEFAULT_LIMIT = 1


def _encode_address(address: str) -> str:
    """
    Encode address by replacing special characters with hex equivalents.
    """
    return (
        address.replace(" ", "%20")
        .replace(",", "%2C")
        .replace("#", "%23")
    )


# --- Helper for API calls with Retries ---
def _call_and_retry(base_url: str, encoded_addr: str, params: dict) -> Optional[requests.Response]:
    """Handles API call for both geocode and search with exponential backoff for 429."""
    url = f"{base_url}/{encoded_addr}.json"
    max_attempts = 5
    response = None

    for attempt in range(max_attempts):
        try:
            response = requests.get(url, params=params, timeout=10)

            # If successful or not a rate limit error, break
            if response.status_code != 429:
                return response

            # If 429 and retries remain, wait
            if attempt < max_attempts - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
        except requests.RequestException:
            return None  # Return None on network failure (like timeout)

    return response


# ---------------------------------------------------------------------
# Problem 1 - findCoordinates (FIXED)
# ---------------------------------------------------------------------
def findCoordinates(address: List[str] | Series, key: Optional[str] = None) -> DataFrame:
    """
    Find coordinates (latitude and longitude) for given addresses using TomTom APIs.
    """

    key_to_use = key if key is not None else MY_API_KEY
    addresses = address.tolist() if isinstance(address, Series) else list(address)

    geocode_base = "https://api.tomtom.com/search/2/geocode"
    search_base = "https://api.tomtom.com/search/2/search"

    lats = []
    lngs = []
    addrs = []
    status_codes = []

    for addr in addresses:
        latitude = np.nan
        longitude = np.nan
        out_address = addr
        status_code = None

        encoded_addr = _encode_address(str(addr))

        params = {
            "key": key_to_use,
            "language": "en-US",
            "limit": DEFAULT_LIMIT,
            "ext": "json"
        }

        # 1) Try Geocoding endpoint first (with retry logic)
        response = _call_and_retry(geocode_base, encoded_addr, params)

        # 2) If geocode failed or not 200, try Search endpoint as fallback
        if response is None or response.status_code != 200:
            response = _call_and_retry(search_base, encoded_addr, params)

        if response is not None:
            status_code = response.status_code

            if status_code == 200:
                try:
                    data = response.json()
                    result_list = data.get("results", [])

                    if result_list:
                        result = result_list[0]
                        position = result.get("position", {})

                        entry_points = result.get("entryPoints", [])
                        if entry_points:
                            main_ep = next((ep for ep in entry_points if ep.get("type") == "main"), entry_points[0])
                            position = main_ep.get("position", position)

                        lat_val = position.get("lat")
                        lon_val = position.get("lon")

                        if lat_val is not None and lon_val is not None:
                            latitude = lat_val
                            longitude = lon_val

                        addr_info = result.get("address", {})
                        out_address = addr_info.get("freeformAddress", out_address)

                except Exception:
                    pass

        lats.append(latitude)
        lngs.append(longitude)
        addrs.append(out_address)
        status_codes.append(status_code)

    df = DataFrame({
        "lat": lats,
        "lng": lngs,
        "address": addrs,
        "status_code": status_codes
    })

    return df


# ---------------------------------------------------------------------
# Problem 2 - findAddress (FIXED)
# ---------------------------------------------------------------------
def findAddress(lat: Tuple[Any, ...], lng: Tuple[Any, ...], key: Optional[str] = None) -> Optional[DataFrame]:
    """
    Find address for given coordinates (latitude and longitude)
    using TomTom Reverse Geocoding API. Includes input validation and retries.
    """

    # --- CRITICAL Type Check (Fixes TypeError) ---
    if not isinstance(lat, tuple) or not isinstance(lng, tuple):
        return None

    # Check that lat and lng have same length
    if len(lat) != len(lng):
        return None
    # ---------------------------------------------

    key_to_use = key if key is not None else MY_API_KEY
    base_url = "https://api.tomtom.com/search/2/reverseGeocode"

    addresses = []
    status_codes = []

    for latitude, longitude in zip(lat, lng):
        formatted_address = None
        status_code = None

        try:
            query_url = f"{base_url}/{latitude},{longitude}.json"
            params = {
                "key": key_to_use,
                "language": "en-US",
                "limit": DEFAULT_LIMIT,
                "ext": "json"
            }

            # --- Exponential Backoff ---
            max_attempts = 5
            response = None
            for attempt in range(max_attempts):
                response = requests.get(query_url, params=params, timeout=10)
                status_code = response.status_code

                if status_code != 429:
                    break

                if attempt < max_attempts - 1:
                    time.sleep(2 ** attempt)
            # ---------------------------

            if status_code == 200 and response is not None:
                data = response.json()
                address_list = data.get("addresses", [])

                if address_list:
                    address_result = address_list[0]
                    addr_obj = address_result.get("address", {})
                    formatted_address = addr_obj.get("freeformAddress", None)

        except Exception:
            pass

        addresses.append(formatted_address)
        status_codes.append(status_code)

    df = DataFrame({
        "address": addresses,
        "status_code": status_codes
    })

    return df