# Java Application Architecture and Object-Oriented Design
## Hostel Room Allocation and Student Accommodation Analysis System

**Course Code:** 25ITT32 – Java Programming  
**Deliverable Category:** 3. Java Programming  

---

### Table of Contents
1. [Architecture Overview](#1-architecture-overview)
2. [Syllabus Mapping (Units 1 to 5)](#2-syllabus-mapping-units-1-to-5)
3. [Package Structure](#3-package-structure)
4. [Critical Business Logic: Preventing Over-Allocation](#4-critical-business-logic-preventing-over-allocation)
5. [Stream API & Lambda Expressions](#5-stream-api--lambda-expressions)
6. [Multithreaded Concurrent Execution Model](#6-multithreaded-concurrent-execution-model)
7. [Compilation and Execution Guide](#7-compilation-and-execution-guide)

---

### 1. Architecture Overview

The Java application component is developed using modern Java SE (compatible with JDK 17 to JDK 27). It provides a robust, thread-safe domain model and service architecture that manages students, rooms, allocations, check-ins/outs, and fee payments while enforcing capacity validation and providing real-time analytics.

---

### 2. Syllabus Mapping (Units 1 to 5)

| Syllabus Unit | Topics Required | Implementation in Hostel System |
| :--- | :--- | :--- |
| **Unit 1: Introduction to Java** | Classes, Objects, Constructors, Method Overloading, Static, Access Control, Console I/O | `Student`, `Room`, `Allocation`, `FeePayment` classes with private fields, public getters/setters, overloaded constructors (`Student(id, name, dept)`), static counters for IDs, and formatted console I/O. |
| **Unit 2: Inheritance, Packages, Interfaces** | Inheritance, `super`, Method Overriding, Abstract Classes, Packages, Interfaces, Dynamic Method Dispatch | Abstract base class `BaseEntity`, inherited by all domain entities; `HostelService` interface implemented by `HostelServiceImpl`; package organization (`com.hostel.model`, `com.hostel.service`, `com.hostel.exception`, `com.hostel.thread`). |
| **Unit 3: Exception Handling & Multithreading** | Try-catch-finally, User-defined Exceptions, Multiple Catch, Java Thread Model, `Runnable`, `Thread`, Synchronization | Custom exceptions: `HostelException`, `RoomCapacityExceededException`, `StudentAlreadyAllocatedException`. Concurrent execution with `OccupancyReportWorker` (Runnable) and `FeeAuditWorker` (Thread) using `synchronized` methods. |
| **Unit 4: String Handling & File/Persistence** | String, StringBuilder, formatting, File I/O | Extensive use of `StringBuilder` for high-performance tabular report generation; `String.format` for aligned console columns; file export to `java_execution_output.txt`. |
| **Unit 5: Generics, Collections, Lambdas & Streams** | Generic Programming, Collections (`List`, `Map`), Lambda Expressions, Stream API (Filtering, Mapping, Sorting, Grouping, Collectors) | In-memory thread-safe `ConcurrentHashMap` and `List`; Stream pipelines for filtering available rooms (`r.availableBeds() > 0`), grouping students by department (`Collectors.groupingBy`), sorting by pending dues, and calculating statistics. |

---

### 3. Package Structure

```
3_java_programming/
├── java_syllabus.jpg
├── Java_Architecture_and_OOP_Design.md
├── run_java.bat
├── java_execution_output.txt
├── java_execution_screenshot.png
└── src/
    └── com/
        └── hostel/
            ├── Main.java
            ├── exception/
            │   ├── HostelException.java
            │   ├── RoomCapacityExceededException.java
            │   ├── StudentAlreadyAllocatedException.java
            │   └── EntityNotFoundException.java
            ├── model/
            │   ├── BaseEntity.java (Abstract Class)
            │   ├── Student.java
            │   ├── Room.java
            │   ├── Allocation.java
            │   ├── CheckInOut.java
            │   └── FeePayment.java
            ├── service/
            │   ├── HostelService.java (Interface)
            │   └── HostelServiceImpl.java
            └── thread/
                ├── OccupancyReportWorker.java (Runnable)
                └── FeeAuditWorker.java (Thread)
```

---

### 4. Critical Business Logic: Preventing Over-Allocation

The core functional requirement (FR-3) states: *Allocate available rooms to students and prevent allocations beyond room capacity.*

In `HostelServiceImpl.java`, the `allocateRoom` method enforces this via atomic checks:

```java
public synchronized Allocation allocateRoom(int studentId, int roomId) throws HostelException {
    Student student = getStudent(studentId);
    Room room = getRoom(roomId);

    // Rule 1: Prevent duplicate active allocation
    boolean hasActive = allocations.values().stream()
            .anyMatch(a -> a.getStudentId() == studentId && a.isActive());
    if (hasActive) {
        throw new StudentAlreadyAllocatedException(studentId);
    }

    // Rule 2: Prevent allocation beyond room capacity
    if (room.isFull() || room.availableBeds() <= 0) {
        throw new RoomCapacityExceededException(room.getRoomId(), room.getRoomNumber(), room.getCapacity());
    }

    // Rule 3: Commit allocation and increment room occupancy atomically
    Allocation alloc = new Allocation(nextAllocationId++, studentId, roomId, LocalDate.now(), "ALLOCATED");
    allocations.put(alloc.getAllocationId(), alloc);
    room.updateOccupancy(1);

    return alloc;
}
```

If an administrator tries to assign a student to a room where $occupancy \ge capacity$, the system immediately aborts the operation and throws `RoomCapacityExceededException`, protecting the hostel invariants.

---

### 5. Stream API & Lambda Expressions

Stream operations are used to compute complex hostel statistics without verbose loops:

- **Filtering Available Rooms:**
  ```java
  List<Room> available = rooms.values().stream()
      .filter(r -> r.availableBeds() > 0)
      .sorted(Comparator.comparing(Room::getRoomNumber))
      .collect(Collectors.toList());
  ```
- **Grouping Students by Department:**
  ```java
  Map<String, Long> deptDistribution = students.values().stream()
      .collect(Collectors.groupingBy(Student::getDepartment, Collectors.counting()));
  ```
- **Financial Aggregation:**
  ```java
  double totalRevenue = feePayments.values().stream()
      .mapToDouble(FeePayment::getPaidAmount)
      .sum();
  ```

---

### 6. Multithreaded Concurrent Execution Model

To demonstrate Unit 3 multithreading:
1. **`OccupancyReportWorker` (implements `Runnable`):** Computes average room utilization metrics in the background.
2. **`FeeAuditWorker` (extends `Thread`):** Calculates outstanding dues and flags defaulters concurrently.
3. Both threads run asynchronously and are joined in `Main.java` before generating final reports.

---

### 7. Compilation and Execution Guide

- **Double-Clickable Execution:** Simply double-click `run_java.bat` in the `3_java_programming` folder.
- **Manual Command Line:**
  ```cmd
  cd D:\HostelManagementSystem\3_java_programming
  javac -d bin src/com/hostel/model/*.java src/com/hostel/exception/*.java src/com/hostel/service/*.java src/com/hostel/thread/*.java src/com/hostel/Main.java
  java -cp bin com.hostel.Main
  ```
