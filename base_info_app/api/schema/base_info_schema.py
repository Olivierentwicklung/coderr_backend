BASE_INFO_DESCRIPTION = """

**Description**: Ruft allgemeine Basisinformationen zur Plattform ab, einschließlich der Anzahl der Bewertungen, des durchschnittlichen Bewertungsergebnisses, der Anzahl der Geschäftsnutzer und der Anzahl der Angebote.


### Request Body

```json
{

}
```

### Success Response

Die Antwort enthält statistische Informationen über die Plattform.

```json
{
  "review_count": 10,
  "average_rating": 4.6,
  "business_profile_count": 45,
  "offer_count": 150
}
```

### Status Codes

-   **200**: Die Basisinformationen wurden erfolgreich abgerufen.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- No Permissions required

### Extra Information:

- Die durchschnittliche Bewertung ('average_rating') basiert auf allen abgegebenen Bewertungen und ist auf eine Dezimalstelle gerundet

"""
