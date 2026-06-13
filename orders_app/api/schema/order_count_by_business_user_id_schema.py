ORDER_COUNT_BY_BUSINESS_USER_ID_DESCRIPTION = """

**Description**: Dieser Endpunkt gibt die Anzahl der laufenden Bestellungen eines bestimmten Geschäftsnutzers (Business User) zurück. Laufende Bestellungen sind solche mit dem Status 'in_progress'.

###  URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| business_user_id | - | Die eindeutige ID des Geschäftsnutzers, dessen laufende Bestellungen gezählt werden sollen.|

### Request Body

```json
{

}
```

### Success Response

Die Antwort enthält die Anzahl der laufenden Bestellungen für den angegebenen Geschäftsnutzer.

```json
{
  "order_count": 5
}
```

### Status Codes

-   **200**: Die Anzahl der laufenden Bestellungen wurde erfolgreich abgerufen.
-   **401**: Benutzer ist nicht authentifiziert.
-   **404**: Kein Geschäftsnutzer mit der angegebenen ID gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Der Benutzer muss authentifiziert sein.

### Extra Information:

- NO Extra Information

"""
