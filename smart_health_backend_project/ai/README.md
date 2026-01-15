# AI endpoints

This document lists the AI endpoints exposed by the `ai` app (mounted at `/api/`).

- POST /api/v1/symptoms/checker/

  - Request body: { "symptoms": "..." }
  - Response: {"status":"success","message":"...","data":{"analysis":"..."}}

- POST /api/v1/medical/summary/

  - Request body: { "medical_history": "..." }
  - Response: {"status":"success","message":"Medical summary generated.","data":{"summary":"..."}}

- POST /api/v1/doctors/recommendation/
  - Request body: { "symptoms": "...", "location": "..." }
  - Response (if doctors found): {"status":"success","message":"Doctor recommendation generated.","data":{"recommendation":"..."}}
  - Response (if no doctors): status 404 with {"status":"error","message":"No verified doctors found in this location.","data":[]}

## Notes

- All AI endpoints require an authenticated user.
- The implementation uses an external AI service; in local/testing environments the call is mocked or returns a message when the GEMINI API key is not configured.
