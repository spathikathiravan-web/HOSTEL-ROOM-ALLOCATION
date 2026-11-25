# System Design and Architecture Documentation
## Hostel Room Allocation and Student Accommodation Analysis System

**Course Code:** 25ITT33 – Software Engineering (Units 2 & 3: Requirements & Software Design)  
**Deliverable Category:** 1. Software Engineering  

---

### Table of Contents
1. [Architectural Overview](#1-architectural-overview)
2. [1. Use Case Diagram](#2-1-use-case-diagram)
3. [2. Class Diagram](#3-2-class-diagram)
4. [3. System Architecture Diagram](#4-3-system-architecture-diagram)
5. [4. Data Flow Diagram – Level 0 (Context Diagram)](#5-4-data-flow-diagram--level-0-context-diagram)
6. [5. Data Flow Diagram – Level 1](#6-5-data-flow-diagram--level-1)
7. [6. Activity Diagram (Room Allocation with Capacity Validation)](#7-6-activity-diagram)
8. [7. Sequence Diagram (Successful Room Allocation Flow)](#8-7-sequence-diagram)
9. [Design Patterns and Principles Applied](#9-design-patterns-and-principles-applied)

---

### 1. Architectural Overview

The Hostel Room Allocation and Student Accommodation Analysis System adopts a decoupled **3-Tier Component Architecture** structured across:
1. **User Presentation & Application Layer (Java SE):** Console administrative dashboard, domain models, business logic services, multi-threaded task runners, and Stream API reporting.
2. **Enterprise Data Persistence Layer (DBMS):** Relational schema, referential integrity constraints, automated triggers for capacity updates, stored views, and ACID transaction boundaries.
3. **Analytics and Visual Insight Layer (Python Data Science):** Statistical preprocessing, NumPy vectorization, Pandas grouping/pivoting, and Matplotlib/Seaborn visual renderers.

---

### 2. 1. Use Case Diagram

The Use Case Diagram defines the behavioral boundaries of the Hostel Management System and illustrates interactions between the primary actor (**Hostel Administrator**) and the core functional capabilities.

> **Diagram Image:** [use_case_diagram.jpg](file:///D:/HostelManagementSystem/1_software_engineering/use_case_diagram.jpg)

```mermaid
flowchart LR
    Admin["fa:fa-user Hostel Administrator"]
    
    subgraph SystemBoundary ["HOSTEL MANAGEMENT SYSTEM"]
        UC1(["Manage student details"])
        UC2(["Allocate / release room"])
        UC3(["Manage fee payments"])
        UC4(["Generate hostel reports"])
        UC5(["Manage hostel / room details"])
        UC6(["Record check-in / check-out"])
        UC7(["Identify pending payments"])
        UC8(["View Python visualizations"])
    end

    Admin --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5
    Admin --> UC6
    Admin --> UC7
    Admin --> UC8
```

#### Actor and Use Case Specification:
- **Hostel Administrator:** Primary operational actor authorized to manage student registries, room inventories, room allocations, check-ins/outs, and payment audits.
- **UC-1 Manage Student Details:** Allows creating, updating, searching, and viewing student profiles.
- **UC-2 Allocate / Release Room:** Performs bed allocation verifying available capacity, and deallocates rooms upon student exit.
- **UC-3 Manage Fee Payments:** Records fee receipts, calculating pending amounts.
- **UC-4 Generate Hostel Reports:** Produces room occupancy, availability, and financial summaries.
- **UC-5 Manage Hostel / Room Details:** Configures room inventory, room types, and bed capacities.
- **UC-6 Record Check-in / Check-out:** Tracks physical dates of arrival and departure.
- **UC-7 Identify Pending Payments:** Filters records where `pendingAmount > 0`.
- **UC-8 View Python Visualizations:** Launches data science scripts to examine graphical occupancy and fee distribution plots.

---

### 3. 2. Class Diagram

The Class Diagram depicts the object-oriented structure of the domain model, capturing core classes, attributes, access visibility modifiers (`+` public, `-` private), methods, and structural associations with multiplicities.

> **Diagram Image:** [class_diagram.jpg](file:///D:/HostelManagementSystem/1_software_engineering/class_diagram.jpg)

```mermaid
classDiagram
    class Student {
        +int studentId
        +String name
        +String department
        +int year
        +String phone
        +String email
        +addStudent()
        +updateStudent()
        +searchStudent()
    }

    class Room {
        +int roomId
        +String roomNumber
        +String roomType
        +int capacity
        +int occupancy
        +availableBeds() int
        +updateOccupancy(int change)
    }

    class Allocation {
        +int allocationId
        +Date allocationDate
        +String status
        +int studentId
        +int roomId
        +allocateRoom()
        +releaseRoom()
    }

    class CheckInOut {
        +int recordId
        +int studentId
        +Date checkInDate
        +Date checkOutDate
        +checkIn()
        +checkOut()
    }

    class FeePayment {
        +int paymentId
        +int studentId
        +Decimal totalFee
        +Decimal paidAmount
        +Decimal pendingAmount
        +String status
        +recordPayment()
        +calculatePending()
    }

    Student "1" --> "0..*" Room : stays in
    Room "1" --> "0..*" Allocation : has
    Student "1" --> "0..*" CheckInOut : has stay record
    Student "1" --> "0..*" FeePayment : makes payments
```

#### Multiplicity and Structural Rules:
- **Student to Allocation (`1` to `0..*`):** A student can have multiple allocation records historically, but at most **ONE active allocation** at any given time.
- **Room to Allocation (`1` to `0..*`):** A room can be allocated to multiple students over time, provided current `occupancy <= capacity`.
- **Student to CheckInOut (`1` to `0..*`):** A student accumulates check-in/out records representing physical stays.
- **Student to FeePayment (`1` to `0..*`):** A student may pay semester fees in multiple installments.

---

### 4. 3. System Architecture Diagram

The System Architecture Diagram illustrates the tiered organization of the software, highlighting communication flows between user actors, application logic, database storage, and analytical pipelines.

> **Diagram Image:** [system_architecture_diagram.jpg](file:///D:/HostelManagementSystem/1_software_engineering/system_architecture_diagram.jpg)

```mermaid
flowchart TD
    Admin["HOSTEL ADMINISTRATOR"] --> AppLayer["JAVA APPLICATION LAYER<br/>User Interface + Business Logic"]
    
    AppLayer -->|"application logic"| JavaMods["JAVA MODULES<br/>Student | Room | Allocation<br/>Check-in/out | Fee | Reports"]
    AppLayer -->|"read / write"| MySQLDB[("MYSQL / RELATIONAL DATABASE<br/>Student | Room | Allocation<br/>CheckInOut | FeePayment")]
    AppLayer -->|"retrieve data"| PyAnalytics["PYTHON ANALYTICS<br/>Pandas preprocessing<br/>Matplotlib / Seaborn"]

    JavaMods -->|"status / records"| ReportsViz["REPORTS AND VISUALIZATIONS<br/>Occupancy | Room availability | Fee status"]
    MySQLDB -->|"stored data"| ReportsViz
    PyAnalytics -->|"charts"| ReportsViz

    ReportsViz --> AdminReview["ADMINISTRATOR REVIEWS RESULTS"]
```

#### Architectural Tiers:
1. **Hostel Administrator Interface:** Initiates commands via CLI or batch scripts.
2. **Java Application Layer:** Hosts core domain business logic, handles input validation, executes Stream pipelines, and initiates asynchronous multi-threaded jobs.
3. **Database Layer:** Maintains relational tables (`STUDENT`, `ROOM`, `ALLOCATION`, `CHECK_IN_OUT`, `FEE_PAYMENT`), enforces constraints and triggers.
4. **Python Analytics Layer:** Preprocesses dataset, performs descriptive statistical calculations, detects outliers with z-scores, and generates 7 distinct high-resolution charts.
5. **Report & Visualization Output:** Aggregates console reports, text exports, and visual charts for review by hostel authorities.

---

### 5. 4. Data Flow Diagram – Level 0 (Context Diagram)

The Level-0 Context Diagram establishes the global information boundary, showing the entire system as a single process interacting with external entities.

> **Diagram Image:** [dfd_level_0.jpg](file:///D:/HostelManagementSystem/1_software_engineering/dfd_level_0.jpg)

```mermaid
flowchart LR
    Admin["HOSTEL ADMINISTRATOR"]
    Sys(("0<br/>HOSTEL ROOM ALLOCATION AND<br/>STUDENT ACCOMMODATION<br/>ANALYSIS SYSTEM"))
    Mgmt["HOSTEL MANAGEMENT"]

    Admin -->|"student / room / fee data"| Sys
    Sys -->|"allocation status / records"| Admin
    Mgmt -->|"report request"| Sys
    Sys -->|"occupancy / payment reports"| Mgmt
```

#### Data Flows:
- **Admin to System:** Student profiles, room details, room allocation requests, check-in/out entries, fee transactions.
- **System to Admin:** Allocation status, validation confirmations, receipt vouchers, search records.
- **Management to System:** High-level requests for room availability, capacity utilization, and fee arrears audits.
- **System to Management:** Room occupancy dashboards, revenue reports, and Python graphical visualizations.

---

### 6. 5. Data Flow Diagram – Level 1

The Level-1 Data Flow Diagram decomposes Process 0 into its constituent functional processes and links them to underlying relational data stores.

> **Diagram Image:** [dfd_level_1.jpg](file:///D:/HostelManagementSystem/1_software_engineering/dfd_level_1.jpg)

```mermaid
flowchart TD
    Admin["ADMIN"]
    
    P1(("1.0 Manage Student<br/>& Room Data"))
    P2(("2.0 Allocate<br/>Room"))
    P3(("3.0 Manage Check-in /<br/>Check-out"))
    P4(("4.0 Manage Fee<br/>Payments"))
    P5(("5.0 Generate<br/>Reports"))
    P6(("6.0 Python Data<br/>Analysis"))

    D1[("D1 Student")]
    D2[("D2 Room / Allocation")]
    D3[("D3 CheckInOut")]
    D4[("D4 FeePayment")]

    Admin -->|"student / room data"| P1
    P1 -->|"student data"| D1
    P1 -->|"room data"| P2
    P2 -->|"allocation"| P3
    P2 -->|"allocation data"| D2

    Admin -->|"payment details"| P4
    P4 -->|"fee data"| D4

    D1 -->|"student data"| P4
    D2 -->|"allocation data"| P5
    P3 -->|"movement records"| D3

    D3 -->|"check-in/out data"| P6
    D2 -->|"hostel data"| P6
    D4 -->|"fee data"| P6

    P5 -->|"report data"| D2
    P6 -->|"visual reports"| Admin
```

---

### 7. 6. Activity Diagram

The Activity Diagram models the decision logic executed during a room allocation request, highlighting strict capacity validation rules that prevent over-allocation.

> **Diagram Image:** [activity_diagram.jpg](file:///D:/HostelManagementSystem/1_software_engineering/activity_diagram.jpg)

```mermaid
flowchart TD
    Start((●)) --> EnterStudent["Enter / select Student ID"]
    EnterStudent --> FetchStudent["Retrieve student details"]
    FetchStudent --> SelectRoom["Select requested room"]
    SelectRoom --> CheckRoom{"Room exists<br/>and is active?"}

    CheckRoom -- "No" --> DispInvalid["Display invalid room message"]
    DispInvalid --> End1((◉))

    CheckRoom -- "Yes" --> CheckCap{"Available beds<br/>> 0?"}

    CheckCap -- "No" --> DispFull["Display room full;<br/>reject allocation"]
    DispFull --> End2((◉))

    CheckCap -- "Yes" --> CreateAlloc["Create allocation record<br/>and update occupancy"]
    CreateAlloc --> ShowSuccess["Show success message"]
    ShowSuccess --> End3((◉))
```

#### Key Decision Gates:
1. **Room Validity Gate:** Ensures the requested room exists in the inventory.
2. **Bed Availability Gate (`availableBeds > 0`):** Compares current `occupancy` with `capacity`. If `occupancy >= capacity`, the request is immediately rejected, guaranteeing that over-allocation cannot occur.

---

### 8. 7. Sequence Diagram

The Sequence Diagram captures the chronological message exchange between participating objects during a successful room allocation transaction.

> **Diagram Image:** [sequence_diagram.jpg](file:///D:/HostelManagementSystem/1_software_engineering/sequence_diagram.jpg)

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Administrator
    participant UI as Java UI
    participant Service as Allocation Service
    participant DB as MySQL DB
    participant RoomData as Room data

    Admin ->> UI: Enter student ID and room ID
    UI ->> Service: allocateRoom(studentId, roomId)
    Service ->> DB: Fetch student and room records
    DB ->> RoomData: Read capacity and occupancy
    RoomData -->> Service: Return available beds
    Service ->> DB: Save allocation + update occupancy
    DB -->> Service: Commit transaction
    Service -->> UI: Allocation successful
    UI -->> Admin: Display confirmation
```

---

### 9. Design Patterns and Principles Applied

1. **Model-View-Controller / Service-Oriented Layering:** Clear separation of concerns between domain entities (`model`), business logic (`service`), exception management (`exception`), and user presentation (`Main`).
2. **Data Access Object (DAO) / Repository Pattern:** Encapsulates persistence interactions, allowing seamless swapping between in-memory collections, SQLite, and MySQL.
3. **Fail-Fast Validation & Custom Exceptions:** Capacity and duplicate allocation rules fail immediately with descriptive checked exceptions (`RoomCapacityExceededException`, `StudentAlreadyAllocatedException`).
4. **Observer / Asynchronous Worker Pattern:** Report generation is dispatched to dedicated worker threads (`OccupancyReportWorker`, `FeeAuditorWorker`), ensuring responsiveness.
