REVIEWS_PARTIAL_UPDATE_BY_ID_DESCRIPTION = """

**Description**: Aktualisiert ausgewählte Felder einer bestehenden Bewertung (nur 'rating' und 'description' sind editierbar). Der Endpunkt erlaubt es dem Ersteller der Bewertung, die Bewertung zu bearbeiten.

###  URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| id | - | Die ID der spezifischen Bewertung, die aktualisiert werden soll.|


### Request Body

```json
{
  "rating": 5,
  "description": "Noch besser als erwartet!"
}
```

### Success Response

Die Antwort enthält die aktualisierten Details der Bewertung.

```json
{
  "id": 1,
  "business_user": 2,
  "reviewer": 3,
  "rating": 5,
  "description": "Noch besser als erwartet!",
  "created_at": "2023-10-30T10:00:00Z",
  "updated_at": "2023-11-01T08:00:00Z"
}
```

### Status Codes

-   **200**: Erfolgreich aktualisiert. Die aktualisierte Bewertung wird zurückgegeben.
-   **400**: Bad Request. Der Anfrage-Body enthält ungültige Daten.
-   **401**: Unauthorized. Der Benutzer muss authentifiziert sein.
-   **403**: Forbidden. Der Benutzer ist nicht berechtigt, diese Bewertung zu bearbeiten.
-   **404**: Nicht gefunden. Es wurde keine Bewertung mit der angegebenen ID gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Nur der Ersteller der Bewertung darf diese Aktion durchführen.

### Extra Information:

- NO Extra Information


"""
