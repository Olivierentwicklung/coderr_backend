OFFERS_DELETE_BY_ID_DESCRIPTION = """

**Description**: Löscht ein spezifisches Angebot anhand der angegebenen ID.

###  URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| id | - | Die ID des zu löschenden Angebots.|


### Request Body

```json
{
 
}
```

### Success Response

Bei Erfolg wird ein HTTP-Statuscode 204 No Content zurückgegeben, ohne Inhalt in der Antwort.

```json
null
```

### Status Codes

-   **204**: Das Angebot wurde erfolgreich gelöscht.
-   **401**: Benutzer ist nicht authentifiziert.
-   **403**: Authentifizierter Benutzer ist nicht der Eigentümer des Angebots
-   **404**: Das Angebot mit der angegebenen ID wurde nicht gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Nur Ersteller des Angebotes können dies löschen.

### Extra Information:

- Dieser Endpunkt gibt im Erfolgsfall keinen Antwortinhalt zurück, sondern nur den HTTP-Statuscode 204.

"""
