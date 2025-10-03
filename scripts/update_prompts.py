#!/usr/bin/env python3
"""
Script to automatically update the generative AI prompts repository.
This script fetches new prompts from various sources and updates the markdown files.
"""

import os
import re
import json
import time
import logging
import requests
from datetime import datetime
from pathlib import Path
import concurrent.futures
import random  # For demo purposes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("update_log.txt"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("prompt_updater")

# Constants
REPO_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"
README_PATH = REPO_ROOT / "README.md"
CONFIG_PATH = REPO_ROOT / "scripts" / "config.json"
USER_AGENT = "AwesomeGenerativeAIPrompts/1.0"

# API endpoints for different sources
# In a real implementation, these would be actual API endpoints
SOURCES = {
    "chatgpt": [
        "https://api.example.com/chatgpt/prompts",
        "https://api.another-source.com/gpt/top-prompts"
    ],
    "midjourney": [
        "https://api.example.com/midjourney/prompts"
    ],
    "dalle": [
        "https://api.example.com/dalle/prompts"
    ],
    "stable-diffusion": [
        "https://api.example.com/stable-diffusion/prompts"
    ],
    "claude": [
        "https://api.example.com/claude/prompts"
    ],
    "gemini": [
        "https://api.example.com/gemini/prompts"
    ]
}

# Sample config (would be loaded from config.json in production)
DEFAULT_CONFIG = {
    "update_frequency": "daily",
    "max_prompts_per_category": 100,
    "min_rating": 4.0,
    "excluded_keywords": ["inappropriate", "nsfw", "offensive"],
    "api_keys": {
        "example_api": "YOUR_API_KEY_HERE"
    }
}


def load_config():
    """Load configuration from config file or create default if not exists."""
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG
    
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)


def fetch_prompts_from_source(source_url, category):
    """
    Fetch prompts from a given source URL.
    
    In a real implementation, this would make actual API calls.
    For demo purposes, we'll generate some random prompts.
    """
    logger.info(f"Fetching prompts from {source_url} for {category}")
    
    # Simulate API call delay
    time.sleep(0.5)
    
    # For demo purposes, generate random prompts
    # In a real implementation, this would parse the API response
    prompts = []
    
    # Different prompt structures based on category
    if category == "chatgpt":
        prompts = [
            {
                "prompt": f"Explain the concept of {random.choice(['quantum computing', 'blockchain', 'neural networks'])} as if I'm {random.choice(['5 years old', 'a medieval peasant', 'an alien'])}",
                "description": "Simplified explanation of complex topics",
                "category": "Education",
                "source": source_url,
                "date_added": datetime.now().strftime("%Y-%m-%d")
            }
            for _ in range(3)  # Generate 3 random prompts
        ]
    elif category in ["midjourney", "dalle", "stable-diffusion"]:
        styles = ["photorealistic", "anime", "oil painting", "watercolor", "3D render"]
        subjects = ["landscape", "portrait", "sci-fi scene", "fantasy character", "abstract concept"]
        prompts = [
            {
                "prompt": f"A {random.choice(styles)} of {random.choice(subjects)}",
                "description": "Generates creative imagery",
                "style": random.choice(styles),
                "parameters": f"--ar {random.choice(['1:1', '16:9', '2:3'])} --v 5",
                "source": source_url,
                "date_added": datetime.now().strftime("%Y-%m-%d")
            }
            for _ in range(3)  # Generate 3 random prompts
        ]
    else:
        prompts = [
            {
                "prompt": f"Generate a {random.choice(['creative', 'detailed', 'concise'])} {random.choice(['story', 'explanation', 'analysis'])} about {random.choice(['technology', 'nature', 'history'])}",
                "description": "General purpose prompt",
                "category": "Content Creation",
                "source": source_url,
                "date_added": datetime.now().strftime("%Y-%m-%d")
            }
            for _ in range(3)  # Generate 3 random prompts
        ]
    
    return prompts


def update_markdown_file(category, new_prompts):
    """Update the markdown file for a specific category with new prompts."""
    file_path = PROMPTS_DIR / f"{category}.md"
    
    # Create file if it doesn't exist
    if not file_path.exists():
        file_path.parent.mkdir(exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(f"# {category.title()} Prompts\n\n")
            f.write(f"A collection of effective prompts specifically designed for {category.title()} models.\n\n")
            
            # Different table headers based on category
            if category in ["midjourney", "dalle", "stable-diffusion"]:
                f.write("| Prompt | Description | Style | Parameters | Source | Date Added |\n")
                f.write("|--------|-------------|-------|------------|--------|------------|\n")
            else:
                f.write("| Prompt | Description | Category | Source | Date Added |\n")
                f.write("|--------|-------------|----------|--------|------------|\n")
            
            f.write("\n<!-- This file is automatically updated daily -->")
    
    # Read existing content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract existing table rows
    if category in ["midjourney", "dalle", "stable-diffusion"]:
        pattern = r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
    else:
        pattern = r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
    
    existing_rows = re.findall(pattern, content)
    
    # Skip header rows
    if existing_rows:
        existing_rows = existing_rows[1:]  # Skip header row
    
    # Convert existing rows to set of prompts for deduplication
    existing_prompts = set()
    for row in existing_rows:
        existing_prompts.add(row[0])  # First column is the prompt
    
    # Add new prompts that don't already exist
    new_rows = []
    for prompt_data in new_prompts:
        if prompt_data["prompt"] not in existing_prompts:
            if category in ["midjourney", "dalle", "stable-diffusion"]:
                new_row = f"| {prompt_data['prompt']} | {prompt_data['description']} | {prompt_data['style']} | {prompt_data.get('parameters', '')} | {prompt_data['source']} | {prompt_data['date_added']} |"
            else:
                new_row = f"| {prompt_data['prompt']} | {prompt_data['description']} | {prompt_data['category']} | {prompt_data['source']} | {prompt_data['date_added']} |"
            new_rows.append(new_row)
    
    # Insert new rows after the header
    if new_rows:
        header_end = content.find("\n|------")
        next_line = content.find("\n", header_end + 1)
        updated_content = content[:next_line + 1] + "\n".join(new_rows) + "\n" + content[next_line + 1:]
        
        # Write updated content
        with open(file_path, 'w') as f:
            f.write(updated_content)
        
        logger.info(f"Added {len(new_rows)} new prompts to {category}.md")
    else:
        logger.info(f"No new prompts to add to {category}.md")


def update_readme_stats():
    """Update the statistics in the README file."""
    # Count total prompts
    total_prompts = 0
    for md_file in PROMPTS_DIR.glob("*.md"):
        with open(md_file, 'r') as f:
            content = f.read()
            # Count table rows (excluding header and separator)
            rows = re.findall(r"^\|.*\|$", content, re.MULTILINE)
            if len(rows) > 2:  # Header + separator + at least one prompt
                total_prompts += len(rows) - 2
    
    # Count categories
    categories = len(list(PROMPTS_DIR.glob("*.md")))
    
    # Update README
    with open(README_PATH, 'r') as f:
        content = f.read()
    
    # Update last refresh date
    today = datetime.now().strftime("%B %d, %Y")
    content = re.sub(r"<h3>Last refresh: <span style=\"color:#00CC66\">(.*?)</span></h3>", 
                    f"<h3>Last refresh: <span style=\"color:#00CC66\">{today}</span></h3>", content)
    
    # Update stats in the new table format
    content = re.sub(r"<td>\d+</td>\s*</tr>\s*<tr>\s*<td align=\"center\"><h3>🗂️</h3></td>", 
                    f"<td>{total_prompts}</td>\n  </tr>\n  <tr>\n    <td align=\"center\"><h3>🗂️</h3></td>", content)
    content = re.sub(r"<td>\d+</td>\s*</tr>\s*<tr>\s*<td align=\"center\"><h3>👥</h3></td>", 
                    f"<td>{categories}</td>\n  </tr>\n  <tr>\n    <td align=\"center\"><h3>👥</h3></td>", content)
    
    with open(README_PATH, 'w') as f:
        f.write(content)
    
    logger.info(f"Updated README stats: {total_prompts} prompts across {categories} categories")


def main():
    """Main function to update all prompt files."""
    logger.info("Starting prompt update process")
    
    config = load_config()
    
    # Create prompts directory if it doesn't exist
    PROMPTS_DIR.mkdir(exist_ok=True)
    
    # Process each category
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_category = {}
        
        for category, source_urls in SOURCES.items():
            # Fetch prompts from all sources for this category
            all_prompts = []
            for url in source_urls:
                try:
                    prompts = fetch_prompts_from_source(url, category)
                    all_prompts.extend(prompts)
                except Exception as e:
                    logger.error(f"Error fetching from {url}: {e}")
            
            # Update the markdown file for this category
            if all_prompts:
                future = executor.submit(update_markdown_file, category, all_prompts)
                future_to_category[future] = category
        
        # Wait for all updates to complete
        for future in concurrent.futures.as_completed(future_to_category):
            category = future_to_category[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error updating {category}: {e}")
    
    # Update README stats
    update_readme_stats()
    
    logger.info("Prompt update process completed successfully")


if __name__ == "__main__":
    main()
