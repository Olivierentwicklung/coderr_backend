REVIEWS_DELETE_BY_ID_DESCRIPTION = """

**Description**: Löscht eine spezifische Bewertung. Nur der Ersteller der Bewertung können diese Aktion ausführen.

###  URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| id | - | Die ID der spezifischen Bewertung, die gelöscht werden soll.|

### Request Body

```json
{

}
```

### Success Response

Die Antwort bestätigt, dass die Bewertung erfolgreich gelöscht wurde.

```json
null
```

### Status Codes

-   **204**: Erfolgreich gelöscht. Es wird kein Inhalt zurückgegeben.
-   **401**: Unauthorized. Der Benutzer muss authentifiziert sein.
-   **403**: Forbidden. Der Benutzer ist nicht berechtigt, diese Bewertung zu löschen.
-   **404**: Nicht gefunden. Es wurde keine Bewertung mit der angegebenen ID gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Nur der Ersteller der Bewertung darf diese Aktion durchführen.

### Extra Information:

- NO Extra Information

"""
