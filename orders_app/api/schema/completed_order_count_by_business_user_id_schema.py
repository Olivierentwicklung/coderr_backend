COMPLETED_ORDER_COUNT_BY_BUSINESS_USER_ID_DESCRIPTION = """

**Description**: Gibt die Anzahl der abgeschlossenen Bestellungen eines bestimmten Geschäftsnutzers zurück. Abgeschlossene Bestellungen haben den Status 'completed'.

###  URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| business_user_id | - | Die eindeutige ID des Geschäftsnutzers, dessen abgeschlossene Bestellungen gezählt werden sollen.|

### Request Body

```json
{

}
```

### Success Response

Die Antwort enthält die Anzahl der abgeschlossenen Bestellungen für den angegebenen Geschäftsnutzer.

```json
{
  "completed_order_count": 10
}
```

### Status Codes

-   **200**: Die Anzahl der abgeschlossenen Bestellungen wurde erfolgreich abgerufen.
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
