from drf_spectacular.utils import OpenApiExample

AUTH_TAG = ["Authentication"]

REGISTRATION_DESCRIPTION = """
## Registrierung

**Description**: Erstellt einen neuen Benutzer. Dieser Benutzer kann entweder ein **Customer**- oder **Business**-User sein.

### Request Body

```json
{
  "username": "exampleUsername",
  "email": "example@mail.de",
  "password": "examplePassword",
  "repeated_password": "examplePassword",
  "type": "customer"
}
```

| Feld | Typ | Pflicht | Beschreibung |
|--------|--------|--------|--------|
| username | string | ✅ | Eindeutiger Benutzername |
| email | string | ✅ | E-Mail-Adresse |
| password | string | ✅ | Passwort |
| repeated_password | string | ✅ | Passwort-Bestätigung |
| type | string | ✅ | customer oder business |

### Success Response

Erfolgreicher Erstellung gibt dies ein Token sowie die Benutzerinformationen zurück, inklusive die einzigartige Nutzer-ID.

```json
{
  "token": "83bf098723b08f7b23429u0fv8274",
  "username": "exampleUsername",
  "email": "example@mail.de",
  "user_id": 123
}
```

### Status Codes

| Code | Beschreibung |
|--------|--------|
| 201 | Benutzer erfolgreich erstellt |
| 400 | Ungültige Eingabedaten |
| 500 | Interner Serverfehler |

### Berechtigung

Für diesen Endpunkt sind keine Berechtigungen erforderlich.

### Rate Limit

Kein Rate Limit.
"""

REGISTRATION_EXAMPLES = [
    OpenApiExample(
        "Customer Registrierung",
        value={
            "username": "customer123",
            "email": "customer@example.com",
            "password": "SecurePassword123!",
            "repeated_password": "SecurePassword123!",
            "type": "customer",
        },
        request_only=True,
    ),
    OpenApiExample(
        "Business Registrierung",
        value={
            "username": "business123",
            "email": "business@example.com",
            "password": "SecurePassword123!",
            "repeated_password": "SecurePassword123!",
            "type": "business",
        },
        request_only=True,
    ),
    OpenApiExample(
        "Fehlende E-Mail",
        value={
            "username": "customer123",
            "password": "SecurePassword123!",
            "repeated_password": "SecurePassword123!",
            "type": "customer",
        },
        request_only=True,
    ),
    OpenApiExample(
        "Passwörter stimmen nicht überein",
        value={
            "username": "customer123",
            "email": "customer@example.com",
            "password": "Password123!",
            "repeated_password": "DifferentPassword123!",
            "type": "customer",
        },
        request_only=True,
    ),
]
