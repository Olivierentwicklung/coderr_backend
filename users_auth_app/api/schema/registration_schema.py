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
