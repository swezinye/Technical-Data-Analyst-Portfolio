# TomTom Geocoding & API Integration

This project implements a robust Python toolkit for interacting with the TomTom Search API. It provides automated solutions for Geocoding (address to coordinates) and Reverse Geocoding (coordinates to address).

## 🚀 Features
- **Smart Geocoding:** Converts physical addresses or landmarks into precise Latitude and Longitude coordinates.
- **Entry Point Logic:** Automatically prioritizes "main" entry points over general position data to ensure higher accuracy for navigation-based tasks.
- **Reverse Geocoding:** Translates geographic coordinates back into human-readable freeform addresses.
- **Resilience Engine:** Implements exponential backoff and retry logic to handle API rate limits (Status Code 429) and network timeouts.
- **Safe Encoding:** Custom URL encoding handles special characters like spaces, commas, and pound signs to prevent query failures.



## 🛠️ Technical Implementation
- **Requests & JSON:** Manages RESTful API communication and parses complex nested JSON responses.
- **Pandas Integration:** Returns data in structured DataFrames, including API status codes for easy debugging and auditing.
- **Validation:** Includes strict input checks to ensure coordinate tuples match in length before executing remote calls.

## 📊 Sample Usage
```python
from PJ9 import findCoordinates, findAddress

# Geocoding
addresses = ["Yankee Stadium, New York", "Fenway Park, Boston"]
coords_df = findCoordinates(addresses)

# Reverse Geocoding
lats = (40.829, 42.345)
lngs = (-73.926, -71.098)
address_df = findAddress(lats, lngs)