OFFERS_PARTIAL_UPDATE_BY_ID_DESCRIPTION = """

**Description**: Aktualisiert ein spezifisches Angebot. Ein PATCH überschreibt nur die angegebenen Felder. Es müssen nicht alle Felder angegeben werden, nur die, die aktualisiert werden sollen.

###  URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| id | - | Die ID des zu aktualisierenden Angebots.|


### Request Body

```json
{
  "title": "Updated Grafikdesign-Paket",
  "details": [
    {
      "title": "Basic Design Updated",
      "revisions": 3,
      "delivery_time_in_days": 6,
      "price": 120,
      "features": [
        "Logo Design",
        "Flyer"
      ],
      "offer_type": "basic"
    }
  ]
}
```

### Success Response

Gibt das aktualisierte Angebot mit allen Feldern zurück, unabhängig davon, welche Felder in der Anfrage angegeben wurden.

```json
{
  "id": 66,
  "title": "Updated Grafikdesign-Paket",
  "image": null,
  "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
  "details": [
    {
      "id": 199,
      "title": "Basic Design Updated",
      "revisions": 3,
      "delivery_time_in_days": 6,
      "price": 120,
      "features": [
        "Logo Design",
        "Flyer"
      ],
      "offer_type": "basic"
    },
    {
      "id": 200,
      "title": "Standard Design",
      "revisions": 5,
      "delivery_time_in_days": 10,
      "price": 120,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier"
      ],
      "offer_type": "standard"
    },
    {
      "id": 201,
      "title": "Premium Design",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 150,
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

-   **200**: Das Angebot wurde erfolgreich aktualisiert.
-   **400**: Ungültige Anfragedaten oder unvollständige Details.
-   **401**: Benutzer ist nicht authentifiziert.
-   **403**: Authentifizierter Benutzer ist nicht der Eigentümer des Angebots
-   **404**: Das Angebot mit der angegebenen ID wurde nicht gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Nur Ersteller des Angebotes können dies verändern.

### Extra Information:

- Nur die angegebenen Felder werden aktualisiert. Alle nicht angegebenen Felder bleiben unverändert. Details können einzeln aktualisiert werden, wobei ihre IDs unverändert bleiben müssen. Desweiteren sollte der Typ (offer_type) immer mitgegeben werden, um das Detail eindeutig zu identifizieren.

"""
