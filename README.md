# MyUtils - A Collection of Python Utilities

This repository contains a collection of useful Python utilities for various tasks. Each utility is designed to be simple, efficient, and easy to use.

## 📂 Current Utilities

### 1. URL Extractor (`network_tools/extracturl.py`)

A Python script that extracts URLs from text files and filters them based on a specific prefix.

#### Features
- Extract URLs using regular expressions
- Filter URLs based on a specified prefix
- Command-line interface for easy usage
- UTF-8 encoding support

#### Usage
```bash
python network_tools/extracturl.py input.txt output.txt "https://example.com"
```

### 2. Text Format Converter (`text_processing/text_converter.py`)

Convert text between different formats (uppercase, lowercase, title case, etc.).

#### Features
- Multiple format options (upper, lower, title, sentence, alternating)
- File-based processing
- UTF-8 encoding support
- Input validation and error handling

#### Usage
```bash
python text_processing/text_converter.py input.txt output.txt --format upper
```

### 3. Batch File Renamer (`file_operations/batch_renamer.py`)

Rename multiple files in a directory using patterns or regular expressions.

#### Features
- Simple pattern replacement
- Regular expression support
- Dry-run option for safe testing
- Detailed operation logging
- Duplicate file detection

#### Usage
```bash
python file_operations/batch_renamer.py directory "old_pattern" "new_pattern" --regex
python file_operations/batch_renamer.py directory "old_pattern" "new_pattern" --dry-run
```

### 4. CSV Processor (`data_processing/csv_processor.py`)

Process CSV files with various operations like sorting, filtering, and statistics.

#### Features
- Sort by multiple columns
- Filter rows based on conditions
- Generate statistical summaries
- Pandas-powered processing
- Column validation
- Null value reporting

#### Usage
```bash
python data_processing/csv_processor.py input.csv output.csv --operation sort --columns "name,age"
python data_processing/csv_processor.py input.csv output.csv --operation filter --columns "age" --value 25
python data_processing/csv_processor.py input.csv stats.txt --operation stats
```

### 5. System Information Collector (`system_utilities/sysinfo.py`)

Collect and display detailed system information.

#### Features
- CPU information (cores, usage, frequency)
- Memory statistics
- Disk usage and partitions
- Network interfaces and I/O
- Multiple output formats (text, JSON)
- Graceful handling of unavailable metrics

#### Usage
```bash
python system_utilities/sysinfo.py --format text
python system_utilities/sysinfo.py --format json --output system_info.json
```

## 🔜 Future Utilities

The following sections are reserved for future utilities that will be added to this repository:

### Text Processing
- [ ] String manipulation tools
- [ ] Character encoding utilities

### File Operations
- [ ] Directory organization tools

### Data Processing
- [ ] JSON/XML utilities
- [ ] Data validation tools

### Network Tools
- [x] URL extractor and filter
- [ ] Web scraping utilities
- [ ] API interaction helpers

### System Utilities
- [ ] Process management tools
- [ ] Backup utilities

## 🛠️ Requirements
- Python 3.6 or higher
- Required packages:
  ```
  pandas>=1.5.0
  psutil>=5.9.0
  ```

## 📝 Contributing
Feel free to contribute to this repository by:
1. Creating a new utility
2. Improving existing utilities
3. Adding documentation
4. Reporting issues

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support
If you encounter any issues or have suggestions, please open an issue in the repository.
