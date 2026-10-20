
import json

import ollama
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from prompts import build_prompt


class Invoice(BaseModel):
    model_config = ConfigDict(extra="ignore")

    invoice_number: str = ""
    customer_name: str = ""
    total_amount: float | None = Field(default=None, ge=0)

class Resume(BaseModel):
    model_config = ConfigDict(extra="ignore")

    full_name: str = ""
    email: str = ""
    phone: str = ""
    skills: list[str] = Field(default_factory=list)
    years_of_experience: float = Field(default=0, ge=0)


def extract_information(text: str, document_type: str):
    # Choose the appropriate schema
    schemas = {
        "invoice": Invoice,
        "resume": Resume,
    }

    if document_type not in schemas:
        raise ValueError("Choose 'invoice' or 'resume'.")

    model_class = schemas[document_type]
    schema = model_class.model_json_schema()

    # Build a reusable prompt
    system_prompt = build_prompt(
        document_type=document_type,
        schema=schema,
    )

    # Ask the local AI model
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        format=schema,
        options={"temperature": 0},
    )

    raw_json = response["message"]["content"]

    # Validate the JSON against the selected schema
    return model_class.model_validate_json(raw_json)


def main():
    print("=== AI Document Information Extractor ===")
    print("1. Invoice")
    print("2. Resume")

    choice = input("Choose document type (1 or 2): ").strip()

    document_types = {
        "1": "invoice",
        "2": "resume",
    }

    if choice not in document_types:
        print("Invalid choice.")
        return

    document_type = document_types[choice]

    print("\nPaste your document text.")
    print("Type END on a new line when finished.")

    lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    document_text = "\n".join(lines).strip()

    if not document_text:
        print("No document text provided.")
        return

    try:
        result = extract_information(
            document_text,
            document_type,
        )

        print("\nValidated JSON:")
        print(result.model_dump_json(indent=2))

    except ValidationError as error:
        print("\nThe extracted data failed validation.")
        print("The model may have returned incorrect or incomplete data.")
        print(error)

    except Exception as error:
        print("\nCould not extract information.")
        print("Check that Ollama is running and the model is available.")
        print(f"Technical details: {error}")


if __name__ == "__main__":
    main()
