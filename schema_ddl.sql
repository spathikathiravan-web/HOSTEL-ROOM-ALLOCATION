-- ==============================================================================
-- Hostel Room Allocation and Student Accommodation Analysis System
-- File: schema_ddl.sql
-- Description: Relational Schema DDL Definitions, Constraints, Indexes & Views
-- Compatible with: MySQL 8.0+ and SQLite 3
-- ==============================================================================

-- 1. STUDENT TABLE
DROP TABLE IF EXISTS check_in_out;
DROP TABLE IF EXISTS fee_payment;
DROP TABLE IF EXISTS allocation;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS student;

CREATE TABLE student (
    student_id INTEGER PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    year_of_study INTEGER NOT NULL CHECK (year_of_study BETWEEN 1 AND 4),
    phone VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- 2. ROOM TABLE
CREATE TABLE room (
    room_id INTEGER PRIMARY KEY,
    room_number VARCHAR(20) NOT NULL UNIQUE,
    room_type VARCHAR(30) NOT NULL CHECK (room_type IN ('Single AC', 'Double Non-AC', 'Triple Non-AC')),
    capacity INTEGER NOT NULL CHECK (capacity > 0 AND capacity <= 5),
    occupancy INTEGER NOT NULL DEFAULT 0 CHECK (occupancy >= 0 AND occupancy <= capacity)
);

-- 3. ALLOCATION TABLE
CREATE TABLE allocation (
    allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    allocation_date DATE NOT NULL,
    allocation_status VARCHAR(20) NOT NULL DEFAULT 'ALLOCATED' CHECK (allocation_status IN ('ALLOCATED', 'RELEASED', 'CANCELLED')),
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES room(room_id) ON DELETE RESTRICT
);

-- 4. CHECK_IN_OUT TABLE
CREATE TABLE check_in_out (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    allocation_id INTEGER NOT NULL,
    checkin_date DATE NOT NULL,
    checkout_date DATE,
    FOREIGN KEY (allocation_id) REFERENCES allocation(allocation_id) ON DELETE CASCADE
);

-- 5. FEE_PAYMENT TABLE
CREATE TABLE fee_payment (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    total_fee DECIMAL(10, 2) NOT NULL CHECK (total_fee >= 0),
    paid_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (paid_amount >= 0 AND paid_amount <= total_fee),
    pending_amount DECIMAL(10, 2) NOT NULL CHECK (pending_amount >= 0),
    payment_date DATE NOT NULL,
    payment_status VARCHAR(20) NOT NULL CHECK (payment_status IN ('PAID', 'PARTIAL', 'PENDING')),
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);

-- ==============================================================================
-- INDEXES FOR QUERY OPTIMIZATION (Unit 3 Syllabus)
-- ==============================================================================
CREATE INDEX idx_student_dept ON student(department);
CREATE INDEX idx_room_number ON room(room_number);
CREATE INDEX idx_alloc_student ON allocation(student_id);
CREATE INDEX idx_alloc_room ON allocation(room_id);
CREATE INDEX idx_fee_status ON fee_payment(payment_status);

-- ==============================================================================
-- VIEWS FOR ADMINISTRATIVE REPORTING (Unit 2 Syllabus)
-- ==============================================================================

-- View 1: Room Occupancy & Availability Summary
DROP VIEW IF EXISTS vw_room_occupancy_summary;
CREATE VIEW vw_room_occupancy_summary AS
SELECT 
    r.room_id,
    r.room_number,
    r.room_type,
    r.capacity,
    r.occupancy,
    (r.capacity - r.occupancy) AS available_beds,
    ROUND((CAST(r.occupancy AS FLOAT) / r.capacity) * 100, 1) AS occupancy_percentage,
    CASE 
        WHEN r.occupancy = 0 THEN 'Vacant'
        WHEN r.occupancy < r.capacity THEN 'Partially Occupied'
        ELSE 'Fully Occupied'
    END AS status_description
FROM room r;

-- View 2: Active Student Allocations with Room Details
DROP VIEW IF EXISTS vw_active_allocations;
CREATE VIEW vw_active_allocations AS
SELECT 
    a.allocation_id,
    s.student_id,
    s.student_name,
    s.department,
    s.year_of_study,
    s.phone,
    r.room_number,
    r.room_type,
    a.allocation_date,
    a.allocation_status
FROM allocation a
JOIN student s ON a.student_id = s.student_id
JOIN room r ON a.room_id = r.room_id
WHERE a.allocation_status = 'ALLOCATED';

-- View 3: Student Fee Status & Pending Dues Report
DROP VIEW IF EXISTS vw_fee_defaulters_report;
CREATE VIEW vw_fee_defaulters_report AS
SELECT 
    f.payment_id,
    s.student_id,
    s.student_name,
    s.department,
    s.phone,
    f.total_fee,
    f.paid_amount,
    f.pending_amount,
    f.payment_status,
    f.payment_date
FROM fee_payment f
JOIN student s ON f.student_id = s.student_id
WHERE f.pending_amount > 0;
