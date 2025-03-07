# CompanyDataStack

This project fetches detailed company information using the Perplexity AI API and processes CSV data to extract and store insights about companies in the chemical industry.

## Features

- **Fetch Company Information:** Uses the Perplexity AI API to retrieve verified details.
- **Structured Data Collection:** Retrieves specific data points in a standardized JSON format:
  - Verified legal company name
  - Official services offered
  - Manufacturing tags (Contract Manufacturing, CRO, CDMO)
  - Contact information (phone, email, headquarters address)
  - Company size (employee count from LinkedIn/D&B)
- **Intelligent Data Parsing:** Identifies manufacturing capabilities based on keyword recognition.
- **Verified Contact Details:** Sources contact information from official company websites.
- **CSV Processing:** Reads company details from a CSV file and appends results to a JSON output file.
- **Environment Variables:** Uses a `.env` file to securely store API credentials.
- **Error Handling:** Provides minimal output for companies that cannot be verified.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/companydatastack.git
cd companydatastack
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Rename `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Prepare Your CSV File

Ensure your CSV file (e.g., `toll_manufacture.csv`) has the following columns:
* `Company` – The company name.
* `Type` – The company type or zone.

### Run the Script

```bash
python fetch_company_info.py
```

The script will process the CSV and create/update `final_chemexpo_data.json` with the output.

## License

Include your license information here if applicable.

## Contributing

Feel free to open issues or submit pull requests if you have any improvements.