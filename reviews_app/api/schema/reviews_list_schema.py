REVIEWS_LIST_DESCRIPTION = """

**Description**: Listet alle verfügbaren Bewertungen auf. Die Bewertungen können nach 'updated_at' oder 'rating' geordnet werden. Es können auch Filter-Parameter wie 'business_user_id' und 'reviewer_id' verwendet werden.

###  Query Parameters

| Name | Type | Description |
|--------|--------|--------|
| business_user_id | integer | Die ID des Geschäftsbenutzers, für den Bewertungen gefiltert werden sollen.|
| reviewer_id | integer | Die ID des Benutzers, der die Bewertungen erstellt hat.|
| ordering | string | Die Sortierreihenfolge der Bewertungen. Mögliche Werte: 'updated_at' oder 'rating'.|


### Request Body

```json
{
  
}
```

### Success Response

Die Antwort enthält eine Liste aller Bewertungen, die gefiltert und geordnet werden können..

```json
[
  {
    "id": 1,
    "business_user": 2,
    "reviewer": 3,
    "rating": 4,
    "description": "Sehr professioneller Service.",
    "created_at": "2023-10-30T10:00:00Z",
    "updated_at": "2023-10-31T10:00:00Z"
  },
  {
    "id": 2,
    "business_user": 5,
    "reviewer": 3,
    "rating": 5,
    "description": "Top Qualität und schnelle Lieferung!",
    "created_at": "2023-09-20T10:00:00Z",
    "updated_at": "2023-09-20T12:00:00Z"
  }
]
```

### Status Codes

-   **200**: Erfolgreiche Antwort mit der Liste der Bewertungen.
-   **401**: Unauthorized. Der Benutzer muss authentifiziert sein
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Jeder authentifizierte Benutzer kann Bewertungen lesen.

### Extra Information:

- NO Extra Information


"""
