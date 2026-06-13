OFFERS_CREATE_DESCRIPTION = """

**Description**: Dieser Endpunkt ermöglicht es, ein neues Angebot (Offer) zu erstellen. Ein Offer muss 3 Details enthalten!

### Request Body

```json
{
  "title": "Grafikdesign-Paket",
  "image": null,
  "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
  "details": [
    {
      "title": "Basic Design",
      "revisions": 2,
      "delivery_time_in_days": 5,
      "price": 100,
      "features": [
        "Logo Design",
        "Visitenkarte"
      ],
      "offer_type": "basic"
    },
    {
      "title": "Standard Design",
      "revisions": 5,
      "delivery_time_in_days": 7,
      "price": 200,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier"
      ],
      "offer_type": "standard"
    },
    {
      "title": "Premium Design",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 500,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier",
        "Flyer"
      ],
      "offer_type": "premium"
    }
  ]
}
```

### Success Response

Bei erfolgreicher Erstellung wird das Angebot mit den zugehörigen Details zurückgegeben, einschließlich IDs für das Angebot und jedes Detail.

```json
{
  "id": 1,
  "title": "Grafikdesign-Paket",
  "image": null,
  "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
  "details": [
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
    },
    {
      "id": 2,
      "title": "Standard Design",
      "revisions": 5,
      "delivery_time_in_days": 7,
      "price": 200,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier"
      ],
      "offer_type": "standard"
    },
    {
      "id": 3,
      "title": "Premium Design",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 500,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier",
        "Flyer"
      ],
      "offer_type": "premium"
    }
  ]
}
```

### Status Codes

-   **201**: Das Angebot wurde erfolgreich erstellt.
-   **400**: Ungültige Anfragedaten oder unvollständige Details.
-   **401**: Benutzer ist nicht authentifiziert.
-   **403**: Authentifizierter Benutzer ist kein 'business' Profil.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Nur User vom type 'business' dürfen Angebote erstellen

### Extra Information:

- No Extra Information

"""
