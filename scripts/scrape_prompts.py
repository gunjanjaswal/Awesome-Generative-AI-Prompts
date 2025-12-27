#!/usr/bin/env python3
"""
Automated prompt scraper that finds new high-quality prompts from various sources.
Runs daily via GitHub Actions to keep the collection fresh.
"""

import json
import re
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# File paths
PROMPTS_FILE = Path(__file__).parent.parent / "prompts.json"

# Sources to scrape (add more as needed)
SOURCES = {
    "reddit": [
        "https://www.reddit.com/r/ChatGPT/top/.json?t=week&limit=25",
        "https://www.reddit.com/r/ClaudeAI/top/.json?t=week&limit=25",
        "https://www.reddit.com/r/PromptEngineering/top/.json?t=week&limit=25",
    ],
    # Add more sources like Twitter, GitHub, etc.
}

def load_existing_prompts() -> Dict:
    """Load existing prompts from JSON file."""
    with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_prompts(data: Dict):
    """Save prompts to JSON file."""
    with open(PROMPTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def scrape_reddit(url: str) -> List[Dict]:
    """Scrape prompts from Reddit."""
    headers = {'User-Agent': 'PromptScraper/1.0'}
    prompts = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return prompts
        
        data = response.json()
        
        for post in data.get('data', {}).get('children', []):
            post_data = post.get('data', {})
            title = post_data.get('title', '')
            selftext = post_data.get('selftext', '')
            
            # Look for prompts in title or text
            # Simple heuristic: posts with "prompt" in title and good engagement
            if 'prompt' in title.lower() and post_data.get('score', 0) > 50:
                # Extract potential prompt
                prompt_text = selftext if selftext else title
                
                # Basic quality check
                if len(prompt_text) > 50 and len(prompt_text) < 2000:
                    prompts.append({
                        'text': prompt_text,
                        'source': f"Reddit: {post_data.get('subreddit', 'unknown')}",
                        'score': post_data.get('score', 0),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}"
                    })
    
    except Exception as e:
        print(f"Error scraping Reddit: {e}")
    
    return prompts

def categorize_prompt(text: str) -> str:
    """Automatically categorize a prompt based on keywords."""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['code', 'function', 'debug', 'programming', 'developer']):
        return 'coding'
    elif any(word in text_lower for word in ['write', 'blog', 'article', 'content', 'copy']):
        return 'content-creation'
    elif any(word in text_lower for word in ['business', 'swot', 'strategy', 'marketing', 'email']):
        return 'business'
    elif any(word in text_lower for word in ['learn', 'explain', 'teach', 'study', 'education']):
        return 'learning'
    elif any(word in text_lower for word in ['story', 'creative', 'character', 'narrative']):
        return 'creative'
    elif any(word in text_lower for word in ['schedule', 'plan', 'organize', 'productivity']):
        return 'productivity'
    elif any(word in text_lower for word in ['image', 'photo', 'picture', 'dall-e', 'midjourney']):
        return 'image-generation'
    else:
        return 'general'

def assess_difficulty(text: str) -> str:
    """Assess prompt difficulty based on complexity."""
    if len(text) > 500 or 'advanced' in text.lower() or 'expert' in text.lower():
        return 'advanced'
    elif len(text) > 200 or 'detailed' in text.lower():
        return 'intermediate'
    else:
        return 'beginner'

def is_high_quality(prompt_candidate: Dict) -> bool:
    """Check if a prompt candidate meets quality standards."""
    text = prompt_candidate.get('text', '')
    score = prompt_candidate.get('score', 0)
    
    # Quality criteria
    if len(text) < 50:  # Too short
        return False
    if score < 50:  # Low engagement
        return False
    if not any(char in text for char in ['[', '{', 'TOPIC', 'SUBJECT']):  # No variables
        # Allow if it's a complete, well-structured prompt
        if len(text) < 100:
            return False
    
    return True

def main():
    """Main scraping function."""
    print("🔍 Starting automated prompt scraping...")
    
    # Load existing prompts
    data = load_existing_prompts()
    existing_prompts = {p['prompt']: p for p in data['prompts']}
    new_prompts_added = 0
    
    # Scrape from all sources
    all_candidates = []
    
    # Reddit
    for url in SOURCES['reddit']:
        print(f"Scraping: {url}")
        candidates = scrape_reddit(url)
        all_candidates.extend(candidates)
    
    # Filter and process candidates
    for candidate in all_candidates:
        if not is_high_quality(candidate):
            continue
        
        prompt_text = candidate['text']
        
        # Check if already exists
        if prompt_text in existing_prompts:
            continue
        
        # Create new prompt entry
        category = categorize_prompt(prompt_text)
        difficulty = assess_difficulty(prompt_text)
        
        # Generate ID
        category_prompts = [p for p in data['prompts'] if p['category'] == category]
        next_id = len(category_prompts) + 1
        
        new_prompt = {
            'id': f"{category}-{next_id:03d}",
            'title': prompt_text[:50] + "..." if len(prompt_text) > 50 else prompt_text,
            'prompt': prompt_text,
            'description': f"Auto-discovered from {candidate['source']}",
            'category': category,
            'difficulty': difficulty,
            'rating': 4.0,  # Default rating
            'models': ['chatgpt', 'claude', 'gemini'],
            'tags': [],
            'use_cases': [],
            'copy_count': 0,
            'source': candidate.get('url', 'web'),
            'date_added': datetime.now().strftime('%Y-%m-%d')
        }
        
        data['prompts'].append(new_prompt)
        new_prompts_added += 1
        print(f"✅ Added: {new_prompt['title']}")
    
    # Update metadata
    data['total_prompts'] = len(data['prompts'])
    data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    
    # Save
    save_prompts(data)
    
    print(f"\n🎉 Scraping complete!")
    print(f"📊 New prompts added: {new_prompts_added}")
    print(f"📊 Total prompts: {data['total_prompts']}")

if __name__ == "__main__":
    main()
