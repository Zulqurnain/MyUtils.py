#!/usr/bin/env python3
"""
Text Format Converter Utility

This script converts text between different formats including uppercase, lowercase,
title case, sentence case, and alternating case. It supports file-based processing
with UTF-8 encoding.

Author: Zulqurnain Haider
Email: zulqurnainjj@gmail.com
"""

import argparse
from pathlib import Path

def convert_text(text, format_type):
    """
    Convert text to specified format.
    
    Args:
        text (str): The input text to convert
        format_type (str): The target format. One of:
            - 'upper': Convert to uppercase
            - 'lower': Convert to lowercase
            - 'title': Convert to title case
            - 'sentence': Convert to sentence case
            - 'alternating': Convert to alternating case
    
    Returns:
        str: The converted text
    
    Example:
        >>> convert_text("hello world", "upper")
        'HELLO WORLD'
        >>> convert_text("hello world", "title")
        'Hello World'
        >>> convert_text("hello world", "alternating")
        'hElLo wOrLd'
    """
    if format_type == "upper":
        return text.upper()
    elif format_type == "lower":
        return text.lower()
    elif format_type == "title":
        return text.title()
    elif format_type == "sentence":
        return '. '.join(s.strip().capitalize() for s in text.split('.') if s.strip())
    elif format_type == "alternating":
        return ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))
    return text

def process_file(input_file, output_file, format_type):
    """
    Process the input file and write converted text to output file.
    
    Args:
        input_file (str): Path to the input file to read
        output_file (str): Path to the output file to write
        format_type (str): The target format for conversion
    
    Returns:
        bool: True if operation was successful, False otherwise
    
    Raises:
        FileNotFoundError: If input file doesn't exist
        IOError: If there are issues reading/writing files
    """
    try:
        # Validate input file
        input_path = Path(input_file)
        if not input_path.is_file():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Create output directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read and process file
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        converted_text = convert_text(text, format_type)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(converted_text)
            
        print(f"Successfully converted text to {format_type} format")
        print(f"Output saved to: {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    return True

def main():
    """
    Main function to handle command-line arguments and execute text conversion.
    
    The script accepts the following arguments:
    1. Input file path
    2. Output file path
    3. Format type (optional, defaults to 'lower')
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Convert text between different formats",
        epilog="For issues or suggestions, contact: zulqurnainjj@gmail.com"
    )
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")
    parser.add_argument(
        "--format", 
        choices=["upper", "lower", "title", "sentence", "alternating"],
        default="lower",
        help="Output format (default: lower)"
    )
    
    args = parser.parse_args()
    success = process_file(args.input_file, args.output_file, args.format)
    if not success:
        exit(1)

if __name__ == "__main__":
    main() 