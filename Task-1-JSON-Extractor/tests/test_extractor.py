
import json
import pytest
import main
from pydantic import ValidationError


def test_invoice_extraction(monkeypatch):
    def fake_chat(**kwargs):
        return {
            "message": {
                "content": json.dumps({
                    "invoice_number": "INV-104",
                    "customer_name": "Ali Khan",
                    "total_amount": 12500
                })
            }
        }

    monkeypatch.setattr(main.ollama, "chat", fake_chat)

    result = main.extract_information(
        "Invoice Number: INV-104",
        "invoice"
    )

    assert result.invoice_number == "INV-104"
    assert result.customer_name == "Ali Khan"
    assert result.total_amount == 12500


def test_resume_extraction(monkeypatch):
    def fake_chat(**kwargs):
        return {
            "message": {
                "content": json.dumps({
                    "full_name": "Sara Ahmed",
                    "email": "sara@example.com",
                    "phone": "03001234567",
                    "skills": ["Python", "SQL", "Git"],
                    "years_of_experience": 2
                })
            }
        }

    monkeypatch.setattr(main.ollama, "chat", fake_chat)

    result = main.extract_information(
        "Name: Sara Ahmed",
        "resume"
    )

    assert result.full_name == "Sara Ahmed"
    assert result.skills == ["Python", "SQL", "Git"]
    assert result.years_of_experience == 2


def test_missing_resume_fields(monkeypatch):
    def fake_chat(**kwargs):
        return {
            "message": {
                "content": json.dumps({
                    "full_name": "Ali Khan",
                    "skills": ["Java", "MySQL"]
                })
            }
        }

    monkeypatch.setattr(main.ollama, "chat", fake_chat)

    result = main.extract_information(
        "Name: Ali Khan; Skills: Java and MySQL",
        "resume"
    )

    assert result.email == ""
    assert result.phone == ""
    assert result.skills == ["Java", "MySQL"]
    assert result.years_of_experience == 0


def test_negative_invoice_amount_is_rejected(monkeypatch):
    def fake_chat(**kwargs):
        return {
            "message": {
                "content": json.dumps({
                    "invoice_number": "INV-105",
                    "customer_name": "Ali Khan",
                    "total_amount": -500
                })
            }
        }

    monkeypatch.setattr(main.ollama, "chat", fake_chat)

    with pytest.raises(ValidationError):
        main.extract_information(
            "Invoice total: -500",
            "invoice"
        )


def test_invalid_document_type():
    with pytest.raises(ValueError):
        main.extract_information("Some document text", "passport")


def test_invalid_json_output(monkeypatch):
    def fake_chat(**kwargs):
        return {
            "message": {
                "content": "This is not valid JSON"
            }
        }

    monkeypatch.setattr(main.ollama, "chat", fake_chat)

    with pytest.raises(ValidationError):
        main.extract_information("Invoice Number: INV-200", "invoice")

def test_missing_invoice_amount(monkeypatch):
    def fake_chat(**kwargs):
        return {
            "message": {
                "content": json.dumps({
                    "invoice_number": "INV-902",
                    "customer_name": "Usman Ahmed",
                    "total_amount": None
                })
            }
        }

    monkeypatch.setattr(main.ollama, "chat", fake_chat)

    result = main.extract_information(
        "Invoice No: INV-902; Customer: Usman Ahmed",
        "invoice"
    )

    assert result.invoice_number == "INV-902"
    assert result.customer_name == "Usman Ahmed"
    assert result.total_amount is None

def test_zero_invoice_amount_is_preserved(monkeypatch):
    def fake_chat(**kwargs):
        return {
            "message": {
                "content": json.dumps({
                    "invoice_number": "INV-904",
                    "customer_name": "Ayesha Malik",
                    "total_amount": 0
                })
            }
        }

    monkeypatch.setattr(main.ollama, "chat", fake_chat)

    result = main.extract_information(
        "Invoice No: INV-904; Customer: Ayesha Malik; Total: Rs. 0",
        "invoice"
    )

    assert result.total_amount == 0
    assert result.total_amount is not None
