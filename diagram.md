erDiagram
    PARTNERS ||--o{ ORDERS : creates
    MANUFACTURERS ||--o{ PRODUCTS : produces
    PRODUCT_TYPES ||--o{ PRODUCTS : classifies
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : included_in
    
    PARTNERS {
        int id PK
        string name
        string contact_person
        string phone
        string email
        string address
        timestamp created_date
    }
    
    MANUFACTURERS {
        int id PK
        string name UK
        string country
        string website
        string contact_info
    }
    
    PRODUCT_TYPES {
        int id PK
        string name UK
        string description
    }
    
    PRODUCTS {
        int id PK
        string name
        string article UK
        decimal price
        int shelf_life_days
        int stock_quantity
        string description
        int manufacturer_id FK
        int type_id FK
    }
    
    ORDERS {
        int id PK
        string order_number UK
        timestamp order_date
        date required_date
        string status
        decimal total_amount
        string notes
        int partner_id FK
    }
    
    ORDER_ITEMS {
        int id PK
        int quantity
        decimal price_per_unit
        decimal total_price
        date expiry_date
        int order_id FK
        int product_id FK
    }