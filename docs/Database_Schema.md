## 1. Overview

This document describes the database design and schema used in **MediTrack – Smart Medicine Inventory & Expiry Management System**.

The system uses a relational database to manage:

* Medicine inventory
* Medicine categories
* Suppliers
* Stock details
* Expiry tracking
* User management
* Notifications
* Sales/usage records
* Reports

The database is designed to maintain data consistency, avoid duplication, and support efficient medicine tracking.

---

# 2. Database Technology

| Component            | Technology                              |
| -------------------- | --------------------------------------- |
| Database             | MySQL                                   |
| Backend Integration  | Python                                  |
| ORM / Query Handling | SQL Queries / Python Database Connector |
| Data Format          | Relational Tables                       |

---

# 3. Entity Relationship Overview

Main entities:

```
Users
  |
  |
Medicine Categories
  |
  |
Medicines
  |
  |
Inventory
  |
  |
Expiry Alerts


Suppliers
  |
  |
Medicines


Users
  |
  |
Transactions
```

---

# 4. Database Tables

## 4.1 Users Table

Stores application users and authentication details.

### Table Name

```
users
```

### Schema

| Column        | Data Type    | Constraint                | Description            |
| ------------- | ------------ | ------------------------- | ---------------------- |
| user_id       | INT          | PRIMARY KEY               | Unique user identifier |
| username      | VARCHAR(100) | NOT NULL                  | User name              |
| email         | VARCHAR(150) | UNIQUE                    | User email             |
| password_hash | VARCHAR(255) | NOT NULL                  | Encrypted password     |
| role          | VARCHAR(50)  | DEFAULT 'user'            | User role              |
| created_at    | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP | Account creation time  |

---

## 4.2 Medicine Categories Table

Stores medicine classification details.

### Table Name

```
medicine_categories
```

### Schema

| Column        | Data Type    | Constraint  | Description          |
| ------------- | ------------ | ----------- | -------------------- |
| category_id   | INT          | PRIMARY KEY | Category ID          |
| category_name | VARCHAR(100) | UNIQUE      | Category name        |
| description   | TEXT         | NULL        | Category description |

---

## 4.3 Suppliers Table

Stores supplier information.

### Table Name

```
suppliers
```

### Schema

| Column         | Data Type    | Constraint  | Description         |
| -------------- | ------------ | ----------- | ------------------- |
| supplier_id    | INT          | PRIMARY KEY | Supplier ID         |
| supplier_name  | VARCHAR(150) | NOT NULL    | Company/person name |
| contact_number | VARCHAR(15)  | NOT NULL    | Supplier phone      |
| email          | VARCHAR(150) | NULL        | Supplier email      |
| address        | TEXT         | NULL        | Supplier address    |

---

# 4.4 Medicines Table

Stores basic medicine information.

### Table Name

```
medicines
```

### Schema

| Column        | Data Type     | Constraint                | Description        |
| ------------- | ------------- | ------------------------- | ------------------ |
| medicine_id   | INT           | PRIMARY KEY               | Medicine ID        |
| category_id   | INT           | FOREIGN KEY               | Medicine category  |
| supplier_id   | INT           | FOREIGN KEY               | Supplier reference |
| medicine_name | VARCHAR(150)  | NOT NULL                  | Medicine name      |
| manufacturer  | VARCHAR(150)  | NULL                      | Manufacturer name  |
| batch_number  | VARCHAR(100)  | UNIQUE                    | Batch number       |
| price         | DECIMAL(10,2) | NOT NULL                  | Medicine price     |
| created_at    | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP | Added date         |

---

# 4.5 Inventory Table

Maintains current medicine stock.

### Table Name

```
inventory
```

### Schema

| Column           | Data Type    | Constraint  | Description        |
| ---------------- | ------------ | ----------- | ------------------ |
| inventory_id     | INT          | PRIMARY KEY | Inventory ID       |
| medicine_id      | INT          | FOREIGN KEY | Medicine reference |
| quantity         | INT          | NOT NULL    | Available quantity |
| purchase_date    | DATE         | NULL        | Purchase date      |
| expiry_date      | DATE         | NOT NULL    | Expiry date        |
| storage_location | VARCHAR(100) | NULL        | Storage location   |
| updated_at       | TIMESTAMP    | AUTO UPDATE | Last update time   |

---

# 4.6 Expiry Alerts Table

Stores expiry notification records.

### Table Name

```
expiry_alerts
```

### Schema

| Column       | Data Type   | Constraint                | Description        |
| ------------ | ----------- | ------------------------- | ------------------ |
| alert_id     | INT         | PRIMARY KEY               | Alert ID           |
| medicine_id  | INT         | FOREIGN KEY               | Medicine reference |
| expiry_date  | DATE        | NOT NULL                  | Expiry date        |
| alert_status | VARCHAR(50) | DEFAULT 'Pending'         | Alert state        |
| created_at   | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP | Alert creation     |

---

# 4.7 Transactions Table

Tracks medicine stock movement.

### Table Name

```
transactions
```

### Schema

| Column           | Data Type   | Constraint                | Description               |
| ---------------- | ----------- | ------------------------- | ------------------------- |
| transaction_id   | INT         | PRIMARY KEY               | Transaction ID            |
| medicine_id      | INT         | FOREIGN KEY               | Medicine reference        |
| user_id          | INT         | FOREIGN KEY               | User who performed action |
| transaction_type | VARCHAR(50) | NOT NULL                  | IN / OUT                  |
| quantity         | INT         | NOT NULL                  | Quantity changed          |
| transaction_date | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP | Transaction time          |

---

# 5. Relationships Between Tables

## Users → Transactions

One user can create many transactions.

Relationship:

```
users (1) -------- (many) transactions
```

---

## Categories → Medicines

One category can contain multiple medicines.

Relationship:

```
medicine_categories (1)
              |
              |
              *
          medicines
```

---

## Suppliers → Medicines

One supplier can provide multiple medicines.

Relationship:

```
suppliers (1)
      |
      |
      *
 medicines
```

---

## Medicines → Inventory

Each medicine can have inventory details.

Relationship:

```
medicines (1)
       |
       |
       *
 inventory
```

---

# 6. SQL Table Creation Example

```sql
CREATE TABLE medicine_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);


CREATE TABLE medicines (
    medicine_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    supplier_id INT,
    medicine_name VARCHAR(150) NOT NULL,
    manufacturer VARCHAR(150),
    batch_number VARCHAR(100) UNIQUE,
    price DECIMAL(10,2),

    FOREIGN KEY(category_id)
    REFERENCES medicine_categories(category_id)
);
```

---

# 7. Database Optimization

The following optimizations are applied:

* Primary keys for unique identification
* Foreign keys for data integrity
* Indexing on frequently searched fields
* Unique constraints to avoid duplicate records
* Timestamp tracking for auditing

---

# 8. Future Database Enhancements

Possible improvements:

* Barcode scanning support
* Multiple pharmacy branch management
* AI-based demand prediction
* Automated supplier ordering
* Cloud database migration
* Advanced analytics dashboard

---

## Conclusion

The MediTrack database schema provides a structured foundation for managing medicine inventory, expiry monitoring, suppliers, and stock transactions efficiently.
