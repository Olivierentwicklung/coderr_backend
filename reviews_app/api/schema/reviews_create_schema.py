REVIEWS_CREATE_DESCRIPTION = """

**Description**: Erstellt eine neue Bewertung für einen Geschäftsbenutzer. Nur authentifizierte Benutzer mit einem Kundenprofil dürfen Bewertungen erstellen. Ein Benutzer kann pro Geschäftsprofil nur eine Bewertung abgeben.


### Request Body

```json
{
  "business_user": 2,
  "rating": 4,
  "description": "Alles war toll!"
}
```

### Success Response

Erfolgreiche Antwort, die die Details der neu erstellten Bewertung zurückgibt.

```json
{
  "id": 3,
  "business_user": 2,
  "reviewer": 3,
  "rating": 4,
  "description": "Alles war toll!",
  "created_at": "2023-10-30T15:30:00Z",
  "updated_at": "2023-10-30T15:30:00Z"
}
```

### Status Codes

-   **201**: Erfolgreich erstellt.
-   **400**: Fehlerhafte Anfrage. Der Benutzer hat möglicherweise bereits eine Bewertung für das gleiche Geschäftsprofil abgegeben.
-   **401**: Unauthorized. Der Benutzer muss authentifiziert sein und ein Kundenprofil besitzen.
-   **403**: Forbidden. Ein Benutzer kann nur eine Bewertung pro Geschäftsprofil abgeben.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Nur authentifizierte Benutzer mit einem Kundenprofil dürfen Bewertungen erstellen. Jeder authentifizierte Benutzer kann Bewertungen lesen.

### Extra Information:

- Dieser Endpunkt erlaubt es Kunden, eine Bewertung für einen Geschäftsbenutzer zu hinterlassen. Eine Bewertung kann nur einmal pro Geschäftsbenutzer abgegeben werden.


"""
