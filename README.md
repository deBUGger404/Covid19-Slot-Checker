# COVID Vaccination Slot Availability Checker

This is a Python script that utilizes the Streamlit framework to create a web application for checking COVID-19 vaccination slot availability in different districts of India. The script fetches data from the CoWIN API, processes it, and displays the information in a tabular format on a Streamlit app.

## Features

- Select the number of days to show vaccination availability using a slider.
- Choose a district name from the dropdown menu to view availability in that district.
- Filter vaccination centers by pincode, minimum age, and availability.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- Streamlit
- Pandas
- Requests

You can install the required packages using the following command:

```bash
pip install streamlit pandas requests

Clone this repository to your local machine:

https://github.com/deBUGger404/Covid19-Slot-Checker.git

Navigate to the project directory:

cd Covid19-Slot-Checker

Run the Streamlit app:

streamlit run app.py

Interact with the app through your web browser. Select the number of days, district name, and use the filters to view vaccination slot availability.

## Data Source
The district-wise data is obtained from the "district_code.csv" file, which is used to map district names to their corresponding district IDs.

Feel free to contribute, report issues, or provide suggestions for improvement. Contributions are always welcome!

