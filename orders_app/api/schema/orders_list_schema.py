ORDERS_LIST_DESCRIPTION = """

**Description**: Gibt eine Liste der Bestellungen zurück, die entweder vom angemeldeten Benutzer als Kunde oder als Geschäftspartner erstellt wurden.


### Request Body

```json
{
  
}
```

### Success Response

Eine Liste von Bestellungen, einschließlich Details wie Kunde, Geschäftspartner, Titel, Status und Erstellungsdatum.

```json
[
  {
    "id": 1,
    "customer_user": 1,
    "business_user": 2,
    "title": "Logo Design",
    "revisions": 3,
    "delivery_time_in_days": 5,
    "price": 150,
    "features": [
      "Logo Design",
      "Visitenkarten"
    ],
    "offer_type": "basic",
    "status": "in_progress",
    "created_at": "2024-09-29T10:00:00Z",
    "updated_at": "2024-09-30T12:00:00Z"
  }
]
```

### Status Codes

-   **200**: Die Liste der Bestellungen wurde erfolgreich abgerufen.
-   **401**: Benutzer ist nicht authentifiziert.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Der Benutzer muss authentifiziert sein.

### Extra Information:

- Dieser Endpunkt gibt nur Bestellungen zurück, die mit dem angemeldeten Benutzer entweder als Kunde oder als Geschäftspartner verbunden sind.


"""
