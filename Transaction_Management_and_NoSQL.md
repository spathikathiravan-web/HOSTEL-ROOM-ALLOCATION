# Transaction Management and NoSQL Evaluation
## Hostel Room Allocation and Student Accommodation Analysis System

**Course Code:** 25ITT31 – Database Management Systems (Units 4 & 5: Transaction Management & NoSQL Databases)  
**Deliverable Category:** 2. Database Management System  

---

### Table of Contents
1. [ACID Properties in Hostel Operations](#1-acid-properties-in-hostel-operations)
2. [Concurrency Control and Two-Phase Locking (2PL)](#2-concurrency-control-and-two-phase-locking-2pl)
3. [Deadlock Detection and Prevention](#3-deadlock-detection-and-prevention)
4. [NoSQL Paradigms: BASE vs. ACID & CAP Theorem](#4-nosql-paradigms-base-vs-acid--cap-theorem)
5. [Document-Oriented Representation (MongoDB BSON/JSON)](#5-document-oriented-representation-mongodb-bsonjson)

---

### 1. ACID Properties in Hostel Operations

In the Hostel Management System, room booking and fee recording are transactional operations that must satisfy ACID guarantees:

1. **Atomicity (All-or-Nothing):**
   - *Scenario:* Room allocation requires (a) inserting an allocation record into `ALLOCATION`, and (b) incrementing `ROOM.occupancy` by 1.
   - If the system crashes after step (a) but before step (b), the database rolls back to the initial state, ensuring an allocated bed is never left uncounted in the room's occupancy.
2. **Consistency (Preserving Invariants):**
   - The system invariant $occupancy \le capacity$ must hold before and after every transaction. An allocation that would violate this invariant is rejected and aborted.
3. **Isolation (Concurrent Independence):**
   - When two administrators concurrently attempt to allocate the final available bed in room `A-101`, the isolation mechanism guarantees that only one transaction succeeds, while the second is informed that the room is full.
4. **Durability (Committed Persistence):**
   - Once a student's fee payment is committed, the transaction log is flushed to non-volatile disk storage, ensuring the payment voucher survives any subsequent power outage or system reboot.

---

### 2. Concurrency Control and Two-Phase Locking (2PL)

To guarantee **conflict serializability**, the system uses strict Two-Phase Locking (Strict 2PL):
1. **Growing Phase:**
   - Transaction acquires a Shared Lock ($S$) to read room occupancy:
     $$\text{LOCK-S}(ROOM_{room\_id})$$
   - Once capacity availability is verified ($occupancy < capacity$), the transaction upgrades to an Exclusive Lock ($X$):
     $$\text{LOCK-X}(ROOM_{room\_id}), \quad \text{LOCK-X}(ALLOCATION)$$
2. **Shrinking Phase:**
   - Under Strict 2PL, all exclusive locks are retained until the transaction explicitly executes `COMMIT` or `ROLLBACK`, eliminating cascading rollbacks (cascadeless schedules).

---

### 3. Deadlock Detection and Prevention

- **Wait-For Graph (WFG):** The DBMS maintains a directed graph $G = (V, E)$, where vertices $V$ represent active transactions and edges $E$ represent lock wait states ($T_1 \rightarrow T_2$ implies $T_1$ waits for a lock held by $T_2$).
- **Deadlock Handling:** If a cycle is detected in the WFG, the deadlock detector terminates and rolls back the younger transaction (victim selection based on lowest CPU cost or fewest modifications), releasing locks to unblock the cycle.

---

### 4. NoSQL Paradigms: BASE vs. ACID & CAP Theorem

#### 4.1 The CAP Theorem
According to Brewer's CAP Theorem, a distributed data system can satisfy at most two of the following three guarantees simultaneously:
- **Consistency (C):** Every read receives the most recent write or an error.
- **Availability (A):** Every non-failing node returns a non-error response.
- **Partition Tolerance (P):** The system continues to operate despite arbitrary network message loss.

- **RDBMS Selection (CA/CP):** Traditional MySQL / SQLite prioritizes **Consistency** and **Integrity** over extreme horizontal scaling, making it ideal for financial fee accounting and capacity enforcement where over-booking is unacceptable.
- **NoSQL Alternative (AP / BASE):** Systems using **Basically Available, Soft-state, Eventual consistency (BASE)** can be employed for distributed student access logs or telemetry.

#### 4.2 Comparison Matrix
| Feature | Relational DBMS (MySQL/SQLite) | Document NoSQL (MongoDB) |
| :--- | :--- | :--- |
| **Data Model** | Tabular relations with fixed schemas | Flexible, nested JSON/BSON documents |
| **Schema Flexibility**| Rigid (DDL migrations required) | Dynamic / Schema-less |
| **Transactions** | Full Multi-table ACID support | Document-level ACID (replica set transactions) |
| **Join Operations** | Efficient relational joins ($STUDENT \bowtie ROOM$) | Denormalized embedded structures or `$lookup` |
| **Scalability** | Vertical scaling (Scale-up) | Horizontal sharding across clusters (Scale-out) |

---

### 5. Document-Oriented Representation (MongoDB BSON/JSON)

In a document-based NoSQL architecture like MongoDB, student details, allocations, and payment histories can be denormalized and stored as a single cohesive student document:

```json
{
  "_id": "STU_2026_101",
  "student_id": 101,
  "name": "Aarav Kumar",
  "department": "CSE",
  "year_of_study": 2,
  "contact": {
    "phone": "9876543210",
    "email": "aarav.kumar@univ.edu"
  },
  "current_allocation": {
    "allocation_id": 1001,
    "room_number": "A-101",
    "room_type": "Single AC",
    "allocated_on": "2026-07-01T09:00:00Z",
    "status": "ALLOCATED"
  },
  "stay_history": [
    {
      "record_id": 501,
      "check_in": "2026-07-01T10:30:00Z",
      "check_out": null
    }
  ],
  "fee_account": {
    "total_fee": 65000.00,
    "paid_amount": 65000.00,
    "pending_amount": 0.00,
    "payment_status": "PAID",
    "transactions": [
      {
        "payment_id": 901,
        "amount": 65000.00,
        "date": "2026-07-05T14:20:00Z",
        "method": "UPI"
      }
    ]
  }
}
```
*Advantage:* Eliminates multi-table joins when retrieving a student's complete profile and fee status in a single query.
