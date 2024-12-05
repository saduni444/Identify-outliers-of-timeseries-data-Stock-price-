
# Backend – Identify outliers of timeseries data (Stock price)

Global fintech companies operate exchanges worldwide. A part of the data these companies need to provide to their customers is price index information from various exchanges. To maintain high data quality, it is essential to identify potential errors or “outliers” in the price data.

This project identifies and returns a list of outliers in the price data from each file of a specified number of stock files belonging to specified global exchanges. The input data is provided as a zip file containing artificial price data for a number of different global
“Exchanges”.


## Acknowledgements

 - [geeksforgeeks](https://www.geeksforgeeks.org/python-programming-language-tutorial/)
 - [Stack Overflow](https://stackoverflow.com/)
 - [Analyticsvidhya](https://www.analyticsvidhya.com/)
 - [Medium](https://medium.com/)


## Script Explanation 

This Python script mainly consists of two core functions.
- 1st function that, for each file provided, returns exactly 30 consecutive data points starting from a random timestamp within the file.
- 2nd function that, gets the output from 1st one as a feed and defines and identifies the list of outliers as per the requirement.

There are three other supporting functions.
- 3rd function that, saves outliers as a CSV file for each processed input file.
- 4th function that, processes input file recursively, finds all CSV files in the input_data directory and subdirectories.
- The main execution function that, extracts the zip file and applies all functionalities to the input data.

Features

- Function 1: Getting exactly 30 data points as sample from each file randomly but consecutively 
    - Random Sampling: Extracts exactly 30 consecutive records randomly from each CSV file, Ensures data integrity by skipping files with fewer than 30 records as per the requirement. 
    - Error handling: Logs warnings for missing values in data files, Handles scenarios like empty file paths or invalid file structures, Skips files with processing errors without interrupting the entire workflow.
- Function 2: Detect outliers
    - Detect outliers: Calculates mean and standard deviation of the sample, Identifies rows where the stock_price column contains values that deviate more than two standard deviations from the mean as outliers, Defines output columns: Stock-ID: Stock-ID, Timestamp: Timestamp, stock_price: actual stock price at that timestamp, mean: mean of 30 data points, deviation: actual stock price – mean, percentage_deviation: % deviation over and above the threshold.
    - Error handling: Handles unexpected errors during execution by printing the error message and returning the dataframe that contains the error details for debugging.
- Function 3: Save outliers as CSV files
    - Save outputs: Creates an output directory and generate a output file for each processed input file.
    - Error handling: Prints any error that occur during the execution.
- Function 4:  Process input file recursively
    - Process input data: Identifies CSV files within the input_data directory and its subdirectories recursively. Limits the processing to the first num_files CSV files in each folder. Calls Function 1 to get a sample of 30 consecutive rows from the file. Calls Function 2 to identify outliers. Calls Function 3 to save the outliers CSV files.
    - Error handling: Prints any error that occur during the execution.
- The main function: Creates the input_data directory and extracts all its contents into the input_data directory. Calls the Function 4 and processes the data through all the functions in the script.

## Execution instructions
1. Python Environment:
- Ensure Python 3.7 or later is installed on your system.
2. Ensure the following Python libraries are installed in your environment:
- os
- random
- pandas
- numpy
- zipfile

You can install pandas and numpy using the following command in a terminal or command prompt:
    
    pip install pandas numpy
3. Prepare Input Data:
- Save the provided zip file "(TC1)(TC2) stock_price_data_files.zip". 
4. Run the Script:
- Save the script to a file, "stock_price_data_outliers.py".
- Ensure the script and the zip file are in the same directory.
- Open a terminal or command prompt, navigate to the directory where the script and the zip file are located, and execute the script using:


        python stock_price_data_outliers.py
5. Customize Parameters:
- If the sample size need to be change then update the below line of the Python script:
    
       SAMPLE_SIZE = 30
- If the zip file and the specific number of files to process (in this case 2) need to be changed then update the below line of the Python script:

         main("(TC1)(TC2) stock_price_data_files.zip", 2)

6. Output files:
- First this script will generate the input_data directory in the current working directory. And will extract all content of the provided zip file into the input_data directory.
- Then the script will generate the output directory in the current working directory. And will generate a csv(<original_file_name>_outliers.csv) for each file processed in the output directory. If outliers are detected outliers will be display in each CSV file and else "No outliers detected" message will be display in those files. 


## Notes
- Delete the input_data folder if re-running the script to avoid duplication.


## Future Improvements
- Add logging for detailed debugging.
- Handle missing values appropriately.
- Handle files with rows less than the sample size appropriately.(For this case all data can be used to detect outliers.)
- Include visualization for outliers.
- Support other file formats like .xlsx or .json.