ORDERS_DELETE_BY_ID_DESCRIPTION = """

**Description**: Löscht eine spezifische Bestellung. Diese Aktion ist auf Admin-Benutzer (Staff) beschränkt.

###  URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| id | - | Die eindeutige ID der zu löschenden Bestellung.|

### Request Body

```json
{

}
```

### Success Response

Die Antwort enthält keinen Inhalt und zeigt an, dass die Bestellung erfolgreich gelöscht wurde.

```json
null
```

### Status Codes

-   **204**: Die Bestellung wurde erfolgreich gelöscht. Keine weiteren Inhalte in der Antwort.
-   **401**: Benutzer ist nicht authentifiziert.
-   **403**: Benutzer hat keine Berechtigung, die Bestellung zu löschen.
-   **404**: Die angegebene Bestellung wurde nicht gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Nur Admin-Benutzer (Staff) dürfen Bestellungen löschen.

### Extra Information:

- NO Extra Information

"""
