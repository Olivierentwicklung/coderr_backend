OFFER_DETAILS_RETRIEVE_DESCRIPTION = """

**Description**: Ruft die Details eines spezifischen Angebotsdetails ab.

###  URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| id | - | Die ID des Angebotsdetails, das abgerufen werden soll.|


### Request Body

```json
{
 
}
```

### Success Response

Gibt die vollständigen Details des Angebotsdetails zurück, einschließlich Titel, Preis, Lieferzeit, Features und Angebotstyp.

```json
{
  "id": 1,
  "title": "Basic Design",
  "revisions": 2,
  "delivery_time_in_days": 5,
  "price": 100,
  "features": [
    "Logo Design",
    "Visitenkarte"
  ],
  "offer_type": "basic"
}
```

### Status Codes

-   **200**: Das Angebotsdetail wurde erfolgreich abgerufen.
-   **401**: Benutzer ist nicht authentifiziert.
-   **404**: Das Angebotsdetail mit der angegebenen ID wurde nicht gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Der Benutzer muss authentifiziert sein.

### Extra Information:

- NO Extra Information.

"""
