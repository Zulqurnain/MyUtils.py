import re
import argparse

def extract_filtered_urls(input_file, output_file, url_prefix):
    # Regular expression to find URLs
    url_pattern = r'https?://[^\s"<>]+'

    # Read input file
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    # Extract URLs
    all_urls = re.findall(url_pattern, text)

    # Filter URLs based on the given prefix
    filtered_urls = [url for url in all_urls if url.startswith(url_prefix)]

    # Write filtered URLs to output file
    with open(output_file, "w", encoding="utf-8") as file:
        for url in filtered_urls:
            file.write(url + "\n")

# Command-line argument parser
parser = argparse.ArgumentParser(description="Extract and filter URLs from a file.")
parser.add_argument("input_file", type=str, help="Path to the input file containing text.")
parser.add_argument("output_file", type=str, help="Path to the output file to save filtered URLs.")
parser.add_argument("url_prefix", type=str, help="URL prefix to filter (e.g., 'https://example.com').")

args = parser.parse_args()

# Run URL extraction with filtering
extract_filtered_urls(args.input_file, args.output_file, args.url_prefix)
