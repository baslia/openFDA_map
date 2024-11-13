import os

import requests
import pandas as pd


def fetch_openfda_data(event_types=['drug'], limit=1000, api_key=None):
    """
    Fetches event data from the openFDA API for specified event types.

    Parameters:
    - event_types: list of strings specifying event types to fetch (e.g., ['drug', 'food'])
    - limit: Number of records to fetch per event type (max 1000 per request)
    - api_key: (Optional) String containing the openFDA API key for higher rate limits

    Returns:
    - DataFrame containing the combined and processed data from specified event types
    """
    base_url = 'https://api.fda.gov/{}/event.json'
    headers = {'User-Agent': 'openFDA Dashboard'}

    all_records = []

    for event_type in event_types:
        if event_type not in ['drug', 'food']:
            print(f"Unsupported event type: {event_type}. Skipping.")
            continue

        url = base_url.format(event_type)
        params = {
            'search': 'patient.reaction.reactionmeddrapt:*',
            'limit': limit
        }

        if api_key:
            params['api_key'] = api_key

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            for entry in results:
                record = {}
                # Common fields
                record['event_type'] = event_type.capitalize()
                record['receivedate'] = entry.get('receivedate')

                # Patient Information
                patient = entry.get('patient', {})
                record['patient_age'] = patient.get('patientage', None)
                sex = patient.get('patientsex', None)
                sex_mapping = {1: 'Male', 2: 'Female', 0: 'Unknown'}
                record['patient_sex'] = sex_mapping.get(sex, 'Unknown')

                # Reaction Information
                reactions = patient.get('reaction', [])
                if reactions:
                    record['reaction'] = reactions[0].get('reactionmeddrapt', None)
                else:
                    record['reaction'] = None

                # Event-specific Information
                if event_type == 'drug':
                    drugs = patient.get('drug', [])
                    if drugs:
                        record['product_name'] = drugs[0].get('medicinalproduct', None)
                    else:
                        record['product_name'] = None
                elif event_type == 'food':
                    foods = patient.get('food', [])
                    if foods:
                        record['product_name'] = foods[0].get('food', None)
                    else:
                        record['product_name'] = None

                all_records.append(record)
        else:
            print(f"Error fetching {event_type} data: {response.status_code} - {response.text}")

    if not all_records:
        print("No data fetched. Returning an empty DataFrame.")
        return pd.DataFrame()

    df = pd.DataFrame(all_records)

    # Convert receivedate to datetime
    df['receivedate'] = pd.to_datetime(df['receivedate'], format='%Y%m%d', errors='coerce')

    # Extract year and month for time series
    df['year'] = df['receivedate'].dt.year
    df['month'] = df['receivedate'].dt.month

    return df


def process_data(df):
    """
    Processes the DataFrame for visualization.

    Parameters:
    - df: Raw DataFrame from openFDA

    Returns:
    - Processed DataFrame
    """
    # Drop rows with missing receivedate
    df = df.dropna(subset=['receivedate'])

    # Fill missing product_names with 'Unknown'
    df['product_name'] = df['product_name'].fillna('Unknown')

    # Fill missing reactions with 'Unknown'
    df['reaction'] = df['reaction'].fillna('Unknown')

    # Convert patient_age to numeric, coerce errors to NaN
    df['patient_age'] = pd.to_numeric(df['patient_age'], errors='coerce')

    # Extract year and month for time series
    df['year'] = df['receivedate'].dt.year
    df['month'] = df['receivedate'].dt.month

    # Additional processing if needed
    # For example, categorizing ages
    bins = [0, 18, 35, 50, 65, 100]
    labels = ['0-18', '19-35', '36-50', '51-65', '66+']
    df['age_group'] = pd.cut(df['patient_age'], bins=bins, labels=labels, right=False)

    return df