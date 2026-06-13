OFFERS_RETRIEVE_BY_ID_DESCRIPTION = """

**Description**: Dieser Endpunkt gibt die Details eines spezifischen Angebots anhand der angegebenen ID zurück.

###  URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| id | - | Die ID des gewünschten Angebots.|


### Request Body

```json
{

}
```

### Success Response

Gibt die Details eines spezifischen Angebots, Angebotsdetails und Metadaten zurück. 'user' ist hier die ID des User der dieses Angebot erstellt hat.

```json
{
  "id": 66,
  "user": 114,
  "title": "Grafikdesign-Paket",
  "image": null,
  "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
  "created_at": "2025-01-23T07:44:15.365773Z",
  "updated_at": "2025-01-23T07:44:15.365773Z",
  "details": [
    {
      "id": 199,
      "url": "http://127.0.0.1:8000/api/offerdetails/199/"
    },
    {
      "id": 200,
      "url": "http://127.0.0.1:8000/api/offerdetails/200/"
    },
    {
      "id": 201,
      "url": "http://127.0.0.1:8000/api/offerdetails/201/"
    }
  ],
  "min_price": 50,
  "min_delivery_time": 5
}
```

### Status Codes

-   **200**: Die Anfrage war erfolgreich, die Angebotsdetails wurden zurückgegeben.
-   **401**: Benutzer ist nicht authentifiziert.
-   **404**: Das Angebot mit der angegebenen ID wurde nicht gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Der Benutzer muss authentifiziert sein

### Extra Information:

- Die Angebotsdetails enthalten die URLs zu den einzelnen Angebotsdetail-Objekten.

"""
