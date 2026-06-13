ORDERS_CREATE_DESCRIPTION = """

**Description**: Erstellt eine neue Bestellung basierend auf den Details eines Angebots (OfferDetail).


### Request Body

```json
{
 "offer_detail_id": 1 
}
```

### Success Response

Die erstellte Bestellung wird zurückgegeben, einschließlich Details wie ID, Kunde, Geschäftspartner, Titel, Preis und Status.

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
  "status": "in_progress",
  "created_at": "2024-09-29T10:00:00Z",
  "updated_at": "2024-09-30T12:00:00Z"
}
```

### Status Codes

-   **201**: Die Bestellung wurde erfolgreich erstellt.
-   **400**: Ungültige Anfragedaten (z. B. wenn 'offer_detail_id' fehlt oder ungültig ist).
-   **401**: Benutzer ist nicht authentifiziert.
-   **403**: Benutzer hat keine Berechtigung, z.B. weil nicht vom typ 'customer'.
-   **404**: Das angegebene Angebotsdetail wurde nicht gefunden.
-   **500**: Interner Serverfehler.

### Rate Limits

- No limit.

### Permissions required: 

- Der Benutzer muss authentifiziert sein und vom typ 'customer' sein.

### Extra Information:

- Nur Benutzer vom typ 'customer' können Bestellungen erstellen. Der Benutzer gibt eine OfferDetail ID an, und die Bestellung wird auf Grundlage dieses Angebots erstellt. Beachte, dass das Angebot sowohl den Anbieter als auch den Kunden beinhalten muss. Diese Informationen können aus der Authentifizierung und der Offer entnommen werden.


"""
