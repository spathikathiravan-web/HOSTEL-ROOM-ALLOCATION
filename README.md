# Hostel Room Allocation and Student Accommodation Analysis System

An enterprise-grade, multi-tier academic project developed using **Java SE (Object-Oriented Programming, Multithreading & Stream API)**, **Relational DBMS (SQL, Transactions, Normalization & Triggers)**, and **Python (Exploratory Data Analysis, NumPy & Data Visualizations)**.

---

## 🏛️ Course & Curriculum Alignment

| Category | Folder Name | Course Code & Title | Syllabi Units Covered | Key Deliverables |
| :--- | :--- | :--- | :--- | :--- |
| **1. Software Engineering** | `1_software_engineering` | **25ITT33** – Software Engineering | Units 1 to 5 (Process, Requirements, Design, Testing, Management) | SRS Document (IEEE 830), 7 UML & Architecture Diagrams, Test Suite & RTM, COCOMO & FP Estimation |
| **2. Database Management System** | `2_database_management_system` | **25ITT31** – Database Management Systems | Units 1 to 5 (ER Model, SQL, Normalization, Transactions, NoSQL) | E-R Diagram, Relational Model, 1NF-BCNF Normalization Proof, DDL/DML Scripts, Views, `run_dbms.bat`, Execution Output & Screenshot |
| **3. Java Programming** | `3_java_programming` | **25ITT32** – Java Programming | Units 1 to 5 (Classes, Inheritance, Exceptions, Multithreading, Streams) | Full Java SE Source Code, Custom Exceptions, Concurrent Worker Threads, Stream API Analytics, `run_java.bat`, Execution Output & Screenshot |
| **4. Foundation of Data Science** | `4_foundation_of_data_science` | **25ITC31** – Foundations of Data Science | Units 1 to 5 (Statistics, Python, NumPy/Pandas, Cleaning, Visualization) | Python EDA Pipeline, Jupyter Notebook, 7 Publication-Quality PNG Plots, `run_data_science.bat`, Execution Output & Screenshot |

---

## 📁 Repository Directory Structure

```
HostelManagementSystem/
│
├── README.md                                          <-- Master Project Documentation
│
├── 1_software_engineering/                            <-- CATEGORY 1: SOFTWARE ENGINEERING
│   ├── software_engineering_syllabus.jpg              <-- Syllabus Copy (25ITT33)
│   ├── SRS_Document.md                                <-- IEEE Std 830-1998 Compliant Specification
│   ├── System_Design_and_Architecture.md              <-- System Architecture & Design Walkthrough
│   ├── Software_Testing_Documentation.md              <-- V-Model Testing Strategy & 17 Test Cases (PASS)
│   ├── Project_Management_and_Metrics.md              <-- 4P's, FP, COCOMO Estimation & RMMM Plan
│   ├── use_case_diagram.jpg                           <-- 1. Use Case Diagram
│   ├── class_diagram.jpg                              <-- 2. Class Diagram
│   ├── system_architecture_diagram.jpg                <-- 3. System Architecture Diagram
│   ├── dfd_level_0.jpg                                <-- 4. Data Flow Diagram - Level 0 Context
│   ├── dfd_level_1.jpg                                <-- 5. Data Flow Diagram - Level 1
│   ├── activity_diagram.jpg                           <-- 6. Activity Diagram (Room Allocation)
│   └── sequence_diagram.jpg                           <-- 7. Sequence Diagram (Allocation Message Flow)
│
├── 2_database_management_system/                      <-- CATEGORY 2: DATABASE MANAGEMENT SYSTEM
│   ├── dbms_syllabus.jpg                              <-- Syllabus Copy (25ITT31)
│   ├── er_diagram.jpg                                 <-- Entity-Relationship Diagram (ERD)
│   ├── Relational_Data_Model_and_Schema.md            <-- Relational Schemas, Constraints & Algebra
│   ├── Database_Normalization.md                      <-- UNF -> 1NF -> 2NF -> 3NF -> BCNF Proof
│   ├── Transaction_Management_and_NoSQL.md            <-- ACID, 2PL, CAP Theorem & MongoDB BSON
│   ├── schema_ddl.sql                                 <-- DDL Script: Tables, Constraints, Views
│   ├── sample_data_dml.sql                            <-- DML Script: 15 Students, 10 Rooms, Payments
│   ├── queries_and_views.sql                          <-- SQL Queries: Joins, Subqueries, Aggregations
│   ├── hostel_database.db                             <-- Populated SQLite Relational Database
│   ├── run_dbms.py                                    <-- Automated DBMS Query Execution Engine
│   ├── run_dbms.bat                                   <-- 🟢 RUNNABLE BATCH FILE (Double-Click to Run)
│   ├── dbms_execution_output.txt                      <-- DBMS Program Execution Text Output
│   └── dbms_execution_screenshot.png                  <-- High-Resolution Execution Screenshot
│
├── 3_java_programming/                                <-- CATEGORY 3: JAVA PROGRAMMING
│   ├── java_syllabus.jpg                              <-- Syllabus Copy (25ITT32)
│   ├── Java_Architecture_and_OOP_Design.md            <-- OOP Design, Streams & Multithreading Guide
│   ├── run_java.bat                                   <-- 🟢 RUNNABLE BATCH FILE (Double-Click to Run)
│   ├── java_execution_output.txt                      <-- Java Program Execution Text Output
│   ├── java_execution_screenshot.png                  <-- High-Resolution Execution Screenshot
│   └── src/com/hostel/
│       ├── Main.java                                  <-- CLI Driver & Automated Verification Suite
│       ├── model/
│       │   ├── BaseEntity.java                        <-- Abstract Base Entity (Polymorphism)
│       │   ├── Student.java                           <-- Student Entity
│       │   ├── Room.java                              <-- Room Entity (Capacity/Occupancy logic)
│       │   ├── Allocation.java                        <-- Allocation Entity
│       │   ├── CheckInOut.java                        <-- Check-in / Check-out Tracker
│       │   └── FeePayment.java                        <-- Fee Ledger & Pending Dues Calculation
│       ├── service/
│       │   ├── HostelService.java                     <-- Interface (Dynamic Method Dispatch)
│       │   └── HostelServiceImpl.java                 <-- Collections, Streams, Thread Safety
│       ├── exception/
│       │   ├── HostelException.java                   <-- Base Checked Exception
│       │   ├── RoomCapacityExceededException.java     <-- Enforces Capacity Boundary Rule (FR-3)
│       │   ├── StudentAlreadyAllocatedException.java  <-- Prohibits Duplicate Active Allocation
│       │   └── EntityNotFoundException.java           <-- Entity Lookup Exception
│       └── thread/
│           ├── OccupancyReportWorker.java             <-- Asynchronous Worker (implements Runnable)
│           └── FeeAuditWorker.java                    <-- Financial Auditor (extends Thread)
│
└── 4_foundation_of_data_science/                      <-- CATEGORY 4: FOUNDATION OF DATA SCIENCE
    ├── data_science_syllabus.jpg                      <-- Syllabus Copy (25ITC31)
    ├── Data_Science_Methodology_and_Analysis.md       <-- Statistics, Preprocessing & EDA Report
    ├── Hostel_Accommodation_Analysis.ipynb            <-- Jupyter Notebook (Interactive EDA)
    ├── hostel_dataset.csv                             <-- Cleaned Project Dataset
    ├── hostel_data_analysis.py                        <-- Python EDA & Statistical Plot Pipeline
    ├── run_data_science.bat                           <-- 🟢 RUNNABLE BATCH FILE (Double-Click to Run)
    ├── data_science_execution_output.txt              <-- Data Science Program Execution Text Output
    ├── data_science_execution_screenshot.png          <-- High-Resolution Execution Screenshot
    └── visualizations/                                <-- 7 Publication-Quality Statistical Charts
        ├── 1_room_occupancy_by_type.png               <-- Grouped Bar: Bed Capacity vs Occupancy
        ├── 2_hostel_occupancy_donut.png               <-- Donut Chart: Occupancy vs Vacancy Rate
        ├── 3_department_wise_distribution.png         <-- Bar Chart: Hostellers by Department
        ├── 4_fee_collection_status.png               <-- Financial Bar: Billed vs Paid vs Pending
        ├── 5_fee_distribution_by_year.png             <-- Box Plot: Fee Dispersion Across Years
        ├── 6_monthly_checkin_checkout_trend.png       <-- Line Plot: Monthly Movement Trend
        └── 7_correlation_heatmap.png                  <-- Correlation Heatmap of Numerical Features
```

---

## ⚡ Quick Start: Running the 3 Runnable Batch Files

Each programming language category contains an autonomous, standalone **`.bat` file** that can be double-clicked directly in Windows File Explorer:

### 1. Database Management System (DBMS)
- **Path:** `2_database_management_system/run_dbms.bat`
- **Action:** Double-click `run_dbms.bat`.
- **What it does:** Initializes the SQLite database engine, executes `schema_ddl.sql`, populates `sample_data_dml.sql`, executes 9 complex SQL queries and views, outputs formatted ASCII tables, updates `dbms_execution_output.txt`, and generates `dbms_execution_screenshot.png`.

### 2. Java Programming Application
- **Path:** `3_java_programming/run_java.bat`
- **Action:** Double-click `run_java.bat`.
- **What it does:** Compiles all Java source code using `javac`, executes `com.hostel.Main`, runs the automated test verification suite (demonstrating student enrollment, room allocation, intercepting over-capacity exceptions, multithreaded workers, and Stream aggregations), updates `java_execution_output.txt`, and generates `java_execution_screenshot.png`.

### 3. Foundation of Data Science (Python)
- **Path:** `4_foundation_of_data_science/run_data_science.bat`
- **Action:** Double-click `run_data_science.bat`.
- **What it does:** Extracts relational records, performs data cleaning, computes descriptive statistics (Mean, Median, Std Dev, Variance, IQR, Z-scores), generates all 7 visualization plots in `visualizations/`, updates `data_science_execution_output.txt`, and generates `data_science_execution_screenshot.png`.

---

## 📋 Summary of Functional Requirements Implementation

1. **FR-1 Student Details Maintenance:** Enrolled 15 students across departments (`CSE`, `IT`, `ECE`, `MECH`, `AIDS`) with contact details and years of study.
2. **FR-2 Room Details Maintenance:** 10 rooms configured across `Single AC` (1 bed), `Double Non-AC` (2 beds), and `Triple Non-AC` (3 beds), tracking dynamic occupancy and bed availability ($capacity - occupancy$).
3. **FR-3 Prevent Allocation Beyond Capacity:** Implemented in Java service and Database triggers. If a room is full, the transaction is rejected with `RoomCapacityExceededException`.
4. **FR-4 Record Check-In / Check-Out:** Full movement tracking with timestamps for arrival and departure.
5. **FR-5 Fee Records & Pending Payment Audit:** Tracks ₹675,000 billed, ₹500,000 collected, and ₹175,000 pending across 7 defaulters.
6. **FR-6 Operational Report Generation:** Asynchronous multi-threaded reporting (`OccupancyReportWorker` & `FeeAuditWorker`) outputting occupancy dashboards and fee default ledgers.
7. **FR-7 Python Data Retrieval & Visualizations:** Automated SQL pipeline generating 7 distinct statistical charts covering bed availability, occupancy rates, financial collection, year-wise boxplots, and correlation heatmaps.

---

## 👨‍💻 Technologies Used
- **Programming Languages:** Java SE (JDK 27), Python 3.12, SQL (ANSI SQL / SQLite 3 / MySQL).
- **Python Libraries:** `numpy`, `matplotlib`, `pillow` (`PIL`).
- **Development Tools:** Windows Batch Automation (`.bat`), Git, Markdown.
