Here's a complete `README.md` file for your **Hotel Booking Case Study Project**, based on the detailed analysis from your report:

---

```markdown
# 🏨 Hotel Booking Case Study - Exploratory Data Analysis (EDA)

## 📌 Project Overview

This project performs a comprehensive **Exploratory Data Analysis (EDA)** on a hotel booking dataset to uncover patterns in guest behavior, pricing strategies, booking dynamics, and operational efficiency. The insights aim to improve revenue strategies and enhance customer satisfaction in the hospitality sector.

---

## 👨‍💻 Author

**Name**: Sahil Karande  
**CDAC ID**: 250240325059

---

## 🎯 Objectives

- Analyze guest booking behavior (lead time, changes, cancellations, etc.).
- Identify factors influencing Average Daily Rate (ADR).
- Explore customer types and their impact on bookings.
- Use statistics and visualizations for actionable insights.

---

## 📂 Dataset Overview

- **Source**: `hotel_bookings.csv`
- **Type**: Structured tabular data
- **Key Features**:
  - Booking details (lead time, ADR, status)
  - Guest info (country, group size, special requests)
  - Stay info (check-in, check-out, nights, cancellations)
  - Customer and market segments

---

## 🔧 Data Preprocessing

- Removed `company` column (94% nulls)
- Filled missing values (`agent`, `children`, `country`)
- Converted data types (e.g., categorical, integers)
- Parsed dates (`arrival_date`, `departure_date`)
- Created derived features:
  - `total_stay_nights`
  - `revenue_generated`
  - `total_members`
- Removed duplicates and visually inspected for outliers

---

## 📊 Exploratory Data Analysis

### 🧍 Univariate Insights
- Most bookings had **short lead times**
- **City Hotels** had twice the bookings vs. Resort Hotels
- **Portugal (PRT)** was the top booking country
- **Monday** had the highest number of arrivals
- ADR was mostly between ₹30–₹100

### 🔄 Bivariate & Multivariate Analysis
- Cancellations higher for early bookings (longer lead times)
- Transient customers booked the most and canceled the most (~30%)
- Room changes occurred in **~15%** of bookings
- Special requests slightly increased ADR and stay duration
- Contract customers stayed the longest (~6 nights)

---

## 🔍 Statistical Tests

1. **ADR by Channel** → No significant difference (p=0.33)
2. **Room Upgrade vs Lead Time** → Significant association (p<0.0001)
3. **Stay Duration by Customer Type** → Significantly different (p<0.0001)

---

## 🌐 Country-Level Insights

- **UK, Ireland, Germany** → Early planners (avg lead time >100 days)
- **Spain, Portugal** → Last-minute bookings (lead time <65 days)
- **Italy, Spain** → Higher ADRs (₹115+)

---

## 📈 Key Business Insights

- Special requests correlate with higher ADR & longer stays
- Transient customers drive most revenue but cancel more
- Booking consistency highest in Corporate & Complementary segments
- Lead time has weak correlation with ADR and booking changes
- 15% room reassignment rate indicates possible overbooking/upselling

---

## 📌 Common Business Questions Answered

| Question | Insight |
|---------|--------|
| What influences ADR? | Mostly special requests; lead time has slight effect |
| Do early bookers make more changes? | Yes, but effect is weak |
| Which countries pay more? | ESP & ITA pay higher ADRs |
| Who cancels more? | Transient customers |
| Who stays longer? | Contract customers |
| Which channel is most consistent? | Corporate & Complementary |
| Who gets upgrades? | Early bookers more likely |

---

## 📅 Conclusion

Booking behavior is heavily influenced by **country**, **customer type**, and **channel**. While most bookings are made within a few weeks of stay, those with more planning often cancel. Revenue and stay duration increase with **special requests**, and transient guests dominate volume but show higher risk for cancellations.

---

## 📎 Technologies Used

- **Python** (Pandas, NumPy, Matplotlib, Seaborn)
- **Jupyter Notebook**
- **Statistical Analysis** (T-Test, Chi-Square, ANOVA)

---

## 📁 File Structure

```

├── data/
│   └── hotel\_bookings.csv
├── notebooks/
│   └── hotel\_booking\_analysis.ipynb
├── README.md
├── Hotel\_Case\_Study\_Report\_Sahil.pdf

```

---

## 📬 Contact

For any queries or collaboration:

📧 Email: [skarande220@gmail.com]  
🔗 LinkedIn: [https://www.linkedin.com/in/sahil-karande-a77aa7207/](#)

