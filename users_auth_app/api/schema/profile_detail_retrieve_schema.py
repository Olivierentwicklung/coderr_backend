from drf_spectacular.utils import OpenApiExample, OpenApiParameter

PROFILE_DETAIL_RETRIEVE_DESCRIPTION = """

**Description**: Ruft die detaillierten Informationen eines Benutzerprofils ab (sowohl für Kunden- als auch für Geschäftsnutzer). Ermöglicht auch das Bearbeiten der Profildaten (PATCH).

### URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| pk | - | Die ID des Benutzers, dessen Profil abgerufen oder bearbeitet wird.|

### Request Body

```json
{
  
}
```

### Success Response

Die Antwort enthält die vollständigen Profildaten eines spezifischen Benutzers. Die Felder first_name, last_name, location, tel, description und working_hours dürfen im Response nicht null sein, sondern müssen, falls keine Werte vorhanden sind, mit einem leeren String ('' '') belegt werden.

```json
{
  "user": 1,
  "username": "max_mustermann",
  "first_name": "Max",
  "last_name": "Mustermann",
  "file": "profile_picture.jpg",
  "location": "Berlin",
  "tel": "123456789",
  "description": "Business description",
  "working_hours": "9-17",
  "type": "business",
  "email": "max@business.de",
  "created_at": "2023-01-01T12:00:00Z"
}
```

### Status Codes

-   **200**: Die Profildaten wurden erfolgreich abgerufen.
-   **401**: Benutzer ist nicht authentifiziert.
-   **404**: Das Benutzerprofil wurde nicht gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Der Benutzer muss authentifiziert sein.

### Extra Information:

-   No Extra Information

"""

PROFILE_DETAIL_RETRIEVE_PARAMETERS = [
    OpenApiParameter(
        name="pk",
        type=int,
        location=OpenApiParameter.PATH,
        description="User ID",
    )
]
PROFILE_DETAIL_RETRIEVE_EXAMPLES = [
    OpenApiExample(
        "Existing User",
        value={
            "id": 3,
            "username": "customer123",
            "email": "customer@example.com",
        },
        response_only=True,
        status_codes=["200"],
    ),
]
