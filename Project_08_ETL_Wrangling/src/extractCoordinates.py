# extractCoordinates.py
import re
import pandas as pd

_COORD_RE = re.compile(r"\(\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*\)")



"""
    Extract latitude and longitude from coordinate strings into separate numeric columns.
    
    This function parses coordinate strings in the format "(latitude, longitude)" from
    a DataFrame column and extracts the latitude and longitude values into separate
    numeric columns. It validates that required columns exist (using case-insensitive
    matching) and converts extracted string values to proper numeric types.

    Args:
        dat (pd.DataFrame): Input DataFrame containing two required columns (case-insensitive):
        station: Station names/identifiers (str).
        coordinates: Coordinate strings in (lat, lon) format (str).

    Returns:
        pd.DataFrame: If successful, a DataFrame with columns:
        station (str): Original station identifier.
        lat (float): Extracted latitude value.
        lon (float): Extracted longitude value. 

    Error Codes (int): If validation fails, returns a specific integer:
        -1: 'station' column is missing.
        -2: 'coordinates' column is missing.

    Empty DataFrame: If input dat is None or empty, returns an empty DataFrame with the expected output columns.

"""
def extractCoordinates(dat: pd.DataFrame):
    # Return empty DataFrame with correct column structure
    if dat is None or dat.empty:
        return pd.DataFrame(columns=["station", "lat", "lon"])

    # Create case-insensitive column lookup
    cols_lower = {c.lower(): c for c in dat.columns}

    # Validate that required 'station' column exists
    # Return error code -1 if missing
    if "station" not in cols_lower:
        return -1
    # Validate that required 'coordinates' column exists
    # Return error code -2 if missing
    if "coordinates" not in cols_lower:
        return -2
    # Get actual column names (preserving original case)
    s_col = cols_lower["station"]
    c_col = cols_lower["coordinates"]

    def _parse(s):
        """
        Extract latitude and longitude from a single coordinate string.

        Searches the input string for the coordinate pattern and extracts
        the latitude and longitude values as strings. Returns None for both
        if the pattern is not found or input is not a string.

        Args:
            s: A value from the coordinates column (typically a string)

        Returns:
            tuple: (latitude_string, longitude_string) if pattern found
                   (None, None) if input is not a string or pattern not found

        """
        # Only process string values
        if not isinstance(s, str):
            return (None, None)
        # Search for coordinate pattern in the string
        m = _COORD_RE.search(s)

        # Extract matched groups (group 1 = latitude, group 2 = longitude)
        # If no match found, return (None, None)
        return (m.group(1), m.group(2)) if m else (None, None)

    latlon = dat[c_col].apply(_parse)
    # Convert Series of tuples to DataFrame with columns ["lat", "lon"]
    # tolist() converts tuples to a list, then unpack into DataFrame columns
    out = pd.DataFrame(latlon.tolist(), columns=["lat", "lon"])
    # Add the station column from the original DataFrame
    out["station"] = dat[s_col].values
    # Convert latitude string values to numeric (float) type
    # errors="coerce" converts unparseable values to NaN
    out["lat"] = pd.to_numeric(out["lat"], errors="coerce")
    # Convert longitude string values to numeric (float) type
    # errors="coerce" converts unparseable values to NaN
    out["lon"] = pd.to_numeric(out["lon"], errors="coerce")
    # Return DataFrame with columns in required order: station, lat, lon
    return out[["station", "lat", "lon"]]

