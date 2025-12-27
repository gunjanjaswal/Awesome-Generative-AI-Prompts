# CLI Tool

A command-line interface for quick access to AI prompts.

## Installation

```bash
npm install -g awesome-ai-prompts-cli
```

Or use directly with npx:
```bash
npx awesome-ai-prompts-cli search "code review"
```

## Usage

### Search for prompts
```bash
prompts search "code review"
prompts search "email"
```

### Get a specific prompt
```bash
prompts get code-001
```

### Copy prompt to clipboard
```bash
prompts copy code-001
```

### List prompts by category
```bash
prompts list coding
prompts list business
```

### Get a random prompt
```bash
prompts random
prompts random coding
```

## Available Categories

- `coding` - Code Generation & Debugging
- `content-creation` - Writing & Content
- `business` - Business & Professional
- `learning` - Education & Learning
- `creative` - Creative & Storytelling
- `productivity` - Productivity & Planning
- `image-generation` - Image Generation

## Features

- 🚀 Fast and lightweight
- 📋 Copy to clipboard support
- 🎨 Colorful output
- 💾 Local caching for speed
- 🔍 Powerful search
- 🎲 Random prompt generator

## Examples

```bash
# Find all coding-related prompts
prompts search code

# Get the expert code reviewer prompt
prompts get code-001

# Copy it to clipboard
prompts copy code-001

# Get a random creative writing prompt
prompts random creative
```
