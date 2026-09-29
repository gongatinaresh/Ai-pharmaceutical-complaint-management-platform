from app.ai.graph import complaint_graph


complaint_text = """
Dear Quality Team,

We received a customer complaint from MedPlus Pharmacy.

Customer Name: MedPlus Pharmacy
Product: Paracetamol Tablets
Strength: 500 mg
Batch Number: PCM240501
Manufacturing Date: 2024-05-01
Expiry Date: 2026-04-30
Quantity Affected: 20 tablets

Complaint Date: 2026-09-10

The customer reported that several tablets were broken inside the
blister pack. No adverse event was reported.

Please investigate this issue.

Regards,
Customer Support Team
"""


result = complaint_graph.invoke(
    {
        "complaint_text": complaint_text
    }
)


print("\n========== AI COMPLAINT RESULT ==========\n")

print("EXTRACTED DATA:")
print(result.get("extracted_data"))

print("\nMISSING FIELDS:")
print(result.get("missing_fields"))

print("\nCOMPLETE:")
print(result.get("is_complete"))

print("\nCATEGORY:")
print(result.get("complaint_category"))

print("\nSEVERITY:")
print(result.get("severity"))

print("\nPRIORITY:")
print(result.get("priority"))

print("\nRISK LEVEL:")
print(result.get("risk_level"))

print("\nRISK REASON:")
print(result.get("risk_reason"))

print("\nSUMMARY:")
print(result.get("summary"))

print("\nDUPLICATE:")
print(result.get("possible_duplicate"))

print("\nDUPLICATE IDS:")
print(result.get("duplicate_complaint_ids"))

print("\nDUPLICATE REASON:")
print(result.get("duplicate_reason"))

print("\nERROR:")
print(result.get("error"))