
import json


EXAMPLES = {
    "invoice": [
        {
            "input": """
Invoice Number: INV-101
Customer: Ahmed Ali
Total: Rs. 5000
""",
            "output": {
                "invoice_number": "INV-101",
                "customer_name": "Ahmed Ali",
                "total_amount": 5000
            }
        },
        {
            "input": """
Invoice No: BILL-202
Billed to: Sara Khan
Amount Due: Rs. 12,750.50
""",
            "output": {
                "invoice_number": "BILL-202",
                "customer_name": "Sara Khan",
                "total_amount": 12750.50
            }
        }
    ],
    "resume": [
        {
            "input": """
Name: Ahmed Ali
Email: ahmed@example.com
Phone: 03001234567
Skills: Python, SQL
Experience: 3 years
""",
            "output": {
                "full_name": "Ahmed Ali",
                "email": "ahmed@example.com",
                "phone": "03001234567",
                "skills": ["Python", "SQL"],
                "years_of_experience": 3
            }
        },
        {
            "input": """
Candidate: Sara Khan
Contact: sara@example.com
Technical Skills: Java, Git, MySQL
Professional Experience: 2 years
""",
            "output": {
                "full_name": "Sara Khan",
                "email": "sara@example.com",
                "phone": "",
                "skills": ["Java", "Git", "MySQL"],
                "years_of_experience": 2
            }
        }
    ]
}


def build_prompt(document_type: str, schema: dict) -> str:
    examples = EXAMPLES[document_type]

    formatted_examples = ""

    for example in examples:
        formatted_examples += (
            "\nExample input:\n"
            + example["input"]
            + "\nExpected JSON output:\n"
            + json.dumps(example["output"], indent=2)
            + "\n"
        )

    return f"""
You are a structured information extraction assistant.

Document type: {document_type}

Extract information from the user's document.

The required JSON schema is:
{json.dumps(schema, indent=2)}

Learn the expected extraction format from these examples:
{formatted_examples}

Rules:
1. Extract actual values from the user's document.
2. Return extracted data, not the schema.
3. Use only information supported by the document.
4. Never copy example values into a new result.
5. Use an empty string for missing string fields.
6. Use an empty list for missing skills.
7. Use null for missing numeric fields.
8. Return a JSON object only, without Markdown.
"""
