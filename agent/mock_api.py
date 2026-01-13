def submit_lead_to_crm(payload: dict) -> dict:
    """
    Mock API function that simulates sending data to an external system
    """

    print("\n📡 [MOCK API CALL] Sending lead data to CRM system...")
    print("Payload:", payload)

    # Simulated API response
    return {
        "status": "success",
        "message": "Lead successfully submitted to CRM"
    }
