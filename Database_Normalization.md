# Database Normalization and Dependency Theory
## Hostel Room Allocation and Student Accommodation Analysis System

**Course Code:** 25ITT31 – Database Management Systems (Unit 3: Normalization and Query Optimization)  
**Deliverable Category:** 2. Database Management System  

---

### Table of Contents
1. [Introduction to Relational Normalization](#1-introduction-to-relational-normalization)
2. [Functional Dependencies (FDs)](#2-functional-dependencies-fds)
3. [Armstrong's Axioms and Inference Rules](#3-armstrongs-axioms-and-inference-rules)
4. [Step-by-Step Normalization Process](#4-step-by-step-normalization-process)
   - 4.1 Unnormalized Form (UNF)
   - 4.2 First Normal Form (1NF)
   - 4.3 Second Normal Form (2NF)
   - 4.4 Third Normal Form (3NF)
   - 4.5 Boyce-Codd Normal Form (BCNF)
5. [Decomposition Properties: Lossless Join & Dependency Preservation](#5-decomposition-properties-lossless-join--dependency-preservation)

---

### 1. Introduction to Relational Normalization

Relational database normalization is the formal process of structuring relational schemas to minimize data redundancy, eliminate update, insertion, and deletion anomalies, and maintain data consistency across database transactions.

---

### 2. Functional Dependencies (FDs)

Let $R$ be a relational schema. A functional dependency $\alpha \rightarrow \beta$ holds on $R$ if, for any two tuples $t_1, t_2 \in R$, whenever $t_1[\alpha] = t_2[\alpha]$, it must also hold that $t_1[\beta] = t_2[\beta]$.

In the Hostel Management System, the set of fundamental functional dependencies $F$ is defined as follows:

- **$FD_1$ (Student Entity):**
  $$student\_id \rightarrow \{student\_name, department, year\_of\_study, phone, email\}$$
- **$FD_2$ (Student Unique Email):**
  $$email \rightarrow \{student\_id, student\_name, department, year\_of\_study, phone\}$$
- **$FD_3$ (Room Entity):**
  $$room\_id \rightarrow \{room\_number, room\_type, capacity, occupancy\}$$
- **$FD_4$ (Room Number Unique):**
  $$room\_number \rightarrow \{room\_id, room\_type, capacity, occupancy\}$$
- **$FD_5$ (Allocation Entity):**
  $$allocation\_id \rightarrow \{student\_id, room\_id, allocation\_date, allocation\_status\}$$
- **$FD_6$ (Check-In/Out Entity):**
  $$record\_id \rightarrow \{allocation\_id, checkin\_date, checkout\_date\}$$
- **$FD_7$ (Fee Payment Entity):**
  $$payment\_id \rightarrow \{student\_id, total\_fee, paid\_amount, pending\_amount, payment\_date, payment\_status\}$$

---

### 3. Armstrong's Axioms and Inference Rules

Using Armstrong's sound and complete inference axioms on $F$:

1. **Axiom of Reflexivity:**
   If $\beta \subseteq \alpha$, then $\alpha \rightarrow \beta$.
   - *Example:* $\{student\_id, student\_name\} \rightarrow student\_id$.
2. **Axiom of Augmentation:**
   If $\alpha \rightarrow \beta$, then $\alpha \gamma \rightarrow \beta \gamma$ for any $\gamma$.
   - *Example:* $student\_id \rightarrow phone \implies \{student\_id, year\_of\_study\} \rightarrow \{phone, year\_of\_study\}$.
3. **Axiom of Transitivity:**
   If $\alpha \rightarrow \beta$ and $\beta \rightarrow \gamma$, then $\alpha \rightarrow \gamma$.
   - *Example:* If $record\_id \rightarrow allocation\_id$ and $allocation\_id \rightarrow room\_id$, then $record\_id \rightarrow room\_id$.
4. **Secondary Rules (Union & Decomposition):**
   - **Union:** If $\alpha \rightarrow \beta$ and $\alpha \rightarrow \gamma$, then $\alpha \rightarrow \beta \gamma$.
   - **Decomposition:** If $\alpha \rightarrow \beta \gamma$, then $\alpha \rightarrow \beta$ and $\alpha \rightarrow \gamma$.

---

### 4. Step-by-Step Normalization Process

#### 4.1 Unnormalized Form (UNF)
Consider an unnormalized flat table capturing all hostel records:
$$UNF\_HOSTEL(student\_id, student\_name, department, year, phone, email, room\_id, room\_no, room\_type, cap, occ, alloc\_id, alloc\_date, checkin, checkout, pay\_id, total\_fee, paid, pending)$$
- *Problem:* Repeating groups of payments and check-ins; massive data duplication; risk of insertion anomalies (cannot add a room without an enrolled student).

#### 4.2 First Normal Form (1NF)
- **Definition:** A relation is in 1NF if and only if the domain of each attribute contains only atomic (indivisible) values, and there are no repeating groups.
- **Transformation:** Eliminate multi-valued attributes and composite contact fields. Define a composite primary key $(student\_id, room\_id, alloc\_id, pay\_id)$.
- *Anomaly in 1NF:* Severe redundancy; partial key dependencies exist.

#### 4.3 Second Normal Form (2NF)
- **Definition:** A relation is in 2NF if it is in 1NF and every non-prime attribute is fully functionally dependent on the primary key (no partial dependencies: $X \rightarrow Y$ where $X \subset \text{Key}$).
- **Decomposition:**
  - $student\_name, department$ depend solely on $student\_id$ (not the entire composite key).
  - $room\_number, capacity$ depend solely on $room\_id$.
  - Therefore, decompose into independent relations:
    - $STUDENT(\underline{student\_id}, \dots)$
    - $ROOM(\underline{room\_id}, \dots)$
    - $ALLOCATION(\underline{allocation\_id}, student\_id, room\_id, \dots)$
    - $FEE\_PAYMENT(\underline{payment\_id}, student\_id, \dots)$
    - $CHECK\_IN\_OUT(\underline{record\_id}, allocation\_id, \dots)$
- *Result:* All partial dependencies eliminated.

#### 4.4 Third Normal Form (3NF)
- **Definition:** A relation schema $R$ is in 3NF if, whenever a non-trivial functional dependency $\alpha \rightarrow \beta$ holds in $R$, either:
  1. $\alpha$ is a superkey of $R$, OR
  2. $\beta$ is a prime attribute (part of a candidate key).
- **Evaluation:** In all five relations:
  - In $STUDENT$: `student_id` is a candidate key.
  - In $ROOM$: `room_id` is a candidate key; `room_number` is an alternate candidate key.
  - In $ALLOCATION$: `allocation_id` is a candidate key.
  - In $CHECK\_IN\_OUT$: `record_id` is a candidate key.
  - In $FEE\_PAYMENT$: `payment_id` is a candidate key.
- There are no transitive dependencies of the form $Key \rightarrow NonKey_1 \rightarrow NonKey_2$.
- *Conclusion:* The schema is fully in **3NF**.

#### 4.5 Boyce-Codd Normal Form (BCNF)
- **Definition:** A relation schema $R$ is in BCNF if, for every non-trivial functional dependency $\alpha \rightarrow \beta$, $\alpha$ is a **superkey** of $R$.
- **Verification:**
  - In $STUDENT$, only $student\_id \rightarrow \text{attributes}$ and $email \rightarrow \text{attributes}$ hold. Both $student\_id$ and $email$ are candidate keys (superkeys).
  - In $ROOM$, both $room\_id$ and $room\_number$ are superkeys.
  - In all other tables, the left-hand side of every dependency is strictly a superkey.
- *Conclusion:* The design strictly satisfies **BCNF**.

---

### 5. Decomposition Properties: Lossless Join & Dependency Preservation

#### 5.1 Lossless Join Decomposition Proof
A decomposition of relation $R$ into $R_1$ and $R_2$ is lossless with respect to a set of FDs $F$ if and only if:
$$(R_1 \cap R_2) \rightarrow R_1 \quad \text{OR} \quad (R_1 \cap R_2) \rightarrow R_2$$
- For $STUDENT$ and $ALLOCATION$:
  $$R_1 \cap R_2 = \{student\_id\}$$
  Since $student\_id \rightarrow STUDENT$, $(R_1 \cap R_2)$ is a superkey of $R_1$. Hence, the natural join $STUDENT \bowtie ALLOCATION$ is guaranteed to be **lossless** (no spurious tuples).

#### 5.2 Dependency Preservation
Every functional dependency in the original set $F$ can be checked using attributes within a single decomposed relation without computing expensive joins.
- $F' \equiv F$, proving complete **dependency preservation**.
