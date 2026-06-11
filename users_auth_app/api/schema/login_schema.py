from drf_spectacular.utils import OpenApiExample

LOGIN_DESCRIPTION = """

**Description**: Authentifiziert einen Benutzer und liefert ein Authentifizierungs-Token zurück, das für weitere API-Anfragen genutzt wird.

### Request Body

```json
{
  "username": "exampleUsername",
  "password": "examplePassword"
}
```

### Success Response

Erfolgreiche Authentifizierung gibt ein Token sowie Benutzerinformationen zurück.

```json
{
  "token": "83bf098723b08f7b23429u0fv8274",
  "username": "exampleUsername",
  "email": "example@mail.de",
  "user_id": 123
}
```

### Status Codes

-   **200**: Erfolgreiche Anmeldung.
-   **400**: Ungültige Anfragedaten.
-   **500**: Interner Serverfehler.

### Rate Limit

- No limit.

### Permissions required: 

- No Permissions required

### Extra Information:

-   No Extra Information

"""

LOGIN_EXAMPLES = [
    OpenApiExample(
        "Customer Login",
        value={
            "username": "customer123",
            "password": "SecurePassword123!",
        },
        request_only=True,
    ),
    OpenApiExample(
        "Business Login",
        value={
            "username": "business123",
            "password": "SecurePassword123!",
        },
        request_only=True,
    ),
    OpenApiExample(
        "Nicht Erfolgreiche Anmeldung",
        value={
            "username": "business123",
            "password": "SecurePassword123!!",
        },
        request_only=True,
    ),
]
