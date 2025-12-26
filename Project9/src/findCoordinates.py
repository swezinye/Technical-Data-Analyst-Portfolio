"""
TomTom Geocoding - Find Coordinates from Addresses
"""
import time

import requests
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import os

# ============================================
# CONFIGURATION
# ============================================
MY_API_KEY = os.getenv("TOMTOM_KEY")
DEFAULT_LIMIT = 1


def _encode_address(address: str) -> str:
    """
    Encode address by replacing special characters with hex equivalents.

    Replaces:
    - Space (" ") → %20
    - Comma (",") → %2C
    - Pound sign ("#") → %23
    """
    return (
        address.replace(" ", "%20")
        .replace(",", "%2C")
        .replace("#", "%23")
    )


def findCoordinates(address, key=None) -> DataFrame:
    """
    Find coordinates (latitude and longitude) for given addresses using TomTom APIs.

    Primary: TomTom Geocoding API (geocode endpoint)
    Fallback: TomTom Search API (search endpoint) if geocode fails.

    Special characters (space, comma, pound) are URL encoded per assignment requirements.

    Parameters
    ----------
    address : list or pandas.Series
        List or Series of addresses for which to find coordinates.

    key : str, optional
        TomTom API key.

    Returns
    -------
    pandas.DataFrame
        Columns:
        - lat        : latitude (float or NaN if query failed)
        - lng        : longitude (float or NaN if query failed)
        - address    : address returned by TomTom (or original input if query fails)
        - status_code: HTTP status code from API request (int or None)
    """

    # Use provided key or default key
    if key is None:
        key = MY_API_KEY

    # Convert to list if Series
    if isinstance(address, Series):
        addresses = address.tolist()
    else:
        addresses = list(address)

    # API endpoints (primary: geocode)
    geocode_base = "https://api.tomtom.com/search/2/geocode"


    # Storage for results
    lats = []
    lngs = []
    addrs = []
    status_codes = []

    for addr in addresses:
        # Default "failed" values
        latitude = np.nan
        longitude = np.nan
        out_address = addr
        status_code = None

        # Encode special characters (per assignment)
        encoded_addr = _encode_address(str(addr))

        # Shared params for both endpoints
        params = {
            "key": key,
            "limit": DEFAULT_LIMIT,

        }


        #URL Request
        url = f"{geocode_base}/{encoded_addr}.json"
        try:
            response = requests.get(url, params=params, timeout=10)
            status_code = response.status_code
            time.sleep(.2)

        #Handle different status codes

            if status_code == 200:
                try:
                    data = response.json()
                    result_list = data.get("results", [])

                    if result_list:
                        result = result_list[0]

                        # Try BOTH entryPoints and main position
                        entry_position = None
                        main_position = result.get("position", {})

                        entry_points = result.get("entryPoints", [])
                        if entry_points:
                            # Look for main entry point first
                            for ep in entry_points:
                                if ep.get("type") == "main":
                                    entry_position = ep.get("position")
                                    if entry_position:
                                        break
                            # If no main, use first entry point
                            if not entry_position and entry_points:
                                entry_position = entry_points[0].get("position")

                        # Use entryPoints if available, otherwise main position
                        if entry_position and isinstance(entry_position, dict):
                            position = entry_position
                        else:
                            position = result.get("position",{})

                        if not isinstance(position, dict):
                            position = {}

                        lat_val = position.get("lat")
                        lon_val = position.get("lon")

                        if lat_val is not None and lon_val is not None:
                            latitude = lat_val
                            longitude = lon_val

                            #Address from TomTom if available-failed
                            addr_info = result.get("address", {})
                            out_address = addr_info.get("freeformAddress", out_address)

                except Exception:
                    # Any parsing error → leave default NaNs and original address
                    pass

            elif status_code == 429:
                latitude = np.nan
                longitude = np.nan
                out_address = addr

            else:
                latitude = np.nan
                longitude = np.nan
                out_address = addr

        except requests.RequestException:
            #Network error or timeout
            status_code = None
            latitute = np.nan
            longitude = np.nan
            out_address = addr

        # Append final values for this address
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