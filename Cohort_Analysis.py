import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset with a different encoding
retail_data = pd.read_csv('online_retail_II.csv', encoding='ISO-8859-1')

# Convert InvoiceDate to datetime
retail_data['InvoiceDate'] = pd.to_datetime(retail_data['InvoiceDate'], errors='coerce')

# Remove rows with missing Customer ID values
cleaned_retail_data = retail_data.dropna(subset=['Customer ID'])

# Recalculate the cohort month and cohort index
cleaned_retail_data['CohortMonth'] = cleaned_retail_data.groupby('Customer ID')['InvoiceDate'].transform('min').apply(lambda x: x.strftime('%Y-%m'))
cleaned_retail_data['CohortIndex'] = (cleaned_retail_data['InvoiceDate'].dt.year - cleaned_retail_data['CohortMonth'].str[:4].astype(int)) * 12 + cleaned_retail_data['InvoiceDate'].dt.month - cleaned_retail_data['CohortMonth'].str[5:7].astype(int) + 1

# Calculate the number of unique customers in each cohort and cohort index
cohort_data = cleaned_retail_data.groupby(['CohortMonth', 'CohortIndex'])['Customer ID'].nunique().reset_index()
cohort_data.rename(columns={'Customer ID': 'CustomerCount'}, inplace=True)

# Pivot the data to create a cohort table
cohort_pivot = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='CustomerCount')
cohort_pivot.fillna(0, inplace=True)

# Create a heatmap for the cohort pivot table
plt.figure(figsize=(12, 8))
sns.heatmap(cohort_pivot, annot=True, fmt='.0f', cmap='Blues')
plt.title('Cohort Analysis - Customer Retention')
plt.xlabel('Cohort Index')
plt.ylabel('Cohort Month')
plt.show()
