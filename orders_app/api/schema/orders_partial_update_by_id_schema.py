ORDERS_PARTIAL_UPDATE_BY_ID_DESCRIPTION = """

**Description**: Aktualisiert den Status einer spezifischen Bestellung. Mögliche Statuswerte sind z.B. 'in_progress', 'completed', oder 'cancelled'.

###  URL Parameters

| Name | Type | Description |
|--------|--------|--------|
| id | - | Die eindeutige ID der Bestellung, die aktualisiert werden soll.|

### Request Body

```json
{
 "status": "completed"
}
```

### Success Response

Die aktualisierten Details der Bestellung werden zurückgegeben, einschließlich des neuen Status und aktualisierter Timestamps.

```json
{
  "id": 1,
  "customer_user": 1,
  "business_user": 2,
  "title": "Logo Design",
  "revisions": 3,
  "delivery_time_in_days": 5,
  "price": 150,
  "features": [
    "Logo Design",
    "Visitenkarten"
  ],
  "offer_type": "basic",
  "status": "completed",
  "created_at": "2024-09-29T10:00:00Z",
  "updated_at": "2024-09-30T15:00:00Z"
}
```

### Status Codes

-   **200**: Der Status der Bestellung wurde erfolgreich aktualisiert.
-   **400**: Ungültiger Status oder unzulässige Felder in der Anfrage.
-   **401**: Benutzer ist nicht authentifiziert.
-   **403**: Benutzer hat keine Berechtigung, diese Bestellung zu aktualisieren.
-   **404**: Die angegebene Bestellung wurde nicht gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Nur ein Benutzer vom typ 'business' kann den Status einer Bestellung aktualisieren.

### Extra Information:

- NO Extra Information

"""
