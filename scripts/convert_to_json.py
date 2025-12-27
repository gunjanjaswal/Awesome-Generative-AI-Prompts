#!/usr/bin/env python3
"""
Convert existing markdown prompts to structured JSON format
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"
OUTPUT_FILE = REPO_ROOT / "prompts.json"

# Map categories to use cases
CATEGORY_MAP = {
    "chatgpt": "general",
    "claude": "general",
    "gemini": "general",
    "coding": "coding",
    "writing": "content-creation",
    "business": "business",
    "dalle": "image-generation",
    "midjourney": "image-generation",
    "stable-diffusion": "image-generation",
    "image-generation": "image-generation"
}

def parse_markdown_table(content, file_category):
    """Parse markdown table and extract prompts"""
    prompts = []
    
    # Find all table rows
    pattern = r"\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|(?:([^|]+)\|)?"
    matches = re.findall(pattern, content)
    
    # Skip header rows
    for i, match in enumerate(matches):
        if i < 2:  # Skip header and separator
            continue
            
        # Clean up the values
        values = [v.strip() for v in match]
        
        # Determine if this is an image generation prompt
        is_image = file_category in ["dalle", "midjourney", "stable-diffusion", "image-generation"]
        
        if is_image and len(values) >= 6:
            prompt_text = values[0]
            description = values[1]
            style = values[2]
            parameters = values[3]
            source = values[4]
            date_added = values[5]
        else:
            prompt_text = values[0]
            description = values[1]
            category = values[2] if len(values) > 2 else "General"
            source = values[3] if len(values) > 3 else "Unknown"
            date_added = values[4] if len(values) > 4 else datetime.now().strftime("%Y-%m-%d")
            style = None
            parameters = None
        
        # Skip if prompt is empty or looks like header
        if not prompt_text or "Prompt" in prompt_text or "---" in prompt_text:
            continue
        
        # Determine difficulty based on prompt complexity
        difficulty = "beginner"
        if len(prompt_text) > 100 or "[" in prompt_text:
            difficulty = "intermediate"
        if "step by step" in prompt_text.lower() or "detailed" in prompt_text.lower():
            difficulty = "advanced"
        
        # Determine compatible models
        models = []
        if file_category in ["chatgpt", "coding", "writing", "business"]:
            models = ["chatgpt", "claude", "gemini"]
        elif file_category == "claude":
            models = ["claude", "chatgpt", "gemini"]
        elif file_category == "gemini":
            models = ["gemini", "chatgpt", "claude"]
        elif file_category in ["dalle", "midjourney", "stable-diffusion", "image-generation"]:
            models = [file_category] if file_category != "image-generation" else ["dalle", "midjourney", "stable-diffusion"]
        
        # Create prompt object
        prompt_obj = {
            "id": f"{file_category}-{len(prompts) + 1}",
            "title": description[:50] if len(description) > 50 else description,
            "prompt": prompt_text,
            "description": description,
            "category": CATEGORY_MAP.get(file_category, "general"),
            "subcategory": file_category,
            "difficulty": difficulty,
            "rating": 4.5,  # Default rating
            "models": models,
            "tags": extract_tags(prompt_text, description),
            "date_added": date_added,
            "copy_count": 0
        }
        
        if style:
            prompt_obj["style"] = style
        if parameters:
            prompt_obj["parameters"] = parameters
        
        prompts.append(prompt_obj)
    
    return prompts

def extract_tags(prompt, description):
    """Extract relevant tags from prompt and description"""
    tags = []
    text = (prompt + " " + description).lower()
    
    # Common tags
    tag_keywords = {
        "code": ["code", "programming", "function", "debug"],
        "writing": ["write", "blog", "article", "content"],
        "creative": ["creative", "story", "imaginative"],
        "business": ["business", "professional", "email", "marketing"],
        "analysis": ["analysis", "analyze", "evaluate"],
        "education": ["explain", "teach", "learn", "education"],
        "image": ["image", "photo", "painting", "render"],
        "professional": ["professional", "expert", "senior"]
    }
    
    for tag, keywords in tag_keywords.items():
        if any(keyword in text for keyword in keywords):
            tags.append(tag)
    
    return tags[:5]  # Limit to 5 tags

def main():
    all_prompts = []
    
    # Process each markdown file
    for md_file in PROMPTS_DIR.glob("*.md"):
        print(f"Processing {md_file.name}...")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_category = md_file.stem
        prompts = parse_markdown_table(content, file_category)
        all_prompts.extend(prompts)
        print(f"  Found {len(prompts)} prompts")
    
    # Create output structure
    output = {
        "version": "1.0",
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "total_prompts": len(all_prompts),
        "prompts": all_prompts
    }
    
    # Write to JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nSuccessfully converted {len(all_prompts)} prompts to {OUTPUT_FILE}")
    
    # Print category breakdown
    categories = {}
    for prompt in all_prompts:
        cat = prompt['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory breakdown:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    main()
