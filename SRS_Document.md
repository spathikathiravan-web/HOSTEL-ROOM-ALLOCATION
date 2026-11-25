# Software Requirements Specification (SRS)
## Hostel Room Allocation and Student Accommodation Analysis System

**Document Version:** 1.0  
**Standard:** IEEE Std 830-1998 Compliant  
**Course Code:** 25ITT33 – Software Engineering  
**Academic Institution:** Department of Information Technology, Velalar College of Engineering and Technology  

---

### Table of Contents
1. [Introduction](#1-introduction)
   - 1.1 Purpose
   - 1.2 Scope of the System
   - 1.3 Definitions, Acronyms, and Abbreviations
   - 1.4 References
   - 1.5 Overview of the Document
2. [Overall Description](#2-overall-description)
   - 2.1 Product Perspective
   - 2.2 Product Functions
   - 2.3 User Classes and Characteristics
   - 2.4 Operating Environment
   - 2.5 Design and Implementation Constraints
   - 2.6 Assumptions and Dependencies
3. [System Features and Functional Requirements](#3-system-features-and-functional-requirements)
   - 3.1 Module 1: Student Information Management
   - 3.2 Module 2: Hostel and Room Management
   - 3.3 Module 3: Room Allocation and Capacity Control
   - 3.4 Module 4: Student Check-In and Check-Out Management
   - 3.5 Module 5: Hostel Fee Payment and Arrears Tracking
   - 3.6 Module 6: Operational Report Generation
   - 3.7 Module 7: Data Science Analytics and Visualization Pipeline
4. [External Interface Requirements](#4-external-interface-requirements)
   - 4.1 User Interfaces
   - 4.2 Hardware Interfaces
   - 4.3 Software Interfaces
   - 4.4 Communication Interfaces
5. [Non-Functional Requirements](#5-non-functional-requirements)
   - 5.1 Performance Requirements
   - 5.2 Reliability and Availability
   - 5.3 Security and Access Control
   - 5.4 Maintainability and Portability
   - 5.5 Data Integrity and Business Rules
6. [Verification, Validation, and Acceptance Criteria](#6-verification-validation-and-acceptance-criteria)

---

### 1. Introduction

#### 1.1 Purpose
The purpose of this Software Requirements Specification (SRS) document is to provide a complete, detailed, and formal description of the **Hostel Room Allocation and Student Accommodation Analysis System**. It defines both functional and non-functional requirements for developers, database administrators, data scientists, software testers, and hostel administrative authorities.

#### 1.2 Scope of the System
The system is designed to automate and optimize the end-to-end accommodation lifecycle in a college hostel. The system replaces manual register-based record-keeping which is prone to over-allocation errors, inaccurate room availability tracking, delayed fee collection, and lack of visual management insights.
Key capabilities include:
- Centralized student profiling across departments and study years.
- Granular room capacity tracking across various room categories (Single AC, Double Non-AC, Triple Non-AC).
- Automated room allocation logic enforcing strict room capacity validation to prohibit over-allocation.
- Movement tracking capturing check-in and check-out timestamps.
- Financial accounting of hostel fees, tracking installments, waivers, and identifying pending fee defaulters.
- Multi-threaded reporting for operational auditing.
- Automated data extraction and Python-based exploratory data analysis (EDA) with statistical visualizations.

#### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS:** Software Requirements Specification (IEEE 830).
- **DBMS:** Database Management System (Relational database management).
- **PK / FK:** Primary Key / Foreign Key.
- **ACID:** Atomicity, Consistency, Isolation, Durability.
- **DFD:** Data Flow Diagram.
- **EDA:** Exploratory Data Analysis.
- **Occupancy:** The number of students currently actively assigned to a specific room.
- **Capacity:** The maximum number of beds physically available in a specific room.
- **Pending Amount:** Total fee minus paid fee amount for an enrolled student.

#### 1.4 References
- IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications.
- Roger S. Pressman & Bruce R. Maxim, *Software Engineering: A Practitioner's Approach*, 9th Edition, McGraw-Hill.
- Abraham Silberschatz, Henry F. Korth, S. Sudarshan, *Database System Concepts*, 7th Edition.
- Anna University / VCET B.Tech IT Curriculum Regulations R2025.

#### 1.5 Overview of the Document
Section 2 provides the overall product context, user characteristics, and technical constraints. Section 3 elaborates on detailed functional requirements categorized by functional modules. Section 4 specifies external interfaces. Section 5 defines non-functional quality attributes. Section 6 provides testing and acceptance standards.

---

### 2. Overall Description

#### 2.1 Product Perspective
The system operates as an integrated three-tier client-server enterprise architecture:
1. **Presentation & Application Layer (Java):** Provides the administrative interface, object-oriented domain models, stream-based queries, business validation logic, and multi-threaded report generators.
2. **Persistence Layer (DBMS / Relational Database):** Enforces ACID transactions, relational integrity constraints, foreign key relationships, triggers, and views.
3. **Analytical & Visualization Layer (Python):** Ingests raw relational tables, performs data wrangling, missing value treatment, outlier detection with z-scores, and renders statistical visualizations using Pandas, NumPy, Matplotlib, and Seaborn.

```
+-------------------------------------------------------------+
|                 Hostel Administrator                        |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|        Java Application Layer (OOP, Streams, Threads)        |
+-------------------------------------------------------------+
           |                                       |
           v                                       v
+-----------------------------+       +-----------------------+
|  Relational Database (DBMS) |<----->| Python Data Analytics |
|  Tables, Constraints, Views |       | Pandas, EDA, Plots    |
+-----------------------------+       +-----------------------+
```

#### 2.2 Product Functions
- Maintain student records with personal, academic, and contact attributes.
- Maintain hostel inventory including room numbers, types, bed capacities, and active occupancies.
- Check available beds dynamically and allocate rooms, strictly rejecting requests exceeding bed limits.
- Manage check-in and check-out logs for student arrivals and departures.
- Manage fee structures, payments, receipts, and filter students with arrears.
- Generate operational text summaries and multi-threaded reports.
- Export datasets and generate 7 distinct visual analytics charts for management review.

#### 2.3 User Classes and Characteristics
- **Hostel Administrator:** Primary operator with rights to register students, create rooms, execute allocations, record check-ins/outs, and log fee payments.
- **Hostel Warden / Management:** Executive authorities who review occupancy dashboards, vacant bed distributions, and fee collection summaries.
- **Database Administrator (DBA):** Maintains database integrity, backups, triggers, and indices.
- **Data Analyst:** Runs Python scripts to derive occupancy patterns, demand forecasting, and arrears trends.

#### 2.4 Operating Environment
- Operating System: Windows 10/11 (64-bit) / Linux.
- Java Runtime: JDK 17 / JDK 21 / JDK 27.
- Python Environment: Python 3.10+ with Pandas, NumPy, Matplotlib, Seaborn.
- Relational Database: SQLite / MySQL 8.0+.
- Execution Shell: Windows Command Prompt / PowerShell with runnable `.bat` scripts.

#### 2.5 Design and Implementation Constraints
- Must implement Object-Oriented principles (Encapsulation, Inheritance, Polymorphism, Interfaces) in Java.
- Must implement Java Collections Framework and Stream API with Lambda expressions.
- Database must satisfy Boyce-Codd Normal Form (BCNF) / 3NF without update or deletion anomalies.
- Room allocation must be atomic: allocation insertion and room occupancy increment must occur within a synchronized transaction.
- Standalone execution must be supported via single-click runnable `.bat` files.

#### 2.6 Assumptions and Dependencies
- Each student possesses a unique institutional Student ID.
- Each room has a fixed maximum bed capacity ($1 \le capacity \le 4$).
- A student can hold at most ONE active room allocation at any point in time.

---

### 3. System Features and Functional Requirements

#### 3.1 Module 1: Student Information Management
- **FR-1.1:** The system shall allow the administrator to register new student records with `studentId`, `studentName`, `department`, `yearOfStudy`, `phone`, and `email`.
- **FR-1.2:** The system shall validate that student phone numbers conform to a 10-digit format and emails follow valid syntax (`user@domain.ext`).
- **FR-1.3:** The system shall allow searching for student records by Student ID or Name.
- **FR-1.4:** The system shall allow updating student contact information and year of study.
- **FR-1.5:** The system shall display a full roster of enrolled hostellers sorted by department and year.

#### 3.2 Module 2: Hostel and Room Management
- **FR-2.1:** The system shall maintain room definitions including `roomId`, `roomNumber`, `roomType` (Single AC, Double Non-AC, Triple Non-AC), `capacity`, and `occupancy`.
- **FR-2.2:** The system shall initialize new room occupancy to 0 upon creation.
- **FR-2.3:** The system shall dynamically compute `availableBeds = capacity - occupancy`.
- **FR-2.4:** The system shall categorize rooms as "Vacant" (`occupancy == 0`), "Partially Occupied" (`0 < occupancy < capacity`), or "Fully Occupied" (`occupancy == capacity`).

#### 3.3 Module 3: Room Allocation and Capacity Control
- **FR-3.1:** The system shall allow selecting a registered student and an active room to generate an allocation record.
- **FR-3.2:** The system shall check whether the student already has an active allocation; if yes, the allocation request shall be rejected with an appropriate error message.
- **FR-3.3 (Critical):** The system shall verify `availableBeds > 0` before committing allocation. If `occupancy >= capacity`, the system shall throw `RoomCapacityExceededException` and abort the allocation.
- **FR-3.4:** Upon successful allocation, the system shall atomically increment the room's `occupancy` by 1 and set allocation status to `ALLOCATED`.
- **FR-3.5:** The system shall allow room release/deallocation, which resets allocation status to `RELEASED` and decrements room `occupancy` by 1.

#### 3.4 Module 4: Student Check-In and Check-Out Management
- **FR-4.1:** The system shall allow recording a student's physical check-in date linked to an active allocation.
- **FR-4.2:** The system shall allow recording a student's physical check-out date.
- **FR-4.3:** The system shall validate that `checkOutDate` is chronologically on or after `checkInDate`.
- **FR-4.4:** The system shall log student stay history for administrative auditing.

#### 3.5 Module 5: Hostel Fee Payment and Arrears Tracking
- **FR-5.1:** The system shall define standard hostel fee tariffs based on room type (e.g., Single AC: ₹65,000, Double Non-AC: ₹45,000, Triple Non-AC: ₹35,000 per semester).
- **FR-5.2:** The system shall record fee payment transactions containing `paymentId`, `studentId`, `totalFee`, `paidAmount`, `pendingAmount`, `paymentDate`, and `paymentStatus`.
- **FR-5.3:** The system shall automatically compute `pendingAmount = totalFee - paidAmount`.
- **FR-5.4:** The system shall classify payment status as `PAID` (pending = 0), `PARTIAL` (paid > 0 and pending > 0), or `PENDING` (paid == 0).
- **FR-5.5:** The system shall query and display all students with outstanding balances.

#### 3.6 Module 6: Operational Report Generation
- **FR-6.1:** The system shall generate a comprehensive Room Availability Report showing all rooms, total capacity, occupied beds, and vacant slots.
- **FR-6.2:** The system shall generate a Hostel Occupancy Summary detailing total rooms, total capacity, total hostellers, and overall occupancy percentage.
- **FR-6.3:** The system shall generate a Fee Defaulter Report listing student IDs, names, phone numbers, and pending balances.
- **FR-6.4:** The system shall execute report generation using asynchronous background worker threads to avoid freezing user workflows.

#### 3.7 Module 7: Data Science Analytics and Visualization Pipeline
- **FR-7.1:** The system shall extract normalized data from the relational database tables into Pandas DataFrames.
- **FR-7.2:** The pipeline shall preprocess the data by handling nulls, verifying data types, and computing descriptive statistics (Mean, Median, Standard Deviation, Z-Scores).
- **FR-7.3:** The pipeline shall produce 7 publication-quality charts saved as PNG images:
  1. Room Occupancy by Room Type (Grouped Bar Chart).
  2. Overall Hostel Occupancy Rate (Donut Chart).
  3. Department-wise Student Accommodation Distribution (Bar / Pie Chart).
  4. Hostel Fee Collection vs Pending Amount (Stacked / Donut Chart).
  5. Fee Payment Distribution across Years of Study (Seaborn Box Plot).
  6. Monthly Check-in and Check-out Trends (Time Series Line Chart).
  7. Multi-Variable Correlation Heatmap (Seaborn Heatmap).
- **FR-7.4:** The system shall output statistical summaries to both console and a formatted output text file.

---

### 4. External Interface Requirements

#### 4.1 User Interfaces
- Clean, structured Console Command-Line Interface (CLI) in Java featuring formatted ANSI tables, hierarchical menus, and automated test demonstrations.
- Interactive terminal progress indicators for background worker threads.
- High-resolution visual output plots generated via Matplotlib and Seaborn.

#### 4.2 Hardware Interfaces
- Processor: x86_64 architecture, Dual-Core 2.0 GHz or higher.
- RAM: Minimum 2 GB (4 GB recommended).
- Storage: Minimum 500 MB free hard disk space.

#### 4.3 Software Interfaces
- Operating System: Microsoft Windows 10/11, Linux, or macOS.
- Language Environments: Java SE 17+ (installed JDK 27.0.1.1), Python 3.12+.
- Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `sqlite3`.
- Scripting: Windows Batch (`.bat`) command scripts.

#### 4.4 Communication Interfaces
- Standard JDBC / native DB connection protocols for data access.
- Local filesystem IPC for dataset exports (`.csv`) and generated charts (`.png`).

---

### 5. Non-Functional Requirements

#### 5.1 Performance Requirements
- Room allocation query and validation response time shall be under 50 milliseconds.
- Java application startup and test suite execution shall complete within 3 seconds.
- Python data wrangling and generation of all 7 visualization plots shall complete within 5 seconds.

#### 5.2 Reliability and Availability
- The system shall ensure zero data loss by utilizing ACID transactions with commit/rollback mechanisms.
- Database write operations shall prevent concurrent dirty reads and lost updates.

#### 5.3 Security and Access Control
- Input sanitization on all user entries to prevent SQL injection and buffer overflow errors.
- Role-based logical boundary isolating student views from administrative allocation privileges.

#### 5.4 Maintainability and Portability
- Modular, package-based Java architecture (`com.hostel.model`, `com.hostel.service`, `com.hostel.exception`, `com.hostel.util`).
- Cross-platform portability across Windows and POSIX-compliant operating systems.

#### 5.5 Data Integrity and Business Rules
1. A student can have multiple historical allocations over time, but only **ONE** active allocation at any given moment.
2. Room occupancy must satisfy: $0 \le occupancy \le capacity$.
3. Financial payments must satisfy: $0 \le paidAmount \le totalFee$ and $pendingAmount = totalFee - paidAmount$.

---

### 6. Verification, Validation, and Acceptance Criteria
- 100% pass rate across all functional unit and integration test cases.
- Successful execution of all three `.bat` scripts (`run_java.bat`, `run_dbms.bat`, `run_data_science.bat`) yielding matching console and text logs.
- Successful generation and verification of all 7 statistical visualization plots.
