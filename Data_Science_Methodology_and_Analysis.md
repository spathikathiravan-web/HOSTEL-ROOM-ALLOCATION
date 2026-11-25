# Data Science Methodology and Statistical Analysis
## Hostel Room Allocation and Student Accommodation Analysis System

**Course Code:** 25ITC31 – Foundations of Data Science  
**Deliverable Category:** 4. Foundation of Data Science  

---

### Table of Contents
1. [Data Science Workflow and Roadmap](#1-data-science-workflow-and-roadmap)
2. [Data Description and Attribute Classifications (Unit 1)](#2-data-description-and-attribute-classifications-unit-1)
3. [Descriptive Statistics and Distribution Analysis (Unit 1)](#3-descriptive-statistics-and-distribution-analysis-unit-1)
4. [Data Wrangling and Vectorized Operations (Unit 3)](#4-data-wrangling-and-vectorized-operations-unit-3)
5. [Data Cleaning, Imputation & Feature Engineering (Unit 4)](#5-data-cleaning-imputation--feature-engineering-unit-4)
6. [Exploratory Data Analysis (EDA) & 7 Visual Charts (Unit 5)](#6-exploratory-data-analysis-eda--7-visual-charts-unit-5)
   - 6.1 Chart 1: Bed Capacity vs. Current Occupancy
   - 6.2 Chart 2: Overall Hostel Bed Occupancy Rate (Donut Chart)
   - 6.3 Chart 3: Department-wise Accommodation Distribution
   - 6.4 Chart 4: Fee Collection vs. Outstanding Arrears
   - 6.5 Chart 5: Fee Dispersion Across Years of Study (Box Plot)
   - 6.6 Chart 6: Longitudinal Check-in / Check-out Timeline
   - 6.7 Chart 7: Correlation Heatmap
7. [Execution Instructions](#7-execution-instructions)

---

### 1. Data Science Workflow and Roadmap

The analysis follows the standard **Data Science Lifecycle**:
1. **Business Understanding:** Optimize bed allocation, identify vacant capacities, and reduce fee arrears.
2. **Data Acquisition:** Automated SQL extraction from the relational DBMS (`hostel_database.db`) joined across `student`, `room`, `allocation`, `check_in_out`, and `fee_payment`.
3. **Data Preprocessing & Cleaning:** Handling null values for unassigned students, casting data types, and detecting duplicates.
4. **Feature Engineering:** Creating ratio indicators (`occupancy_rate_pct`, `available_beds`, `fee_clearance_ratio`).
5. **Statistical Modeling:** Central tendency, dispersion, quartiles, IQR, and Z-score outlier detection.
6. **Data Visualization:** Rendering 7 publication-quality visual plots.

---

### 2. Data Description and Attribute Classifications (Unit 1)

| Attribute Name | Data Type | Measurement Scale | Description & Invariant |
| :--- | :--- | :--- | :--- |
| `student_id` | Integer | Nominal (Identifier) | Unique institutional identifier for each hosteller. |
| `student_name` | String | Nominal | Full name of the student. |
| `department` | String | Nominal (Categorical) | Academic department (`CSE`, `IT`, `ECE`, `MECH`, `AIDS`). |
| `year_of_study` | Integer | Ordinal ($1 \le y \le 4$) | Current academic year of study. |
| `room_number` | String | Nominal (Identifier) | Unique room designation (e.g. `A-101`, `B-201`). |
| `room_type` | String | Nominal (Categorical) | Room tier (`Single AC`, `Double Non-AC`, `Triple Non-AC`). |
| `capacity` | Integer | Ratio ($1 \le c \le 5$) | Maximum bed slots physically available in room. |
| `occupancy` | Integer | Ratio ($0 \le o \le c$) | Number of students actively residing in room. |
| `total_fee` | Float | Ratio ($\ge 0$) | Total semester hostel fee dues (in INR ₹). |
| `paid_amount` | Float | Ratio ($\ge 0$) | Sum of fee installments collected to date. |
| `pending_amount`| Float | Ratio ($\ge 0$) | Outstanding uncollected arrears ($total - paid$). |
| `payment_status`| String | Nominal | Payment state (`PAID`, `PARTIAL`, `PENDING`). |

---

### 3. Descriptive Statistics and Distribution Analysis (Unit 1)

Summary descriptive metrics calculated across $N=15$ hostellers:

| Feature | Mean ($\bar{x}$) | Median ($M$) | Std Dev ($s$) | Variance ($s^2$) | Min | Max | IQR ($Q_3 - Q_1$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **year_of_study** | 2.47 | 2.00 | 1.06 | 1.12 | 1.0 | 4.0 | 1.00 |
| **capacity** | 1.80 | 2.00 | 1.15 | 1.31 | 0.0 | 3.0 | 2.00 |
| **occupancy** | 1.60 | 2.00 | 1.06 | 1.11 | 0.0 | 3.0 | 1.00 |
| **total_fee** | ₹45,000.00 | ₹45,000.00 | ₹11,338.93 | 128,571,428.57 | ₹35,000.0 | ₹65,000.0 | ₹10,000.00 |
| **paid_amount** | ₹33,333.33 | ₹35,000.00 | ₹20,412.41 | 416,666,666.67 | ₹0.0 | ₹65,000.0 | ₹27,500.00 |
| **pending_amount**| ₹11,666.67 | ₹0.00 | ₹13,972.76 | 195,238,095.24 | ₹0.0 | ₹35,000.0 | ₹20,000.00 |

#### Outlier Detection via Standard Z-Scores
A data point $x_i$ is classified as a statistical outlier if its standard score satisfies:
$$|z_i| = \left|\frac{x_i - \bar{x}}{s}\right| > 2.0$$
- Result: Both `total_fee` and `pending_amount` have zero points beyond $|z| > 2.0$, confirming a balanced and realistic distribution without aberrant anomalies.

---

### 4. Data Wrangling and Vectorized Operations (Unit 3)

Using NumPy vectorized operations:
- **Mean Capacity & Occupancy by Room Type:**
  - `Single AC`: Mean Capacity = 1.00 beds, Mean Occupancy = 1.00 beds (100% full).
  - `Double Non-AC`: Mean Capacity = 2.00 beds, Mean Occupancy = 1.80 beds (90% full).
  - `Triple Non-AC`: Mean Capacity = 3.00 beds, Mean Occupancy = 2.60 beds (86.7% full).

---

### 5. Data Cleaning, Imputation & Feature Engineering (Unit 4)

1. **Handling Missing Values:**
   - Unallocated students (e.g., student 115) had missing room attributes, imputed with `capacity = 0`, `occupancy = 0`, and `room_type = 'Unassigned'`.
2. **Feature Engineering:**
   - **`available_beds`**:
     $$\text{available\_beds} = \max(0, \text{capacity} - \text{occupancy})$$
   - **`occupancy_rate_pct`**:
     $$\text{occupancy\_rate\_pct} = \frac{\text{occupancy}}{\text{capacity}} \times 100\%$$
   - **`fee_clearance_ratio`**:
     $$\text{fee\_clearance\_ratio} = \frac{\text{paid\_amount}}{\text{total\_fee}}$$

---

### 6. Exploratory Data Analysis (EDA) & 7 Visual Charts (Unit 5)

All 7 publication-quality visual plots have been generated and saved into the `visualizations/` folder.

#### 6.1 Chart 1: Bed Capacity vs. Current Occupancy
- **File Link:** [1_room_occupancy_by_type.png](file:///D:/HostelManagementSystem/4_foundation_of_data_science/visualizations/1_room_occupancy_by_type.png)
- **Description:** Grouped bar chart comparing total bed inventory versus occupied beds across `Single AC` (3/3), `Double Non-AC` (5/8), and `Triple Non-AC` (5/9).

#### 6.2 Chart 2: Overall Hostel Bed Occupancy Rate (Donut Chart)
- **File Link:** [2_hostel_occupancy_donut.png](file:///D:/HostelManagementSystem/4_foundation_of_data_science/visualizations/2_hostel_occupancy_donut.png)
- **Description:** Donut chart illustrating total hostel bed utilization: 13 occupied beds (65.0%) vs. 7 vacant beds (35.0%) out of 20 total beds.

#### 6.3 Chart 3: Department-wise Accommodation Distribution
- **File Link:** [3_department_wise_distribution.png](file:///D:/HostelManagementSystem/4_foundation_of_data_science/visualizations/3_department_wise_distribution.png)
- **Description:** Bar chart showing enrolled hosteller counts across engineering disciplines: CSE (4 students, 27%), ECE (3 students, 20%), MECH (3 students, 20%), IT (3 students, 20%), AIDS (2 students, 13%).

#### 6.4 Chart 4: Fee Collection vs. Outstanding Arrears
- **File Link:** [4_fee_collection_status.png](file:///D:/HostelManagementSystem/4_foundation_of_data_science/visualizations/4_fee_collection_status.png)
- **Description:** Financial audit bar chart: Total Billed = ₹675,000 (100%), Total Collected = ₹500,000 (74.1%), Total Outstanding Arrears = ₹175,000 (25.9%).

#### 6.5 Chart 5: Fee Dispersion Across Years of Study (Box Plot)
- **File Link:** [5_fee_distribution_by_year.png](file:///D:/HostelManagementSystem/4_foundation_of_data_science/visualizations/5_fee_distribution_by_year.png)
- **Description:** Five-number summary box plot depicting medians, quartiles, and spreads of fees paid by students in 1st, 2nd, 3rd, and 4th year cohorts.

#### 6.6 Chart 6: Longitudinal Check-in / Check-out Timeline
- **File Link:** [6_monthly_checkin_checkout_trend.png](file:///D:/HostelManagementSystem/4_foundation_of_data_science/visualizations/6_monthly_checkin_checkout_trend.png)
- **Description:** Time series line chart displaying student arrivals and departures across calendar months, highlighting semester intake peaks.

#### 6.7 Chart 7: Correlation Heatmap
- **File Link:** [7_correlation_heatmap.png](file:///D:/HostelManagementSystem/4_foundation_of_data_science/visualizations/7_correlation_heatmap.png)
- **Description:** Annotated correlation matrix revealing strong positive correlation between `capacity` and `occupancy` ($r = 0.94$), and moderate correlation between `total_fee` and `paid_amount` ($r = 0.65$).

---

### 7. Execution Instructions

- **Run via Runnable Batch File:** Simply double-click `run_data_science.bat` in the `4_foundation_of_data_science` folder.
- **Run via Python Command Line:**
  ```cmd
  cd D:\HostelManagementSystem\4_foundation_of_data_science
  D:\python_env\Scripts\python.exe hostel_data_analysis.py
  ```
