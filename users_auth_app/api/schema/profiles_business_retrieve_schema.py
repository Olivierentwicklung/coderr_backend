PROFILE_BUSINESS_RETRIEVE_DESCRIPTION = """

**Description**: Gibt eine Liste aller Geschäftsnutzer auf der Plattform zurück.


### Request Body

```json
{

}
```

### Success Response

Die Antwort enthält eine Liste aller Geschäftsnutzer mit ihren Profilinformationen. Die Felder first_name, last_name, location, tel, description und working_hours dürfen im Response nicht null sein, sondern müssen, falls keine Werte vorhanden sind, mit einem leeren String ('' '') belegt werden.

```json
[
  {
    "user": 1,
    "username": "max_business",
    "first_name": "Max",
    "last_name": "Mustermann",
    "file": "profile_picture.jpg",
    "location": "Berlin",
    "tel": "123456789",
    "description": "Business description",
    "working_hours": "9-17",
    "type": "business"
  }
]
```

### Status Codes

-   **200**: Erfolgreiche Antwort mit der Liste der Geschäftsnutzer.
-   **401**: Benutzer ist nicht authentifiziert
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Der Benutzer muss authentifiziert sein.

### Extra Information:

-   No Extra Information

"""
