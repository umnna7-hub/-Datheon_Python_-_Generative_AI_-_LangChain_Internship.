# AI Structured JSON Extractor

An AI-powered information extraction tool that converts unstructured invoice and resume text into structured, validated JSON using a locally running Ollama model and Pydantic.

## Features

- Extracts invoice numbers, customer names, and total amounts.
- Extracts resume names, email addresses, phone numbers, skills, and years of experience.
- Uses reusable prompt templates.
- Validates extracted data with Pydantic.
- Handles missing fields using default values.
- Rejects invalid values, such as negative invoice amounts.
- Includes automated tests using pytest.
- Runs locally using Ollama without requiring a paid AI API key.

## Technologies

- Python
- Ollama
- Llama 3.2 (3B)
- Pydantic
- Pytest

## Prerequisites

- Python installed
- Ollama installed
- The `llama3.2:3b` model downloaded

Download the model by running:


ollama run llama3.2:3b


## Installation

Clone this repository and enter its folder:


git clone (https://github.com/umnna7-hub/-Datheon_Python_-_Generative_AI_-_LangChain_Internship..git)
cd structured-json-extractor


Create and activate a virtual environment on Windows:

python -m venv venv
.\venv\Scripts\Activate.ps1


Install the dependencies:


python -m pip install -r requirements.txt


Ensure Ollama is running and the model is available.

## Usage

Run the application:


python main.py


Choose either invoice or resume extraction, paste the document text, and type `END` on a new line when finished.

The application prints the extracted information as formatted JSON.

## Run Automated Tests


python -m pytest -v


The project includes tests for invoice extraction, resume extraction, missing fields, and negative invoice amounts.

## Limitations

- The current version accepts pasted text rather than PDF or image uploads.
- Extraction accuracy depends on the language model and input quality.
- Pydantic validates data structure and field constraints; it does not independently verify whether extracted information is factually correct.

## Future Improvements

- Add PDF and image input.
- Add more document types.
- Improve extraction accuracy with additional test cases.
- Add structured logging and more detailed error handling.

## Author

Created as an AI engineering internship project.