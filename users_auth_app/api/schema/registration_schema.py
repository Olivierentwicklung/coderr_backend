from drf_spectacular.utils import OpenApiExample

REGISTRATION_DESCRIPTION = """

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

-   **201**: Der Benutzer wurde erfolgreich erstellt.
-   **400**: Ungültige Anfragedaten.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- No Permissions required

### Extra Information:

-   No Extra Information

"""

REGISTRATION_EXAMPLES = [
    OpenApiExample(
        "Customer Registration",
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
        "Business Registration",
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
            "username": "customer1234",
            "password": "SecurePassword123!",
            "repeated_password": "SecurePassword123!",
            "type": "customer",
        },
        request_only=True,
    ),
    OpenApiExample(
        "Passwörter stimmen nicht überein",
        value={
            "username": "customer1234",
            "email": "customer1234@example.com",
            "password": "Password123!",
            "repeated_password": "DifferentPassword123!",
            "type": "customer",
        },
        request_only=True,
    ),
]
