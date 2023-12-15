import pandas as pd

# Load the Excel file
file_path = '/mnt/data/人工校准结果.xlsx'
excel_data = pd.ExcelFile(file_path)

# Initialize dictionaries to store results
sheet_results = {}
overall_results = {'total': 0, 1: 0, 2: 0, 3: 0, 4: 0}

# Process each sheet
for sheet_name in excel_data.sheet_names:
    df = pd.read_excel(excel_data, sheet_name=sheet_name)
    # Assuming the column with audit results is named '审核结果'
    if '审核结果' in df.columns:
        results = df['审核结果'].value_counts()
        total = results.sum()
        qualified = results.get(3, 0) + results.get(4, 0)
        qualified_rate = qualified / total if total else 0

        # Store results for each sheet
        sheet_results[sheet_name] = {
            'total': total,
            'qualified_rate': qualified_rate,
            1: results.get(1, 0),
            2: results.get(2, 0),
            3: results.get(3, 0),
            4: results.get(4, 0)
        }

        # Update overall results
        overall_results['total'] += total
        for i in range(1, 5):
            overall_results[i] += results.get(i, 0)

# Calculate overall qualified rate
overall_qualified = overall_results[3] + overall_results[4]
overall_results['qualified_rate'] = overall_qualified / overall_results['total'] if overall_results['total'] else 0

sheet_results, overall_results

# Creating a DataFrame to store all the results in a single sheet
results_df = pd.DataFrame()

# Adding overall results to the DataFrame
overall_df = pd.DataFrame([overall_results])
overall_df.index = ['整体结果']
results_df = results_df.append(overall_df)

# Adding each sheet's results
for sheet_name, result in sheet_results.items():
    temp_df = pd.DataFrame([result])
    temp_df.index = [sheet_name]
    results_df = results_df.append(temp_df)

# Reordering columns for better readability
results_df = results_df[['total', 1, 2, 3, 4, 'qualified_rate']]

# Saving the DataFrame to an Excel file
output_file_path = '/mnt/data/审核结果统计.xlsx'
results_df.to_excel(output_file_path)

output_file_path
