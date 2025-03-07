import csv
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key from environment variable
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")


def fetch_company_info(company_name: str, zone: str) -> dict:
    """Fetches details about a company using the Perplexity AI API."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a chemical industry intelligence analyst. Verify all data using at least 2 reliable sources (e.g., D&B, Bloomberg, official sites). "
                "For manufacturing tags, look for these exact phrases in the verified services: 'contract manufacturing' (case-insensitive), 'CRO', and 'CDMO' (both exact uppercase). "
                "Also, check the 'Contact Us' page or website footer for contact info and additional details on company operations. "
                "If the verified legal name or services cannot be confirmed 100%, return an empty JSON object. Do not include any extra commentary."
            )
        },
        {
            "role": "user",
            "content": (
                f"Analyze {company_name} in {zone} using verified records. Return EXACTLY the following JSON structure:\n\n"
                "{\n"
                "  \"name\": \"[Verified legal name]\",\n"
                "  \"services_offered\": [\"Official services only\"],\n"
                "  \"manufacturing_tags\": [\n"
                "       \"Contract Manufacturing\" (if exact phrase 'contract manufacturing' is found),\n"
                "       \"CRO\" (if exact uppercase match is found),\n"
                "       \"CDMO\" (if exact uppercase match is found)\n"
                "  ],\n"
                "  \"contact_information\": {\n"
                "    \"phone\": \"[Verified format: +1-XXX-XXX-XXXX]\",\n"
                "    \"email\": \"[Verified email format]\",\n"
                "    \"address\": \"[Verified HQ, ideally from Contact Us page or footer]\"\n"
                "  },\n"
                "  \"size_of_company\": \"[Employees from LinkedIn/D&B]\"\n"
                "}\n\n"
                "Return an empty JSON object if the name or services cannot be verified with 100% certainty. No additional explanations."
            )
        }
    ]

    response = client.chat.completions.create(model="sonar-pro", messages=messages)

    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        print(f"Invalid JSON response for {company_name}: {response.choices[0].message.content}")
        return None


def append_to_json_file(data: dict, file_path: str):
    """Append a JSON object to a JSON array stored in a file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                current_data = json.load(f)
        except json.JSONDecodeError:
            current_data = []
    else:
        current_data = []

    current_data.append(data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(current_data, f, indent=4)


def process_csv(file_path: str, json_output_path: str):
    """Reads a CSV file and fetches information for each company."""
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            company_name = row.get("Company")
            zone = row.get("Type")

            if company_name:
                info = fetch_company_info(company_name, zone)
                if info and info != {}:
                    print(info)
                    append_to_json_file(info, json_output_path)
                else:
                    minimal_obj = {"name": company_name, "error": "No valid data found"}
                    print(minimal_obj)
                    append_to_json_file(minimal_obj, json_output_path)


# Example usage
if __name__ == "__main__":
    CSV_FILE_PATH = "toll_manufacture.csv"  # Update with actual CSV file path
    JSON_OUTPUT_PATH = "final_chemexpo_data.json"  # File to save JSON output

    process_csv(CSV_FILE_PATH, JSON_OUTPUT_PATH)
    print(f"Data saved to {JSON_OUTPUT_PATH}")
