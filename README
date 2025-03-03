# Log Processor for API Order Analysis

A Python tool that processes API order request logs, extracts relevant data using regular expressions, and performs statistical analysis such as calculating orders per second.

## Features

- Parse log files using regex pattern matching
- Extract order request and response details
- Calculate order frequency statistics
- Export processed data to Excel
- Readable and maintainable code structure

## Requirements

- Python 3.6+
- pandas
- openpyxl

## Installation

```bash
git clone https://github.com/alshirin/test_interview_assignment_1.git
cd test_interview_assignment_1
pip install -r requirements.txt
```

## Usage

1. Place your log file in the project directory
2. Run the processor script:

```bash
pytest -v
```

The script will:
- Read and parse the log file
- Extract API order information
- Calculate orders per second metrics
- Generate an Excel file with the parsed data

## Data Fields

The processor extracts numerous data points from each log entry, including:

- Client information (IP)
- Request details (symbol, side, quantity, price, etc.)
- Response data (orderId, status, transaction time)
- Performance metrics (processing time, latency)

## Output

Results are saved to `orders.xlsx` with all extracted fields. The maximum requests per second value is displayed in the console output.