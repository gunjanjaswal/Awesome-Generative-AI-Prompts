# Automated Daily Updates

This repository automatically updates with new high-quality prompts every day!

## How It Works

### 1. **Automated Scraping** 🤖
- GitHub Actions runs daily at 00:00 UTC
- Scrapes prompts from:
  - Reddit (r/ChatGPT, r/ClaudeAI, r/PromptEngineering)
  - Top posts from the past week
  - Posts with high engagement (50+ upvotes)

### 2. **Quality Filtering** ✅
Each prompt is evaluated for:
- **Length**: 50-2000 characters
- **Engagement**: Minimum 50 upvotes
- **Structure**: Contains variables or well-structured
- **Uniqueness**: Not already in collection

### 3. **Auto-Categorization** 🏷️
Prompts are automatically categorized based on keywords:
- Coding & Development
- Content Creation
- Business & Professional
- Learning & Education
- Creative & Storytelling
- Productivity & Planning
- Image Generation

### 4. **Commit & Push** 📤
- New prompts added to `prompts.json`
- Automatic commit with date
- Pushed to repository
- Workflow stays active with keepalive mechanism

## Workflow File

See [`.github/workflows/daily-update.yml`](../.github/workflows/daily-update.yml)

## Scraper Script

See [`scripts/scrape_prompts.py`](../scripts/scrape_prompts.py)

## Manual Trigger

You can manually trigger the workflow:
1. Go to Actions tab on GitHub
2. Select "Daily Prompt Updates"
3. Click "Run workflow"

## Adding More Sources

To add more scraping sources, edit `scripts/scrape_prompts.py`:

```python
SOURCES = {
    "reddit": [
        # Add more subreddits
    ],
    "twitter": [
        # Add Twitter search queries
    ],
    "github": [
        # Add GitHub repo searches
    ]
}
```

## Community Contributions

While the repository auto-updates daily, **community contributions are still welcome!**

Submit prompts via:
- [GitHub Issues](https://github.com/gunjanjaswal/Awesome-Generative-AI-Prompts/issues/new?template=submit-prompt.yml)
- Pull requests to `prompts.json`

Community-submitted prompts are manually reviewed for quality and added with proper attribution.

## Benefits

✅ **Always Fresh**: New prompts added automatically  
✅ **Quality Controlled**: Only high-engagement prompts  
✅ **No Manual Work**: Fully automated  
✅ **Community Driven**: Both automated and manual submissions  
✅ **Transparent**: All changes visible in commit history

## Monitoring

Check the [Actions tab](https://github.com/gunjanjaswal/Awesome-Generative-AI-Prompts/actions) to see:
- Daily workflow runs
- Number of prompts added
- Any errors or issues

---

**Last Updated**: Automatically updated daily via GitHub Actions
