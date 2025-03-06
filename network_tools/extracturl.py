#!/usr/bin/env python3
"""
URL Extractor Utility

This script extracts URLs from text files and filters them based on a specified prefix.
It supports both HTTP and HTTPS URLs and provides detailed output statistics.

Author: Zulqurnain Haider
Email: zulqurnainjj@gmail.com
"""

import re
import argparse
from pathlib import Path

def extract_filtered_urls(input_file, output_file, url_prefix):
    """
    Extract and filter URLs from a text file.
    
    Args:
        input_file (str): Path to the input file containing text with URLs
        output_file (str): Path where filtered URLs will be saved
        url_prefix (str): URL prefix to filter by (e.g., 'https://example.com')
    
    Returns:
        bool: True if operation was successful, False otherwise
    
    Example:
        >>> extract_filtered_urls('input.txt', 'output.txt', 'https://example.com')
        Found 10 URLs
        Filtered 5 URLs starting with 'https://example.com'
        Results saved to: output.txt
        True
    """
    try:
        # Validate input file
        input_path = Path(input_file)
        if not input_path.is_file():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Create output directory if needed
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Regular expression to find URLs
        url_pattern = r'https?://[^\s"<>]+'
        
        # Read and process file
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Extract URLs
        all_urls = re.findall(url_pattern, text)
        
        # Filter URLs based on the given prefix
        filtered_urls = [url for url in all_urls if url.startswith(url_prefix)]
        
        # Write filtered URLs to output file
        with open(output_file, "w", encoding="utf-8") as f:
            for url in filtered_urls:
                f.write(url + "\n")
        
        print(f"Found {len(all_urls)} URLs")
        print(f"Filtered {len(filtered_urls)} URLs starting with '{url_prefix}'")
        print(f"Results saved to: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    """
    Main function to handle command-line arguments and execute URL extraction.
    
    The script accepts three arguments:
    1. Input file path
    2. Output file path
    3. URL prefix to filter by
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Extract and filter URLs from a file",
        epilog="For issues or suggestions, contact: zulqurnainjj@gmail.com"
    )
    parser.add_argument("input_file", help="Path to the input file containing text")
    parser.add_argument("output_file", help="Path to the output file to save filtered URLs")
    parser.add_argument("url_prefix", help="URL prefix to filter (e.g., 'https://example.com')")
    
    args = parser.parse_args()
    success = extract_filtered_urls(args.input_file, args.output_file, args.url_prefix)
    if not success:
        exit(1)

if __name__ == "__main__":
    main() 