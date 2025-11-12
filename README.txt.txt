============================================================
SPRINGER CAPITAL - DATA ENGINEERING INTERNSHIP PROJECT
Author: Vishnu
Date: November 2025
============================================================

🧠 PROJECT OVERVIEW
------------------------------------------------------------
This project was developed as part of the Springer Capital Data Engineering Internship Assessment.

The objective is to integrate, clean, and validate multiple datasets using Python. 
The final output file generates a validated referral report combining all seven input CSV files.

The project automates:
- Loading of all CSV datasets
- Cleaning and formatting of data
- Merging datasets using relationships
- Applying business logic validation
- Generating a final clean report (referral_business_logic_report.csv)


📂 DATASETS USED
------------------------------------------------------------
1. lead_logs.csv
2. user_referrals.csv
3. user_referral_logs.csv
4. user_logs.csv
5. user_referral_statuses.csv
6. referral_rewards.csv
7. paid_transactions.csv


⚙️ TECH STACK
------------------------------------------------------------
- Python 3.10
- Pandas
- NumPy
- Docker (for containerization)
- Excel / CSV for reporting


🚀 HOW TO RUN THE PROJECT (WITHOUT DOCKER)
------------------------------------------------------------
1. Make sure all CSV files are in the same folder as the Python script.
2. Open Command Prompt or PyCharm terminal.
3. Run the command:
   python springer_pipeline_final.py

4. The script will:
   - Load and clean all input data
   - Merge and validate all tables
   - Create a final output CSV file named:
     referral_business_logic_report.csv

5. The output file will be saved in:
   C:\Users\vishn\Downloads\referral_business_logic_report.csv


🐳 HOW TO RUN THE PROJECT (WITH DOCKER)
------------------------------------------------------------
1. Open terminal in your project directory.
2. Build the Docker image:
   docker build -t springer-data-pipeline .

3. Run the container:
   docker run -it springer-data-pipeline

4. The script will automatically execute inside the container.


📊 OUTPUT FILE DETAILS
------------------------------------------------------------
File: referral_business_logic_report.csv

Columns:
1. referral_id – Unique referral record ID
2. referrer_id – ID of user who made the referral
3. referee_id – ID of referred person
4. referral_source – Source of referral (app/web/lead)
5. referral_source_category – Derived category (Online, Offline, Lead)
6. referral_at – Date and time of referral
7. transaction_id – Linked transaction reference
8. transaction_status – Transaction status (e.g., Paid)
9. transaction_type – Type of transaction (New/Renewal)
10. reward_value – Value of referral reward
11. description – Referral status (Completed, Pending, etc.)
12. is_reward_granted – Whether reward was granted (True/False)
13. is_business_logic_valid – Final validation result (True/False)


📘 SUPPORTING FILES INCLUDED
------------------------------------------------------------
1. springer_pipeline_final.py          → Main Python script
2. referral_business_logic_report.csv  → Final output file
3. data_profiling_report.png           → Screenshot of profiling results
4. Data_Dictionary.xlsx                → Column meanings and sources
5. requirements.txt                    → Python dependencies list
6. Dockerfile                          → Container setup configuration
7. README.txt                          → Project documentation (this file)


🧩 AUTHOR DETAILS
------------------------------------------------------------
Name: Vishnu
Program: B.Tech – Data Science
Internship: Data Engineering Internship – Springer Capital
Date: November 2025

============================================================
END OF DOCUMENT
============================================================
