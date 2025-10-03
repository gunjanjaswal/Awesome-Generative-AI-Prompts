#!/usr/bin/env python3
"""
Script to check if images in the README are valid.
"""

import re
import requests
from pathlib import Path

def check_image_url(url):
    """Check if an image URL is valid."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

def main():
    """Main function to check images in README."""
    readme_path = Path(__file__).parent.parent / "README.md"
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all image URLs in the README
    image_urls = re.findall(r'!\[.*?\]\((.*?)\)', content)
    image_urls += re.findall(r'<img src="(.*?)"', content)
    
    print(f"Found {len(image_urls)} image URLs in README.md")
    
    # Check each image URL
    valid_count = 0
    invalid_count = 0
    invalid_urls = []
    
    for url in image_urls:
        if url.startswith('http'):
            is_valid = check_image_url(url)
            if is_valid:
                valid_count += 1
                print(f"✅ Valid: {url}")
            else:
                invalid_count += 1
                invalid_urls.append(url)
                print(f"❌ Invalid: {url}")
        else:
            print(f"⚠️ Skipping local path: {url}")
    
    print(f"\nSummary: {valid_count} valid, {invalid_count} invalid images")
    
    if invalid_urls:
        print("\nInvalid URLs:")
        for url in invalid_urls:
            print(f"- {url}")

if __name__ == "__main__":
    main()
