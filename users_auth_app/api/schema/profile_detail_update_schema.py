from drf_spectacular.utils import OpenApiExample, OpenApiParameter

PROFILE_DETAIL_UPDATE_DESCRIPTION = """

**Description**: Ermöglicht es einem Benutzer, bestimmte Profilinformationen zu aktualisieren.

### URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| pk | - | Die ID des Benutzers, dessen Profil bearbeitet wird.|

### Request Body

```json
{
  "first_name": "Max",
  "last_name": "Mustermann",
  "location": "Berlin",
  "tel": "987654321",
  "description": "Updated business description",
  "working_hours": "10-18",
  "email": "new_email@business.de"
}
```

### Success Response

Die Antwort enthält das aktualisierte Profil des Benutzers. Die Felder first_name, last_name, location, tel, description und working_hours dürfen im Response nicht null sein, sondern müssen, falls keine Werte vorhanden sind, mit einem leeren String ('' '') belegt werden.

```json
{
  "user": 1,
  "username": "max_mustermann",
  "first_name": "Max",
  "last_name": "Mustermann",
  "file": "profile_picture.jpg",
  "location": "Berlin",
  "tel": "987654321",
  "description": "Updated business description",
  "working_hours": "10-18",
  "type": "business",
  "email": "new_email@business.de",
  "created_at": "2023-01-01T12:00:00Z"
}
```

### Status Codes

-   **200**: Das Profil wurde erfolgreich aktualisiert.
-   **401**: Benutzer ist nicht authentifiziert
-   **403**: Authentifizierter Benutzer ist nicht der Eigentümer Profils
-   **404**: Das Benutzerprofil wurde nicht gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Der Benutzer kann NUR sein eigenes Profil bearbeiten.

### Extra Information:

-   No Extra Information

"""

PROFILE_DETAIL_UPDATE_PARAMETERS = [
    OpenApiParameter(
        name="pk",
        type=int,
        location=OpenApiParameter.PATH,
        description="User ID",
    )
]
PROFILE_DETAIL_UPDATE_EXAMPLES = [
    OpenApiExample(
        "Customer Profile Update",
        value={
            "first_name": "Max",
            "last_name": "Mustermann",
            "file": None,
            "location": "Berlin",
            "tel": "123456789",
            "description": "Neue Beschreibung",
            "working_hours": "9-17",
            "email": "new_email@business.de",
        },
        request_only=True,
    ),
]
