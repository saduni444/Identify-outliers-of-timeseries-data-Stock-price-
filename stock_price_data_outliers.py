import os
import random
import pandas as pd
import numpy as np
from zipfile import ZipFile



SAMPLE_SIZE = 30

# Function 1: Getting exactly 30 data points as sample from each file randomly but consecutively 
def fetch_sample_data(file_path):
    try:
        # Check if the file path is empty or invalid
        if not file_path or not os.path.exists(file_path):
            raise ValueError(f"File path is empty or does not exist: {file_path}")

        # Assign column names explicitly as per the reference document
        column_names = ['Stock-ID', 'Timestamp', 'stock_price']
        df = pd.read_csv(file_path, header=None, names=column_names)

        # Check for missing values
        if df.isnull().values.any():
            print(f"Warning: File {file_path} contains missing values.")

        # Check if the file has fewer than the required sample size
        if len(df) < SAMPLE_SIZE:
            raise ValueError(f"File {file_path} has fewer than {SAMPLE_SIZE} data points. Cannot proceed with sampling.")

        # Define the range for valid random start indices
        max_start_index = len(df) - SAMPLE_SIZE

        # Pick a random starting index
        start_index = random.randint(0, max_start_index)
        
        # Return exactly 30 consecutive data points
        return df.iloc[start_index: start_index + SAMPLE_SIZE].copy()
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        # Optional: Log errors to a file for detailed tracking
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"{file_path}: {e}\n")
        return None





# Function 2: Detect outliers
def detect_outliers(sampled_data):
    try:
        #  mean and standard deviation for sample data 
        mean = sampled_data['stock_price'].mean()
        std_dev = sampled_data['stock_price'].std()

        # outlier thresholds
        lower_bound = mean - 2 * std_dev
        upper_bound = mean + 2 * std_dev

        
        outliers = sampled_data[
            (sampled_data['stock_price'] < lower_bound) |
            (sampled_data['stock_price'] > upper_bound)
        ].copy()

        # define columns
        outliers['mean'] = mean
        outliers['deviation'] = outliers['stock_price'] - mean
        outliers['percentage_deviation'] = (
            (outliers['deviation'].abs() - 2 * std_dev) / (2 * std_dev) * 100
        ).round(2)

        # Return the required columnsas per the reference document
        return outliers[['Stock-ID', 'Timestamp', 'stock_price', 'mean', 'deviation', 'percentage_deviation']]
    except Exception as e:
        print(f"Error in outlier detection: {e}")
        
        return pd.DataFrame({'Error': [str(e)]})

#Function 3: Save outliers as csv file 
def save_outliers_to_csv(outliers, input_file_path):
    try:
        
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)  
        input_file_name = os.path.basename(input_file_path).replace('.csv', '_outliers.csv')
        output_file_path = os.path.join(output_dir, input_file_name)

        if not outliers.empty:
            # Save outliers to CSV
            outliers.to_csv(output_file_path, index=False)
            print(f"Outliers saved to {output_file_path}")
        else:
            with open(output_file_path, 'w') as f:
                f.write("No outliers detected.\n")
            print(f"No outliers found. Empty file created: {output_file_path}")
    except Exception as e:
        print(f"Error saving outliers to file: {e}")


#Function 4: Process input file recursively 
def process_files_recursively(input_dir, num_files):
    try:
        for root, _, files in os.walk(input_dir):
            csv_files = [os.path.join(root, file) for file in files if file.endswith('.csv')]
            if not csv_files:
                print(f"No CSV files found in folder: {root}")
                continue

            # Process only the specified number of files
            files_to_process = csv_files[:num_files]
            for file_path in files_to_process:
                print(f"Processing file: {file_path}")
                sampled_data = fetch_sample_data(file_path)
                if sampled_data is not None:
                    outliers = detect_outliers(sampled_data)
                    save_outliers_to_csv(outliers, file_path)
                else:
                    print(f"Skipping file due to processing errors: {file_path}")
    except Exception as e:
        print(f"Error while processing files: {e}")


# Main Execution
def main(input_zip, num_files):
    input_dir = "input_data"
    os.makedirs(input_dir, exist_ok=True)

    # Extract files
    with ZipFile(input_zip, 'r') as zip_ref:
        zip_ref.extractall(input_dir)
    
    process_files_recursively(input_dir, num_files)
#enter your zip file location and maximum number of files you need to consider within the one section
if __name__ == "__main__":
    main("(TC1)(TC2) stock_price_data_files.zip", 2)
