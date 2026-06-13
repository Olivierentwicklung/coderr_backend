OFFERS_RETRIEVE_DESCRIPTION = """

**Description**: Dieser Endpunkt gibt eine Liste von Angeboten zurück. Jedes Angebot enthält eine Übersicht der Angebotsdetails, den minimalen Preis und die kürzeste Lieferzeit.

###  Query Parameters

| Name | Type | Description |
|--------|--------|--------|
| creator_id | integer | Filtert die Angebote nach dem Benutzer, der sie erstellt hat.|
| min_price | float | Filtert Angebote mit einem Mindestpreis.|
| max_delivery_time | integer | Filtert Angebote, deren Lieferzeit kürzer oder gleich dem angegebenen Wert ist.|
| ordering | string | Sortiert die Angebote nach den Feldern 'updated_at' oder 'min_price'.|
| search | string | Durchsucht die Felder 'title' und 'description' nach Übereinstimmungen.|
| page_size | integer | Gibt an, wie viele Ergebnisse pro Seite zurückgegeben werden sollen. Dies sollte mit dem Frontend abgestimmt sein.|

### Request Body

```json
{
  
}
```

### Success Response

Die Antwort ist eine paginierte Liste von Angeboten mit den zugehörigen Details.

```json
{
  "count": 1,
  "next": "http://127.0.0.1:8000/api/offers/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "title": "Website Design",
      "image": null,
      "description": "Professionelles Website-Design...",
      "created_at": "2024-09-25T10:00:00Z",
      "updated_at": "2024-09-28T12:00:00Z",
      "details": [
        {
          "id": 1,
          "url": "/offerdetails/1/"
        },
        {
          "id": 2,
          "url": "/offerdetails/2/"
        },
        {
          "id": 3,
          "url": "/offerdetails/3/"
        }
      ],
      "min_price": 100,
      "min_delivery_time": 7,
      "user_details": {
        "first_name": "John",
        "last_name": "Doe",
        "username": "jdoe"
      }
    }
  ]
}
```

### Status Codes

-   **200**: Die Anfrage war erfolgreich und eine Liste von Angeboten wurde zurückgegeben.
-   **400**: Ungültige Anfrageparameter.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- No Permissions required

### Extra Information:

- Die Antwort verwendet PageNumberPagination

"""
