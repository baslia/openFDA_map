import requests
import pandas as pd


def fetch_openfda_data(limit=1000):
    """
    Fetches drug adverse event data from the openFDA API.

    Parameters:
    - limit: Number of records to fetch (max 1000 per request)

    Returns:
    - DataFrame containing the fetched data
    """
    url = 'https://api.fda.gov/drug/event.json'
    params = {
        'search': 'patient.reaction.reactionmeddrapt:*',
        'limit': limit
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        records = []
        for entry in results:
            record = {}
            # Extracting some key fields
            record['receivedate'] = entry.get('receivedate')
            record['patient_age'] = entry.get('patient', {}).get('patientage', None)
            record['patient_sex'] = entry.get('patient', {}).get('patientsex', None)
            record['drug_name'] = entry.get('patient', {}).get('drug', [{}])[0].get('medicinalproduct', None)
            record['reaction'] = entry.get('patient', {}).get('reaction', [{}])[0].get('reactionmeddrapt', None)
            records.append(record)
        df = pd.DataFrame(records)
        # Convert receivedate to datetime
        df['receivedate'] = pd.to_datetime(df['receivedate'], format='%Y%m%d', errors='coerce')
        return df
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()


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

    # Extract year and month for time series
    df['year'] = df['receivedate'].dt.year
    df['month'] = df['receivedate'].dt.month

    # Map patient sex
    sex_mapping = {1: 'Male', 2: 'Female', 0: 'Unknown'}
    df['patient_sex'] = df['patient_sex'].map(sex_mapping)

    return df