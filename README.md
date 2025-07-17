# Golden Valley Software – Meal Break Compliance Evaluation

## California Meal Break Law Overview

Under **California Labor Code § 512(a)** and applicable **Wage Orders**:

- An employer **may not employ any employee** for a work period of **more than five (5) hours** per day **without providing a 30-minute unpaid, duty-free meal period**.
- The **meal break must begin before the end of the fifth hour** of work.  
  ⤷ In practice, this means **the lunch break must begin no later than 4 hours and 59 minutes after clock-in**.

**Example:**  
If an employee clocks in at **8:00 AM**, their lunch must begin **by 12:59:59 PM** to comply.

### Waiver Clause – California Labor Code § 512 and Wage Orders

A **first meal period** may be waived under the following conditions:

- The employee's **total shift duration is no more than six (6) hours**  
- The **meal period is waived voluntarily** by mutual agreement between employer and employee  
- The waiver is **signed and retained** for audit or legal review

**Key compliance detail:**  
With a valid waiver in place, the employee is **not required to begin the meal period before the end of the fifth hour**. Instead, the lunch (if taken) may begin **any time up to the end of the sixth hour** (i.e., no later than 5 hours and 59 minutes after clock-in).

If no waiver exists, a meal period must start **no later than the end of the fifth hour** of work.

In all cases, if a lunch is taken, it must be **30 minutes long, unpaid, and duty-free**.

---

This compliance evaluation software uses these standards to detect:
- On-time lunches
- Late lunches without waiver
- Late lunches with waiver (allowed, but tracked)
- Missed lunches

These outputs are compiled monthly and year-to-date to aid HR policy reviews and proactive compliance.

## Project Summary

This project delivers a fully automated **Python-based compliance pipeline** that evaluates adherence to California's meal break law (Labor Code § 512). It is designed to scale across months, ensuring consistent monitoring and risk detection for HR and operations teams.

The pipeline performs the following steps end-to-end:

1. **Ingest** raw monthly timecard data (`.csv`)
2. **Clean** the dataset to ensure structural integrity and filter out unusable rows
3. **Detect violations** based on lunch timing and waiver status, using encoded business logic aligned with California law
4. **Generate reports** that summarize valid shifts, violations, and their breakdown by type
5. **Compile year-to-date (YTD) summaries** automatically as each new month's data is processed

This is a **turnkey solution**: once raw data is dropped into the folder, the pipeline handles everything from compliance checks to summary reporting **no manual intervention required**.


### Current Findings – Golden Valley Software

![Violation Summary](report_viz/year_to_date_line_graph.png)

- **40.7%** of employee shifts have resulted in a violation of Labor Code § 512(a).  
- **Figure 1:** Violation rate by month  
- **Figure 2:** Violation breakdown by type  

**Violation Breakdown:**
![Violation Summary](report_viz/violation_distribution.png)

These results indicate that Golden Valley Software may be exposed to **significant litigation risk** if compliance is not addressed.

### Future Enhancements

Planned improvements include:

- Weekly and daily trend analysis  
- Employee-level violation frequency  
- Interactive dashboards with Tableau  

