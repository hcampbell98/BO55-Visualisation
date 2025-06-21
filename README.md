# Lisense Analysis - BO55 Plates

This Python application analyzes vehicle data from a CSV file and generates visualizations of vehicle makes. The data in the CSV file is sourced directly from the DVSA API.

## Overview

The tool loads vehicle data from a CSV file and creates a high-quality visualization showing the distribution of vehicle makes. It uses a modern dark-themed style with a custom color palette.

## Files

-   `app.py` - Main Python script containing data loading and visualization functions
-   `bo55_plates.csv` - Input CSV data file containing vehicle information
-   `vehicle_makes.png` - Output visualization of vehicle makes

## Features

-   Loads and processes vehicle data from CSV
-   Creates a modern visualization of the top 12 vehicle makes
-   Includes proper attribution and timestamp on the generated visualization
-   Error handling for file loading issues

## Usage

Run the script with Python:

```python
python app.py
```
