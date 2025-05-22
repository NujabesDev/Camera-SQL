# Chicago Traffic Camera Analysis

## Overview
A database analysis tool for exploring Chicago's traffic camera violations data. This project connects to a SQLite database containing red light and speed camera information, allowing users to perform various analyses through a command-line interface.

## Requirements
- Python 3.x
- SQLite3
- matplotlib
- Official Chicago traffic camera database

## Installation

1. Clone or download this repository
2. Download the official Chicago traffic camera data:
   - [Speed Camera Violations](https://data.cityofchicago.org/Transportation/Speed-Camera-Violations/hhkd-xvj4/about_data)
   - [Red Light Camera Violations](https://data.cityofchicago.org/Transportation/Red-Light-Camera-Violations/spqx-js37/about_data)
3. Convert the data to a SQLite database named "chicago-traffic-cameras.db"
4. Place the database file in the same directory as main.py
5. Ensure "chicago.png" (map file) is in the same directory for mapping functionality

## Usage
Run the program with:
```
python main.py
```

For automated testing using predefined inputs:
```
python main.py input.txt
```

## Features
The program displays a menu with 9 analysis options:

1. **Find an intersection by name** - Search with wildcards support
2. **Find all cameras at an intersection** - Lists both red light and speed cameras
3. **Percentage of violations for a specific date** - Breakdown of violation types
4. **Number of cameras at each intersection** - With percentage of total cameras
5. **Number of violations at each intersection for a year** - Sorted by violation count
6. **Number of violations by year for a camera** - With optional trend plotting
7. **Monthly violation breakdown** - Analyze patterns by month with plotting
8. **Compare red light and speed violations** - Year-long comparison with visualization
9. **Find cameras on a street** - With map visualization of camera locations

## Implementation Details
- Uses SQLite for database queries
- Implements matplotlib for data visualization
- Includes map overlay functionality for geographic display
- Handles data gaps and edge cases
- Organizes code with a function-based approach

## Known Issues
- Map visualization annotations can be cluttered with many cameras
- Limited error handling for malformed database files

## Author
Matthew Witkowski - CS341 Spring 2025

## Acknowledgements
- Chicago Data Portal for providing the open data
- course staff for project requirements and guidance
