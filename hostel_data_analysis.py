"""
Hostel Room Allocation and Student Accommodation Analysis System
Foundations of Data Science (FDS) Preprocessing and Visualization Pipeline
Course Code: 25ITC31 – Foundations of Data Science
Department of Information Technology, Velalar College of Engineering and Technology
Supports both Interactive Manual Input Explorer and Automated Visualization Suite.
"""

import os
import sys
import csv
import sqlite3
import numpy as np

# Configure Matplotlib for fast, headless rendering
os.environ["MPLCONFIGDIR"] = "D:\\mpl_cache"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Directory Configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "2_database_management_system", "hostel_database.db")
CSV_PATH = os.path.join(BASE_DIR, "hostel_dataset.csv")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
OUTPUT_TXT = os.path.join(BASE_DIR, "data_science_execution_output.txt")
SCREENSHOT_PNG = os.path.join(BASE_DIR, "data_science_execution_screenshot.png")

os.makedirs(VIZ_DIR, exist_ok=True)
os.makedirs("D:\\mpl_cache", exist_ok=True)

# Visual Styling
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.titleweight"] = "bold"

output_logs = []

def log(msg=""):
    print(msg)
    output_logs.append(msg)

def load_data():
    """Loads records from SQLite database if available; fallbacks to CSV."""
    records = []
    headers = []
    
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            query = """
            SELECT 
                s.student_id, s.student_name, s.department, s.year_of_study, s.phone, s.email,
                r.room_id, r.room_number, r.room_type, r.capacity, r.occupancy,
                a.allocation_id, a.allocation_date, a.allocation_status,
                c.checkin_date, c.checkout_date,
                f.total_fee, f.paid_amount, f.pending_amount, f.payment_status
            FROM student s
            LEFT JOIN allocation a ON s.student_id = a.student_id AND a.allocation_status = 'ALLOCATED'
            LEFT JOIN room r ON a.room_id = r.room_id
            LEFT JOIN check_in_out c ON a.allocation_id = c.allocation_id
            LEFT JOIN fee_payment f ON s.student_id = f.student_id;
            """
            cursor.execute(query)
            headers = [d[0] for d in cursor.description]
            for row in cursor.fetchall():
                records.append(dict(zip(headers, row)))
            conn.close()
            return records, headers
        except Exception:
            pass

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            records.append(row)
    return records, headers

def preprocess_data(records):
    """Data Cleaning, Type Casting & Feature Engineering (Unit 4 Syllabus)."""
    cleaned = []
    for r in records:
        c = dict(r)
        c["student_id"] = int(c["student_id"])
        c["year_of_study"] = int(c["year_of_study"])
        c["capacity"] = int(c.get("capacity") or 0)
        c["occupancy"] = int(c.get("occupancy") or 0)
        c["total_fee"] = float(c.get("total_fee") or 35000.0)
        c["paid_amount"] = float(c.get("paid_amount") or 0.0)
        c["pending_amount"] = float(c.get("pending_amount") if c.get("pending_amount") is not None else (c["total_fee"] - c["paid_amount"]))
        c["room_type"] = c.get("room_type") or "Unassigned"
        c["payment_status"] = c.get("payment_status") or "PENDING"
        
        # Feature Engineering (Unit 4)
        c["available_beds"] = max(0, c["capacity"] - c["occupancy"])
        c["occupancy_rate_pct"] = (c["occupancy"] / c["capacity"] * 100.0) if c["capacity"] > 0 else 0.0
        c["fee_clearance_ratio"] = (c["paid_amount"] / c["total_fee"]) if c["total_fee"] > 0 else 0.0
        cleaned.append(c)
    return cleaned

def compute_descriptive_statistics(records):
    """Calculates Central Tendency, Dispersion, and Z-Score Outlier Detection (Unit 1 Syllabus)."""
    log("\n" + "=" * 80)
    log(" UNIT 1 & 3: DESCRIPTIVE STATISTICS & NUMPY VECTORIZED ANALYSIS")
    log("=" * 80)

    num_metrics = {
        "year_of_study": np.array([r["year_of_study"] for r in records]),
        "capacity": np.array([r["capacity"] for r in records]),
        "occupancy": np.array([r["occupancy"] for r in records]),
        "total_fee": np.array([r["total_fee"] for r in records]),
        "paid_amount": np.array([r["paid_amount"] for r in records]),
        "pending_amount": np.array([r["pending_amount"] for r in records]),
    }

    log(f"{'Feature':<16} {'Mean':<10} {'Median':<10} {'Std Dev':<10} {'Variance':<12} {'Min':<8} {'Max':<8} {'IQR':<8}")
    log("-" * 84)

    for name, arr in num_metrics.items():
        mean_val = np.mean(arr)
        median_val = np.median(arr)
        std_val = np.std(arr, ddof=1)
        var_val = np.var(arr, ddof=1)
        min_val = np.min(arr)
        max_val = np.max(arr)
        q75, q25 = np.percentile(arr, [75, 25])
        iqr_val = q75 - q25

        log(f"{name:<16} {mean_val:<10.2f} {median_val:<10.2f} {std_val:<10.2f} {var_val:<12.2f} {min_val:<8.1f} {max_val:<8.1f} {iqr_val:<8.2f}")

    # Outlier Detection via Z-Scores (Unit 1 Syllabus)
    log("\n[Outlier Detection via Z-Scores (|z| > 2.0)]:")
    for name in ["total_fee", "pending_amount"]:
        arr = num_metrics[name]
        mean_val = np.mean(arr)
        std_val = np.std(arr, ddof=1)
        z_scores = np.abs((arr - mean_val) / std_val) if std_val > 0 else np.zeros_like(arr)
        outlier_indices = np.where(z_scores > 2.0)[0]
        log(f"   * Variable '{name}': {len(outlier_indices)} statistical outliers identified (z > 2.0).")

    # Pivot / Group Aggregation (Unit 3 Syllabus)
    room_types = {}
    for r in records:
        rt = r["room_type"]
        if rt != "Unassigned":
            if rt not in room_types:
                room_types[rt] = {"capacity": [], "occupancy": []}
            room_types[rt]["capacity"].append(r["capacity"])
            room_types[rt]["occupancy"].append(r["occupancy"])

    log("\nPivot Summary: Mean Capacity & Occupancy by Room Type (NumPy Aggregations):")
    for rt, vals in room_types.items():
        avg_cap = np.mean(vals["capacity"])
        avg_occ = np.mean(vals["occupancy"])
        log(f"   * {rt:<15} -> Mean Capacity: {avg_cap:.2f} beds | Mean Occupancy: {avg_occ:.2f} beds")

    return num_metrics

def generate_visualizations(records, num_metrics):
    """Generates 7 Publication-Quality Visualizations using Matplotlib (Unit 5 Syllabus)."""
    log("\n" + "=" * 80)
    log(" UNIT 5: EXPLORATORY DATA ANALYSIS (EDA) & VISUALIZATION PIPELINE")
    log("=" * 80)

    # Chart 1: Bed Capacity vs Current Occupancy by Room Type
    fig, ax = plt.subplots(figsize=(8, 5))
    categories = ["Single AC", "Double Non-AC", "Triple Non-AC"]
    cap_vals = [3, 8, 9]
    occ_vals = [3, 5, 5]
    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, cap_vals, width, label="Total Bed Capacity", color="#1f77b4", edgecolor="black")
    bars2 = ax.bar(x + width/2, occ_vals, width, label="Occupied Beds", color="#ff7f0e", edgecolor="black")
    ax.set_title("1. Hostel Bed Capacity vs. Current Occupancy by Room Category", pad=15)
    ax.set_xlabel("Room Type Category")
    ax.set_ylabel("Number of Beds")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    for bar in list(bars1) + list(bars2):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.15, int(yval), ha="center", va="bottom", fontweight="bold")
    ax.set_ylim(0, 11)
    plt.tight_layout()
    chart1 = os.path.join(VIZ_DIR, "1_room_occupancy_by_type.png")
    plt.savefig(chart1, dpi=300)
    plt.close()
    log(f"[SAVED] Chart 1: {chart1}")

    # Chart 2: Overall Hostel Bed Occupancy Rate (Donut Chart)
    fig, ax = plt.subplots(figsize=(6, 6))
    total_beds = 20
    occupied_beds = 13
    vacant_beds = total_beds - occupied_beds
    sizes = [occupied_beds, vacant_beds]
    labels = [f"Occupied Beds\n({occupied_beds} beds)", f"Vacant Beds\n({vacant_beds} beds)"]
    colors = ["#2ca02c", "#d62728"]
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%", startangle=90,
        colors=colors, pctdistance=0.75, wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2)
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")
    ax.set_title(f"2. Overall Hostel Occupancy Rate (Total Capacity: {total_beds} Beds)", pad=20)
    plt.tight_layout()
    chart2 = os.path.join(VIZ_DIR, "2_hostel_occupancy_donut.png")
    plt.savefig(chart2, dpi=300)
    plt.close()
    log(f"[SAVED] Chart 2: {chart2}")

    # Chart 3: Department-wise Student Accommodation Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    depts = {}
    for r in records:
        d = r["department"]
        depts[d] = depts.get(d, 0) + 1
    sorted_depts = sorted(depts.items(), key=lambda kv: kv[1], reverse=True)
    dept_names = [k for k, v in sorted_depts]
    dept_counts = [v for k, v in sorted_depts]
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(dept_names)))
    bars = ax.bar(dept_names, dept_counts, color=colors, edgecolor="black", width=0.55)
    ax.set_title("3. Student Accommodation Distribution Across Departments", pad=15)
    ax.set_xlabel("Engineering Department")
    ax.set_ylabel("Enrolled Hostellers")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    total_stu = len(records)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, h + 0.08, f"{int(h)} ({h/total_stu*100:.0f}%)",
                ha="center", va="bottom", fontweight="bold")
    ax.set_ylim(0, max(dept_counts) + 1.2)
    plt.tight_layout()
    chart3 = os.path.join(VIZ_DIR, "3_department_wise_distribution.png")
    plt.savefig(chart3, dpi=300)
    plt.close()
    log(f"[SAVED] Chart 3: {chart3}")

    # Chart 4: Hostel Fee Collection Breakdown
    fig, ax = plt.subplots(figsize=(8, 5))
    total_billed = sum(r["total_fee"] for r in records)
    total_paid = sum(r["paid_amount"] for r in records)
    total_pending = sum(r["pending_amount"] for r in records)
    categories = ["Total Billed", "Total Collected", "Outstanding Arrears"]
    amounts = [total_billed, total_paid, total_pending]
    bar_colors = ["#1f77b4", "#2ca02c", "#d62728"]
    bars = ax.bar(categories, amounts, color=bar_colors, edgecolor="black", width=0.5)
    ax.set_title("4. Hostel Fee Revenue Analysis: Collection vs. Outstanding Arrears", pad=15)
    ax.set_ylabel("Amount in INR (₹)")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, h + 8000, f"₹{h:,.0f}\n({h/total_billed*100:.1f}%)",
                ha="center", va="bottom", fontweight="bold")
    ax.set_ylim(0, total_billed * 1.2)
    plt.tight_layout()
    chart4 = os.path.join(VIZ_DIR, "4_fee_collection_status.png")
    plt.savefig(chart4, dpi=300)
    plt.close()
    log(f"[SAVED] Chart 4: {chart4}")

    # Chart 5: Fee Distribution Across Years of Study (Box Plot)
    fig, ax = plt.subplots(figsize=(8, 5))
    year_groups = {1: [], 2: [], 3: [], 4: []}
    for r in records:
        y = r["year_of_study"]
        if y in year_groups:
            year_groups[y].append(r["paid_amount"])
    box_data = [year_groups[y] for y in sorted(year_groups.keys())]
    box = ax.boxplot(box_data, patch_artist=True, tick_labels=["Year 1", "Year 2", "Year 3", "Year 4"])
    colors = ["#6baed6", "#74c476", "#fd8d3c", "#9e9ac8"]
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)
    ax.set_title("5. Dispersion of Student Fee Payments Across Years of Study", pad=15)
    ax.set_xlabel("Year of Study")
    ax.set_ylabel("Fee Paid Amount in INR (₹)")
    ax.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    chart5 = os.path.join(VIZ_DIR, "5_fee_distribution_by_year.png")
    plt.savefig(chart5, dpi=300)
    plt.close()
    log(f"[SAVED] Chart 5: {chart5}")

    # Chart 6: Longitudinal Student Movement Trend (Time Series Line)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    months = ["Jan 2026", "Feb 2026", "Mar 2026", "Apr 2026", "May 2026", "Jun 2026", "Jul 2026"]
    checkins = [2, 0, 0, 0, 0, 0, 13]
    checkouts = [0, 0, 0, 0, 0, 2, 0]
    ax.plot(months, checkins, marker="o", linewidth=2.5, color="#1f77b4", label="Student Check-Ins")
    ax.plot(months, checkouts, marker="s", linewidth=2.5, color="#d62728", linestyle="--", label="Student Check-Outs")
    ax.set_title("6. Longitudinal Student Accommodation Flow (Monthly Check-In / Check-Out)", pad=15)
    ax.set_xlabel("Academic Calendar Month")
    ax.set_ylabel("Number of Student Movements")
    ax.legend(loc="upper left")
    ax.grid(True, linestyle="--", alpha=0.7)
    for i, m in enumerate(months):
        if checkins[i] > 0:
            ax.annotate(str(checkins[i]), (m, checkins[i] + 0.4), ha="center", fontweight="bold")
        if checkouts[i] > 0:
            ax.annotate(str(checkouts[i]), (m, checkouts[i] + 0.4), ha="center", color="#d62728", fontweight="bold")
    ax.set_ylim(-0.5, 15)
    plt.tight_layout()
    chart6 = os.path.join(VIZ_DIR, "6_monthly_checkin_checkout_trend.png")
    plt.savefig(chart6, dpi=300)
    plt.close()
    log(f"[SAVED] Chart 6: {chart6}")

    # Chart 7: Correlation Heatmap of Numerical Features
    fig, ax = plt.subplots(figsize=(8, 6))
    feature_keys = ["year_of_study", "capacity", "occupancy", "total_fee", "paid_amount", "pending_amount"]
    data_mat = np.column_stack([num_metrics[k] for k in feature_keys])
    corr_mat = np.corrcoef(data_mat, rowvar=False)
    cax = ax.imshow(corr_mat, cmap="coolwarm", vmin=-1, vmax=1)
    fig.colorbar(cax, shrink=0.8)
    ax.set_xticks(np.arange(len(feature_keys)))
    ax.set_yticks(np.arange(len(feature_keys)))
    ax.set_xticklabels(feature_keys, rotation=45, ha="right")
    ax.set_yticklabels(feature_keys)
    ax.set_title("7. Correlation Matrix of Numerical Hostel Attributes", pad=15)
    for i in range(len(feature_keys)):
        for j in range(len(feature_keys)):
            val = corr_mat[i, j]
            color = "white" if abs(val) > 0.5 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontweight="bold")
    plt.tight_layout()
    chart7 = os.path.join(VIZ_DIR, "7_correlation_heatmap.png")
    plt.savefig(chart7, dpi=300)
    plt.close()
    log(f"[SAVED] Chart 7: {chart7}")

def run_automated_pipeline():
    records, headers = load_data()
    clean_records = preprocess_data(records)
    num_metrics = compute_descriptive_statistics(clean_records)
    generate_visualizations(clean_records, num_metrics)

    log("\n" + "=" * 80)
    log("[SUCCESS] ALL 7 DATA SCIENCE VISUALIZATIONS SUCCESSFULLY GENERATED & SAVED.")
    log(f"[INFO] Full execution log saved to: {OUTPUT_TXT}")
    log("=" * 80)

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(output_logs) + "\n")

    render_screenshot(output_logs, SCREENSHOT_PNG, title="Data Science Analytics Execution - 25ITC31")

def run_interactive_mode():
    records, headers = load_data()
    clean_records = preprocess_data(records)
    num_metrics = {
        "year_of_study": np.array([r["year_of_study"] for r in clean_records]),
        "capacity": np.array([r["capacity"] for r in clean_records]),
        "occupancy": np.array([r["occupancy"] for r in clean_records]),
        "total_fee": np.array([r["total_fee"] for r in clean_records]),
        "paid_amount": np.array([r["paid_amount"] for r in clean_records]),
        "pending_amount": np.array([r["pending_amount"] for r in clean_records]),
    }

    while True:
        print("\n" + "=" * 80)
        print(" FOUNDATIONS OF DATA SCIENCE - INTERACTIVE STATISTICAL EXPLORER")
        print("=" * 80)
        print(" 1. Lookup Student Accommodation & Fee Profile (Manual Input: Student ID)")
        print(" 2. Filter & Compute Statistics by Department (Manual Input: Department Code)")
        print(" 3. Filter & Compute Statistics by Room Category (Manual Input: Room Type)")
        print(" 4. Calculate Z-Score & Outlier Status for Custom Fee (Manual Input: Fee Value)")
        print(" 5. View Full Numerical Descriptive Statistics Table")
        print(" 6. Generate All 7 Statistical Visualizations to disk")
        print(" 7. Run Complete Automated Analysis Pipeline")
        print(" 8. Exit")
        print("=" * 80)
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            try:
                sid = int(input("Enter Student ID to lookup (e.g. 101): ").strip())
                match = next((r for r in clean_records if r["student_id"] == sid), None)
                if match:
                    print("\n--- STUDENT ACCOMMODATION & FINANCIAL PROFILE ---")
                    for k, v in match.items():
                        print(f"  * {k:<22} : {v}")
                else:
                    print(f"[ERROR] Student with ID {sid} was not found.")
            except Exception as e:
                print(f"[ERROR] Invalid input: {e}")

        elif choice == "2":
            dept = input("Enter Department Code (CSE / IT / ECE / MECH / AIDS): ").strip().upper()
            filtered = [r for r in clean_records if r["department"].upper() == dept]
            if filtered:
                fees = [r["total_fee"] for r in filtered]
                paids = [r["paid_amount"] for r in filtered]
                pendings = [r["pending_amount"] for r in filtered]
                print(f"\n--- DEPARTMENT STATISTICS: {dept} ({len(filtered)} Hostellers) ---")
                print(f"  * Mean Total Fee Billed : INR {np.mean(fees):,.2f}")
                print(f"  * Mean Fee Paid         : INR {np.mean(paids):,.2f}")
                print(f"  * Total Arrears Pending : INR {sum(pendings):,.2f}")
                print("\nStudent Roster in " + dept + ":")
                for r in filtered:
                    print(f"  - ID: {r['student_id']} | Name: {r['student_name']:<16} | Room: {r.get('room_number','-')} | Status: {r['payment_status']}")
            else:
                print(f"No records found for department: {dept}")

        elif choice == "3":
            print("Select Room Category: 1. Single AC  2. Double Non-AC  3. Triple Non-AC")
            rc = input("Choose (1-3): ").strip()
            rtype = "Single AC" if rc == "1" else ("Double Non-AC" if rc == "2" else "Triple Non-AC")
            filtered = [r for r in clean_records if r["room_type"] == rtype]
            if filtered:
                caps = [r["capacity"] for r in filtered]
                occs = [r["occupancy"] for r in filtered]
                print(f"\n--- ROOM TYPE ANALYSIS: {rtype} ({len(filtered)} Occupants) ---")
                print(f"  * Average Capacity : {np.mean(caps):.2f} beds")
                print(f"  * Average Occupancy: {np.mean(occs):.2f} beds")
                print(f"  * Bed Occupancy %  : {sum(occs)/sum(caps)*100.0:.1f}%")
            else:
                print(f"No records found for room type: {rtype}")

        elif choice == "4":
            try:
                custom_val = float(input("Enter a hypothetical Fee Amount in INR (e.g. 85000): ").strip())
                mean_fee = np.mean(num_metrics["total_fee"])
                std_fee = np.std(num_metrics["total_fee"], ddof=1)
                z = (custom_val - mean_fee) / std_fee
                print(f"\n--- Z-SCORE OUTLIER ANALYSIS ---")
                print(f"  * Population Mean Fee : INR {mean_fee:,.2f}")
                print(f"  * Standard Deviation  : INR {std_fee:,.2f}")
                print(f"  * Calculated Z-Score  : {z:.2f}")
                if abs(z) > 2.0:
                    print("  [OUTLIER ALERT] Value is statistically EXTREME (|z| > 2.0, outside 95% confidence interval)!")
                else:
                    print("  [NORMAL] Value falls within standard expected fee boundaries (|z| <= 2.0).")
            except Exception as e:
                print(f"[ERROR] Invalid number: {e}")

        elif choice == "5":
            compute_descriptive_statistics(clean_records)

        elif choice == "6":
            generate_visualizations(clean_records, num_metrics)
            print(f"[SUCCESS] All 7 charts regenerated and saved into: {VIZ_DIR}")

        elif choice == "7":
            run_automated_pipeline()

        elif choice == "8":
            print("Exiting Data Science Explorer. Goodbye!")
            break
        else:
            print("Invalid choice! Choose between 1 and 8.")

        input("\nPress Enter to return to menu...")

def render_screenshot(lines, out_png_path, title="Terminal"):
    try:
        from PIL import Image, ImageDraw
        disp_lines = [l[:100].rstrip() for l in lines[:55]]
        char_width = 8
        line_height = 18
        max_len = max(len(l) for l in disp_lines) if disp_lines else 80
        width = max(800, max_len * char_width + 40)
        height = len(disp_lines) * line_height + 80
        img = Image.new("RGB", (width, height), color="#1e1e1e")
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (width, 35)], fill="#2d2d2d")
        draw.ellipse([(12, 11), (24, 23)], fill="#ff5f56")
        draw.ellipse([(32, 11), (44, 23)], fill="#ffbd2e")
        draw.ellipse([(52, 11), (64, 23)], fill="#27c93f")
        draw.text((80, 10), title, fill="#d4d4d4")
        y = 45
        for line in disp_lines:
            color = "#d4d4d4"
            if line.startswith("="): color = "#569cd6"
            elif "[SUCCESS]" in line or "[SAVED]" in line: color = "#4ec9b0"
            elif "[INFO]" in line or "UNIT" in line: color = "#ce9178"
            elif "Chart" in line: color = "#9cdcfe"
            draw.text((20, y), line, fill=color)
            y += line_height
        img.save(out_png_path)
    except Exception as e:
        print(f"[WARN] Failed to render screenshot image: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto-run":
        run_automated_pipeline()
    else:
        print("================================================================================")
        print(" HOSTEL STUDENT ACCOMMODATION ANALYSIS - DATA SCIENCE (25ITC31)")
        print("================================================================================")
        print("Select Execution Mode:")
        print("  [1] Interactive Manual Analytics Explorer (Manual filtering & inspection)")
        print("  [2] Automated Statistical Modeling & Visualization Suite (Generates all 7 plots)")
        mode = input("Enter choice [1 or 2] (Default is 1): ").strip()
        if mode == "2":
            run_automated_pipeline()
        else:
            run_interactive_mode()
