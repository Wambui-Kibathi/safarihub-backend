# SafariHub Backend - Entity Relationship Diagram

```mermaid
erDiagram
    USER {
        int id PK
        string email UK
        string password_hash
        string first_name
        string last_name
        string phone
        enum role "traveler, guide, admin"
        datetime created_at
        datetime updated_at
        boolean is_active
    }
    
    DESTINATION {
        int id PK
        string name
        text description
        string location
        decimal price_per_person
        int max_capacity
        string image_url
        int guide_id FK
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    BOOKING {
        int id PK
        int traveler_id FK
        int destination_id FK
        int number_of_people
        decimal total_amount
        enum status "pending, confirmed, cancelled, completed"
        date booking_date
        date travel_date
        datetime created_at
        datetime updated_at
    }
    
    PAYMENT {
        int id PK
        int booking_id FK
        decimal amount
        enum payment_method "mpesa, stripe, cash"
        string transaction_id
        enum status "pending, completed, failed, refunded"
        datetime created_at
        datetime updated_at
    }
    
    REVIEW {
        int id PK
        int traveler_id FK
        int destination_id FK
        int booking_id FK
        int rating
        text comment
        datetime created_at
    }
    
    USER ||--o{ DESTINATION : "guides create"
    USER ||--o{ BOOKING : "travelers book"
    DESTINATION ||--o{ BOOKING : "has bookings"
    BOOKING ||--|| PAYMENT : "has payment"
    USER ||--o{ REVIEW : "travelers review"
    DESTINATION ||--o{ REVIEW : "receives reviews"
    BOOKING ||--o| REVIEW : "can be reviewed"
```

## Relationships Explained:

1. **USER to DESTINATION (1:Many)**
   - Guides (users with role='guide') can create multiple destinations
   - Each destination belongs to one guide

2. **USER to BOOKING (1:Many)**
   - Travelers (users with role='traveler') can make multiple bookings
   - Each booking belongs to one traveler

3. **DESTINATION to BOOKING (1:Many)**
   - Each destination can have multiple bookings
   - Each booking is for one destination

4. **BOOKING to PAYMENT (1:1)**
   - Each booking has exactly one payment record
   - Each payment belongs to one booking

5. **USER to REVIEW (1:Many)**
   - Travelers can write multiple reviews
   - Each review is written by one traveler

6. **DESTINATION to REVIEW (1:Many)**
   - Each destination can have multiple reviews
   - Each review is for one destination

7. **BOOKING to REVIEW (1:0..1)**
   - Each booking can optionally have one review
   - Each review is based on one booking

## Key Features:
- **Multi-role system**: Users can be travelers, guides, or admins
- **Booking management**: Track booking status and travel dates
- **Payment integration**: Support for M-Pesa, Stripe, and cash payments
- **Review system**: Travelers can rate and review destinations
- **Guide management**: Guides manage their own destinations