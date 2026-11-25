-- ==============================================================================
-- Hostel Room Allocation and Student Accommodation Analysis System
-- File: queries_and_views.sql
-- Description: Comprehensive SQL Queries Demonstrating Unit 2 SQL Syllabus
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. BASIC QUERIES AND SELECTION / PROJECTION
-- ------------------------------------------------------------------------------
-- Q1: Retrieve student ID, Name, Department, and Email for all 2nd-year students
SELECT student_id, student_name, department, email
FROM student
WHERE year_of_study = 2
ORDER BY department, student_name;

-- Q2: List all available rooms having vacant beds (available_beds > 0)
SELECT room_id, room_number, room_type, capacity, occupancy, (capacity - occupancy) AS available_beds
FROM room
WHERE occupancy < capacity
ORDER BY available_beds DESC;

-- ------------------------------------------------------------------------------
-- 2. AGGREGATE FUNCTIONS AND GROUP BY / HAVING (Unit 2 Syllabus)
-- ------------------------------------------------------------------------------
-- Q3: Hostel Capacity and Occupancy Metrics Summary
SELECT 
    COUNT(room_id) AS total_rooms,
    SUM(capacity) AS total_bed_capacity,
    SUM(occupancy) AS total_occupied_beds,
    (SUM(capacity) - SUM(occupancy)) AS total_vacant_beds,
    ROUND((CAST(SUM(occupancy) AS FLOAT) / SUM(capacity)) * 100, 2) AS overall_occupancy_rate_pct
FROM room;

-- Q4: Department-wise Count of Enrolled Students with HAVING filter
SELECT 
    department, 
    COUNT(student_id) AS student_count
FROM student
GROUP BY department
HAVING COUNT(student_id) >= 2
ORDER BY student_count DESC;

-- Q5: Financial Revenue and Arrears Audit
SELECT 
    payment_status,
    COUNT(payment_id) AS transaction_count,
    SUM(total_fee) AS total_billed,
    SUM(paid_amount) AS total_collected,
    SUM(pending_amount) AS total_pending
FROM fee_payment
GROUP BY payment_status;

-- ------------------------------------------------------------------------------
-- 3. INTERMEDIATE SQL: MULTI-TABLE JOINS (Unit 2 Syllabus)
-- ------------------------------------------------------------------------------
-- Q6: Full Active Hosteller Profile (Inner Join: Student + Allocation + Room)
SELECT 
    s.student_id,
    s.student_name,
    s.department,
    s.year_of_study,
    r.room_number,
    r.room_type,
    a.allocation_date,
    a.allocation_status
FROM allocation a
JOIN student s ON a.student_id = s.student_id
JOIN room r ON a.room_id = r.room_id
WHERE a.allocation_status = 'ALLOCATED'
ORDER BY r.room_number;

-- Q7: Left Outer Join: All Students and their current Room (including unallocated)
SELECT 
    s.student_id,
    s.student_name,
    s.department,
    COALESCE(r.room_number, 'NOT ALLOCATED') AS room_number,
    COALESCE(a.allocation_status, 'NONE') AS allocation_status
FROM student s
LEFT JOIN allocation a ON s.student_id = a.student_id AND a.allocation_status = 'ALLOCATED'
LEFT JOIN room r ON a.room_id = r.room_id;

-- ------------------------------------------------------------------------------
-- 4. NESTED SUBQUERIES AND ADVANCED SQL (Unit 2 Syllabus)
-- ------------------------------------------------------------------------------
-- Q8: Nested Subquery with IN: Students who are currently living in 'Single AC' rooms
SELECT student_id, student_name, department, phone
FROM student
WHERE student_id IN (
    SELECT student_id 
    FROM allocation 
    WHERE room_id IN (
        SELECT room_id FROM room WHERE room_type = 'Single AC'
    ) AND allocation_status = 'ALLOCATED'
);

-- Q9: Correlated Subquery with EXISTS: Rooms that have at least one active allocation
SELECT r.room_id, r.room_number, r.room_type
FROM room r
WHERE EXISTS (
    SELECT 1 FROM allocation a 
    WHERE a.room_id = r.room_id AND a.allocation_status = 'ALLOCATED'
);

-- Q10: Subquery in FROM clause: Room types with occupancy rate greater than 60%
SELECT room_type, total_cap, total_occ, occupancy_pct
FROM (
    SELECT 
        room_type,
        SUM(capacity) AS total_cap,
        SUM(occupancy) AS total_occ,
        ROUND((CAST(SUM(occupancy) AS FLOAT) / SUM(capacity)) * 100, 1) AS occupancy_pct
    FROM room
    GROUP BY room_type
) room_stats
WHERE occupancy_pct >= 60.0;

-- ------------------------------------------------------------------------------
-- 5. SET OPERATIONS (UNION, INTERSECT, EXCEPT / NOT IN)
-- ------------------------------------------------------------------------------
-- Q11: Find students who have made full payment UNION students who are 4th year
SELECT student_id, 'Full Payment Student' AS category FROM fee_payment WHERE payment_status = 'PAID'
UNION
SELECT student_id, 'Final Year Student' AS category FROM student WHERE year_of_study = 4;

-- ------------------------------------------------------------------------------
-- 6. VIEWS EXECUTION (Unit 2 Syllabus)
-- ------------------------------------------------------------------------------
-- Q12: Query View 1: Room Occupancy Summary
SELECT * FROM vw_room_occupancy_summary;

-- Q13: Query View 2: Fee Defaulters with Arrears > 0
SELECT * FROM vw_fee_defaulters_report ORDER BY pending_amount DESC;
