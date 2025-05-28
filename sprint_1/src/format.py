import csv
import re
 
# Function to read unformatted data from a .txt file
def read_data_from_file(filename):
    with open(filename, mode='r') as file:
        # Read all lines from the file and strip any extra whitespace
        return [line.strip() for line in file.readlines()]
 
# Function to process and format the data
def format_data(data):
    formatted_data = []
   
    # Regex pattern to capture the required fields
    for line in data:
        match = re.match(
            r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})\s+([A-Za-z\s]+)\s+([A-Za-z\s]+)\s+"?(.+?)"?\s+([\d.]+)\s+(CARD|CASH)\s*(\d+)?',
            line
        )
       
        if match:
            date = match.group(1)  # Date
            time = match.group(2)  # Time
            location = match.group(3).strip()  # Location (branch)
            customer_name = match.group(4).strip()  # Customer's full name
            items = match.group(5).strip()  # Items ordered
            total_amount = match.group(6)  # Total amount
            payment_method = match.group(7)  # Transaction type
            card_no = match.group(8) if match.group(8) else "N/A"  # Transaction ID or N/A
           
            # Format the result as required
            formatted_entry = [date,time,location,customer_name,f'"{items}"',total_amount,payment_method,card_no]
            formatted_data.append(formatted_entry)
        else:
            # Log skipped lines for debugging
            print(f"Skipped line: {line}")
   
    return formatted_data
 
# Function to write formatted data to CSV
def write_to_csv(formatted_data, filename="formatted_data.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
       
        # Writing header row
        writer.writerow(["date", "time", "branch_name", "first_name", "last_name", "items", "total", "trans_type", "card_no"])
       
        # Writing data rows
        writer.writerows(formatted_data)

def format_func(file_path): 
# Main execution
    if __name__ == "__main__":
        # Read unformatted data from a .txt file
        data = read_data_from_file(file_path)
    
        # Format the data
        formatted_data = format_data(data)
    
        # Write formatted data to a CSV file
        output_filename = "formatted_data_thurs_pm.csv"
        write_to_csv(formatted_data, output_filename)
    
        # Optionally print the formatted data to check
        for row in formatted_data:
            print(row)
        # Print summary
        print(f"Total lines processed: {len(formatted_data)}")