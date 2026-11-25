-- ==============================================================================
-- Hostel Room Allocation and Student Accommodation Analysis System
-- File: sample_data_dml.sql
-- Description: Population of realistic test records across all entities
-- ==============================================================================

-- 1. INSERT STUDENTS (15 Students across CSE, IT, ECE, MECH, AIDS; Years 1-4)
INSERT INTO student (student_id, student_name, department, year_of_study, phone, email) VALUES
(101, 'Aarav Kumar', 'CSE', 2, '9876543210', 'aarav.kumar@univ.edu'),
(102, 'Diya Sharma', 'IT', 3, '9876543211', 'diya.sharma@univ.edu'),
(103, 'Rohan Verma', 'ECE', 1, '9876543212', 'rohan.verma@univ.edu'),
(104, 'Ananya Iyer', 'CSE', 4, '9876543213', 'ananya.iyer@univ.edu'),
(105, 'Kavya Nair', 'AIDS', 2, '9876543214', 'kavya.nair@univ.edu'),
(106, 'Siddharth Patel', 'MECH', 3, '9876543215', 'siddharth.patel@univ.edu'),
(107, 'Pooja Reddy', 'IT', 2, '9876543216', 'pooja.reddy@univ.edu'),
(108, 'Vikram Singh', 'CSE', 1, '9876543217', 'vikram.singh@univ.edu'),
(109, 'Meera Joshi', 'ECE', 4, '9876543218', 'meera.joshi@univ.edu'),
(110, 'Aditya Menon', 'MECH', 2, '9876543219', 'aditya.menon@univ.edu'),
(111, 'Sneha Pillai', 'AIDS', 3, '9876543220', 'sneha.pillai@univ.edu'),
(112, 'Harish Balan', 'IT', 1, '9876543221', 'harish.balan@univ.edu'),
(113, 'Varun Rao', 'CSE', 3, '9876543222', 'varun.rao@univ.edu'),
(114, 'Tanvi Deshmukh', 'ECE', 2, '9876543223', 'tanvi.deshmukh@univ.edu'),
(115, 'Pranav Sundaram', 'MECH', 4, '9876543224', 'pranav.sundaram@univ.edu');

-- 2. INSERT ROOMS (10 Rooms across Single AC, Double Non-AC, Triple Non-AC)
-- Initial occupancy is set according to active allocations
INSERT INTO room (room_id, room_number, room_type, capacity, occupancy) VALUES
(201, 'A-101', 'Single AC', 1, 1),
(202, 'A-102', 'Single AC', 1, 1),
(203, 'A-103', 'Single AC', 1, 0),
(204, 'B-201', 'Double Non-AC', 2, 2),
(205, 'B-202', 'Double Non-AC', 2, 2),
(206, 'B-203', 'Double Non-AC', 2, 1),
(207, 'B-204', 'Double Non-AC', 2, 0),
(208, 'C-301', 'Triple Non-AC', 3, 3),
(209, 'C-302', 'Triple Non-AC', 3, 2),
(210, 'C-303', 'Triple Non-AC', 3, 0);

-- Total Capacity = 1+1+1+2+2+2+2+3+3+3 = 20 beds
-- Total Occupancy = 1+1+0+2+2+1+0+3+2+0 = 12 allocated students

-- 3. INSERT ALLOCATIONS (Active and historical)
INSERT INTO allocation (allocation_id, student_id, room_id, allocation_date, allocation_status) VALUES
(1001, 101, 201, '2026-07-01', 'ALLOCATED'),
(1002, 102, 202, '2026-07-01', 'ALLOCATED'),
(1003, 103, 204, '2026-07-02', 'ALLOCATED'),
(1004, 104, 204, '2026-07-02', 'ALLOCATED'),
(1005, 105, 205, '2026-07-03', 'ALLOCATED'),
(1006, 106, 205, '2026-07-03', 'ALLOCATED'),
(1007, 107, 206, '2026-07-04', 'ALLOCATED'),
(1008, 108, 208, '2026-07-05', 'ALLOCATED'),
(1009, 109, 208, '2026-07-05', 'ALLOCATED'),
(1010, 110, 208, '2026-07-05', 'ALLOCATED'),
(1011, 111, 209, '2026-07-06', 'ALLOCATED'),
(1012, 112, 209, '2026-07-06', 'ALLOCATED'),
(1013, 113, 203, '2026-01-10', 'RELEASED'),
(1014, 114, 207, '2026-01-15', 'RELEASED');

-- 4. INSERT CHECK-IN AND CHECK-OUT RECORDS
INSERT INTO check_in_out (record_id, allocation_id, checkin_date, checkout_date) VALUES
(501, 1001, '2026-07-01', NULL),
(502, 1002, '2026-07-01', NULL),
(503, 1003, '2026-07-02', NULL),
(504, 1004, '2026-07-02', NULL),
(505, 1005, '2026-07-03', NULL),
(506, 1006, '2026-07-03', NULL),
(507, 1007, '2026-07-04', NULL),
(508, 1008, '2026-07-05', NULL),
(509, 1009, '2026-07-05', NULL),
(510, 1010, '2026-07-05', NULL),
(511, 1011, '2026-07-06', NULL),
(512, 1012, '2026-07-06', NULL),
(513, 1013, '2026-01-10', '2026-06-30'),
(514, 1014, '2026-01-15', '2026-06-30');

-- 5. INSERT FEE PAYMENTS (Standard: Single AC = 65000, Double Non-AC = 45000, Triple Non-AC = 35000)
INSERT INTO fee_payment (payment_id, student_id, total_fee, paid_amount, pending_amount, payment_date, payment_status) VALUES
(901, 101, 65000.00, 65000.00, 0.00, '2026-07-05', 'PAID'),
(902, 102, 65000.00, 45000.00, 20000.00, '2026-07-06', 'PARTIAL'),
(903, 103, 45000.00, 45000.00, 0.00, '2026-07-05', 'PAID'),
(904, 104, 45000.00, 25000.00, 20000.00, '2026-07-07', 'PARTIAL'),
(905, 105, 45000.00, 45000.00, 0.00, '2026-07-04', 'PAID'),
(906, 106, 45000.00, 15000.00, 30000.00, '2026-07-08', 'PARTIAL'),
(907, 107, 45000.00, 45000.00, 0.00, '2026-07-05', 'PAID'),
(908, 108, 35000.00, 35000.00, 0.00, '2026-07-06', 'PAID'),
(909, 109, 35000.00, 20000.00, 15000.00, '2026-07-09', 'PARTIAL'),
(910, 110, 35000.00, 0.00, 35000.00, '2026-07-10', 'PENDING'),
(911, 111, 35000.00, 35000.00, 0.00, '2026-07-07', 'PAID'),
(912, 112, 35000.00, 15000.00, 20000.00, '2026-07-10', 'PARTIAL'),
(913, 113, 65000.00, 65000.00, 0.00, '2026-01-12', 'PAID'),
(914, 114, 45000.00, 45000.00, 0.00, '2026-01-16', 'PAID'),
(915, 115, 35000.00, 0.00, 35000.00, '2026-07-12', 'PENDING');
