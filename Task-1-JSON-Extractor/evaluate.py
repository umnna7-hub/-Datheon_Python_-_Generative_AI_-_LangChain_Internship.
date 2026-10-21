
import json
from pathlib import Path
from datetime import datetime, timezone
from main import extract_information


def main():
    dataset_path = Path(__file__).parent / "evaluation_samples.json"

    with dataset_path.open("r", encoding="utf-8") as file:
        samples = json.load(file)

    total_fields = 0
    correct_fields = 0
    field_results = []

    print("=== Structured JSON Extractor Evaluation ===\n")

    for index, sample in enumerate(samples, start=1):
        print(f"Evaluating document {index}/{len(samples)}...")

        try:
            result = extract_information(
                sample["text"],
                sample["document_type"]
            )

            actual = result.model_dump()
            expected = sample["expected"]
            for field, expected_value in expected.items():
                total_fields += 1
                actual_value = actual.get(field)

                if actual_value == expected_value:
                    correct_fields += 1
                    status = "PASS"
                else:
                    status = "FAIL"

                field_results.append({
                    "document_type": sample["document_type"],
                    "field": field,
                    "expected": expected_value,
                    "actual": actual_value,
                    "status": status
                })
                print(
                    f"  {field}: {status} "
                    f"(expected={expected_value!r}, actual={actual_value!r})"
                )

        except Exception as error:
            print(f"  ERROR: {error}")

        print()
    accuracy = correct_fields / total_fields * 100 if total_fields else 0.0

    report = {
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "total_documents": len(samples),
        "total_fields": total_fields,
        "correct_fields": correct_fields,
        "accuracy_percent": round(accuracy, 2),
        "results": field_results
    }

    report_path = Path(__file__).parent / "evaluation_report.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("\n=== Evaluation Summary ===")
    print(f"Correct fields: {correct_fields}/{total_fields}")
    if total_fields:
        print(f"Field-level accuracy: {accuracy:.2f}%")
    else:
        print("No fields were evaluated.")
    print(f"Report saved to: {report_path.name}")


if __name__ == "__main__":
    main()