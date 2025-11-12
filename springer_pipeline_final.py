# =======================================================================
# Springer Capital - Data Engineer Internship Take-Home Test
# Final Pandas Version (Warning-Free + Improved Logic)
# Author: Vishnu
# =======================================================================

import pandas as pd
import numpy as np
from datetime import datetime

# =======================================================================
# STEP 1: LOAD ALL CSV FILES
# =======================================================================

print("📂 Loading datasets...")

lead_logs = pd.read_csv(r"C:\Users\vishn\Downloads\OneDrive_1_12-11-2025\lead_log.csv")
user_referrals = pd.read_csv(r"C:\Users\vishn\Downloads\OneDrive_1_12-11-2025\user_referrals.csv")
user_referral_logs = pd.read_csv(r"C:\Users\vishn\Downloads\OneDrive_1_12-11-2025\user_referral_logs.csv")
user_logs = pd.read_csv(r"C:\Users\vishn\Downloads\OneDrive_1_12-11-2025\user_logs.csv")
user_referral_statuses = pd.read_csv(r"C:\Users\vishn\Downloads\OneDrive_1_12-11-2025\user_referral_statuses.csv")
referral_rewards = pd.read_csv(r"C:\Users\vishn\Downloads\OneDrive_1_12-11-2025\referral_rewards.csv")
paid_transactions = pd.read_csv(r"C:\Users\vishn\Downloads\OneDrive_1_12-11-2025\paid_transactions.csv")

print("✅ All CSV files loaded successfully!")

# =======================================================================
# STEP 2: BASIC DATA PROFILING
# =======================================================================

def profile(df, name):
    print(f"\n📊 Profiling {name}")
    print(f"Shape: {df.shape}")
    print("Nulls per column:\n", df.isnull().sum())
    print("Distinct values per column:\n", df.nunique())
    print("-" * 70)

for name, df in {
    "lead_logs": lead_logs,
    "user_referrals": user_referrals,
    "user_referral_logs": user_referral_logs,
    "user_logs": user_logs,
    "user_referral_statuses": user_referral_statuses,
    "referral_rewards": referral_rewards,
    "paid_transactions": paid_transactions
}.items():
    profile(df, name)

# =======================================================================
# STEP 3: CLEANING AND DATATYPE CONVERSIONS
# =======================================================================

def clean_dataframe(df):
    # Clean column names
    df.columns = [c.strip() for c in df.columns]
    # Clean strings
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()
    # Convert date/datetime columns
    for col in df.columns:
        if any(x in col.lower() for x in ["date", "at", "time"]):
            df[col] = pd.to_datetime(df[col], errors='coerce', utc=True)
    return df

lead_logs = clean_dataframe(lead_logs)
user_referrals = clean_dataframe(user_referrals)
user_referral_logs = clean_dataframe(user_referral_logs)
user_logs = clean_dataframe(user_logs)
user_referral_statuses = clean_dataframe(user_referral_statuses)
referral_rewards = clean_dataframe(referral_rewards)
paid_transactions = clean_dataframe(paid_transactions)

print("✅ Data cleaning completed!")

# =======================================================================
# STEP 4: COMBINE ALL TABLES USING JOINS (FIXED)
# =======================================================================

df = user_referrals.copy()

# Ensure all ID columns are consistent type (convert to string)
for col in df.columns:
    if 'id' in col.lower():
        df[col] = df[col].astype(str)

for dataset in [lead_logs, user_referral_logs, user_logs, user_referral_statuses, referral_rewards, paid_transactions]:
    for col in dataset.columns:
        if 'id' in col.lower():
            dataset[col] = dataset[col].astype(str)

print("🧩 ID columns converted to string for consistent merging...")

# Perform joins
df = df.merge(referral_rewards, how='left', left_on='referral_reward_id', right_on='id', suffixes=('','_reward'))
df = df.merge(user_referral_statuses, how='left', left_on='user_referral_status_id', right_on='id', suffixes=('','_status'))
df = df.merge(user_logs, how='left', left_on='referrer_id', right_on='user_id', suffixes=('','_referrer'))
df = df.merge(paid_transactions, how='left', on='transaction_id', suffixes=('','_txn'))
df = df.merge(lead_logs, how='left', left_on='referee_id', right_on='lead_id', suffixes=('','_lead'))
df = df.merge(user_referral_logs, how='left', left_on='referral_id', right_on='user_referral_id', suffixes=('','_log'))

print("✅ All tables merged successfully!")
print("Final shape:", df.shape)

# =======================================================================
# STEP 5: CREATE NEW FIELD - referral_source_category
# =======================================================================

def source_category(src):
    src = str(src).strip().lower()
    if 'sign up' in src:
        return 'Online'
    elif 'draft' in src:
        return 'Offline'
    elif 'lead' in src:
        return 'Lead'
    else:
        return 'Other'

df['referral_source_category'] = df['referral_source'].apply(source_category)

# =======================================================================
# STEP 6: BUSINESS LOGIC VALIDATION (IMPROVED)
# =======================================================================

def check_valid(row):
    try:
        reward_value = float(row.get('reward_value', 0) or 0)
        status = str(row.get('description', '')).strip().lower()
        txn_status = str(row.get('transaction_status', '')).strip().lower()
        txn_type = str(row.get('transaction_type', '')).strip().lower()
        reward_granted = str(row.get('is_reward_granted', '')).strip().lower() in ['true', '1', 'yes']
        deleted = str(row.get('is_deleted', '')).strip().lower() in ['true', '1', 'yes']
        referral_at = row.get('referral_at')
        txn_at = row.get('transaction_at')

        txn_after_ref = pd.notna(referral_at) and pd.notna(txn_at) and txn_at >= referral_at
        same_month = pd.notna(referral_at) and pd.notna(txn_at) and (
            referral_at.year == txn_at.year and referral_at.month == txn_at.month
        )

        # VALID CASES (less strict, handles variations)
        if (
            reward_value > 0 and
            'berhasil' in status and
            'paid' in txn_status and
            'new' in txn_type and
            txn_after_ref and same_month and
            not deleted and reward_granted
        ):
            return True

        # Pending or failed but with no reward
        if any(x in status for x in ['menunggu', 'tidak berhasil']) and reward_value == 0:
            return True

        # Otherwise invalid
        return False

    except Exception as e:
        return False

df['is_business_logic_valid'] = df.apply(check_valid, axis=1)

print("✅ Business logic validation complete!")

# =======================================================================
# STEP 7: FINAL OUTPUT & SAVE
# =======================================================================

final_cols = [
    'referral_id',
    'referrer_id',
    'referee_id',
    'referral_source',
    'referral_source_category',
    'referral_at',
    'transaction_id',
    'transaction_status',
    'transaction_type',
    'reward_value',
    'description',
    'is_reward_granted',
    'is_business_logic_valid'
]

final_df = df[final_cols].copy()

# Save to CSV
final_output_path = r"C:\Users\vishn\Downloads\referral_business_logic_report.csv"
final_df.to_csv(final_output_path, index=False)

print(f"\n✅ Final report generated successfully!")
print(f"📁 Saved at: {final_output_path}")

# Show sample
print("\n📄 Sample Output:")
print(final_df.head(10))

# =======================================================================
# STEP 8: SUMMARY
# =======================================================================
print("\n🎯 Summary:")
print(f"Total records: {len(final_df)}")
print("Valid rows:", final_df['is_business_logic_valid'].sum())
print("Invalid rows:", len(final_df) - final_df['is_business_logic_valid'].sum())
