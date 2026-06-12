PROFILE_CUSTOMER_RETRIEVE_DESCRIPTION = """

**Description**: Gibt eine Liste aller Kundenprofile auf der Plattform zurück.


### Request Body

```json
{

}
```

### Success Response

Die Antwort enthält eine Liste aller Kunden mit ihren Profilinformationen. Die Felder first_name, last_name, location, tel, description und working_hours dürfen im Response nicht null sein, sondern müssen, falls keine Werte vorhanden sind, mit einem leeren String ('' '') belegt werden.

```json
[
  {
    "user": 2,
    "username": "customer_jane",
    "first_name": "Jane",
    "last_name": "Doe",
    "file": "profile_picture_customer.jpg",
    "uploaded_at": "2023-09-15T09:00:00",
    "type": "customer"
  }
]
```

### Status Codes

-   **200**: Erfolgreiche Antwort mit der Liste der Kundenprofile.
-   **401**: Benutzer ist nicht authentifiziert
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Der Benutzer muss authentifiziert sein.

### Extra Information:

-   No Extra Information

"""
