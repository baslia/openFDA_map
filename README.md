# openFDA Events Dashboard

![Dashboard Screenshot](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Dashboard](#running-the-dashboard)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

The **openFDA Events Dashboard** is an interactive web application built using [Plotly Dash](https://plotly.com/dash/) that visualizes drug adverse event data retrieved from the [openFDA API](https://open.fda.gov/apis/drug/event/). This dashboard provides users with insightful visualizations to analyze and explore FDA-reported adverse drug events, enabling stakeholders such as healthcare professionals, researchers, and the general public to make informed decisions based on real-world data.

## Features

- **Time Series Analysis**: View the number of adverse events reported each month for a selected year.
- **Top Reported Drugs**: Identify the top 10 drugs most frequently reported in adverse events.
- **Top Reactions**: Discover the most common adverse reactions associated with drugs.
- **Interactive Filters**: Select specific years to update all visualizations dynamically.
- **Data Table**: Explore a sample of adverse event reports in a tabular format.

## Prerequisites

Before setting up the dashboard, ensure you have the following installed on your machine:

- **Python** (version 3.7 or higher): [Download Python](https://www.python.org/downloads/)
- **pip**: Python package installer (comes bundled with Python)
- **Git** (optional, for cloning the repository): [Download Git](https://git-scm.com/downloads)

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine using Git. If you don't have Git installed, you can download the source code as a ZIP file and extract it.

```bash
git clone https://github.com/baslia/openfda_map.git
cd openfda-dashboard
```

### 2. Create a Virtual Environment (Optional but Recommended)

Creating a virtual environment isolates the project's dependencies from other Python projects on your system.

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows:**

  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

If a `requirements.txt` file is not provided, you can install the dependencies manually:

```bash
pip install dash plotly pandas requests
```

## Configuration

The dashboard fetches data from the openFDA API, which has certain rate limits:

- **Public Access**: 240 requests per minute. Each request can retrieve a maximum of 100 records.
- **API Key (Optional)**: For higher rate limits, you can obtain a free API key from [openFDA](https://open.fda.gov/apis/authentication/).

### Setting Up an API Key (Optional)

1. **Request an API Key**: Visit the [openFDA API Key Request Page](https://open.fda.gov/apis/authentication/) and follow the instructions to obtain a key.
2. **Configure the Application**: Modify the `fetch_openfda_data` function in `openfda_dashboard.py` to include your API key.

```python
params = {
    'api_key': 'YOUR_API_KEY_HERE',
    'search': 'patient.reaction.reactionmeddrapt:*',
    'limit': limit
}
```

**Note**: Replace `'YOUR_API_KEY_HERE'` with your actual API key.

## Running the Dashboard

Once the installation and configuration are complete, you can run the dashboard locally.

1. **Navigate to the Project Directory** (if not already there):

   ```bash
   cd openfda-dashboard
   ```

2. **Run the Application**:

   ```bash
   python openfda_dashboard.py
   ```

   You should see output similar to:

   ```
   Dash is running on http://127.0.0.1:8050/

   * Serving Flask app 'openfda_dashboard'
   * Debug mode: on
   ```

3. **Access the Dashboard**:

   Open your web browser and navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to view the dashboard.

## Usage

### Navigating the Dashboard

- **Year Selection Dropdown**: Located at the top of the dashboard, allow you to select the year for which you want to view adverse event data. All visualizations will update based on the selected year.

- **Time Series Plot**:
  - **Description**: Shows the number of reported adverse events each month for the selected year.
  - **Use Case**: Identify trends or spikes in adverse events over time.

- **Top Reported Drugs**:
  - **Description**: Displays a horizontal bar chart of the top 10 drugs most frequently reported in adverse events.
  - **Use Case**: Determine which drugs have the highest number of reported adverse events.

- **Top Reactions**:
  - **Description**: Shows a horizontal bar chart of the top 10 most common adverse reactions.
  - **Use Case**: Understand which adverse reactions are most frequently reported.

- **Data Table**:
  - **Description**: Presents a sample of adverse event reports in a table format, including drug name, reaction, patient age, and sex.
  - **Use Case**: Examine specific details of individual adverse event reports.

### Interactivity

- **Dynamic Updates**: Changing the year in the dropdown will automatically refresh all visualizations to reflect data from the selected year.
- **Hover Information**: Hover over data points in the charts to view detailed information such as exact counts and categories.

## Contributing

Contributions are welcome! If you'd like to improve the dashboard or add new features, please follow these steps:

1. **Fork the Repository**: Click the "Fork" button at the top right of the repository page.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/basli/openFDA_map.git
   cd openfda-dashboard
   ```

3. **Create a New Branch**:

   ```bash
   git checkout -b feature/awesome-feature
   ```

4. **Make Your Changes**: Implement your feature or fix.

5. **Commit Your Changes**:

   ```bash
   git commit -m "Add awesome feature"
   ```

6. **Push to Your Fork**:

   ```bash
   git push origin feature/awesome-feature
   ```

7. **Open a Pull Request**: Navigate to the original repository and open a pull request from your fork.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- **[openFDA](https://open.fda.gov/)**: For providing the comprehensive APIs used to access FDA data.
- **[Plotly Dash](https://plotly.com/dash/)**: For the powerful framework to build interactive dashboards.
- **[Pandas](https://pandas.pydata.org/)**: For data manipulation and analysis.
- **[Requests](https://docs.python-requests.org/)**: For handling HTTP requests to the openFDA API.

---