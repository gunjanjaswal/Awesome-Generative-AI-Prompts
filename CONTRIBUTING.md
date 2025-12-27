# Contributing to Awesome Generative AI Prompts

Thank you for your interest in contributing! This guide will help you submit high-quality prompts.

## How to Contribute

### Submit a Prompt (Recommended)

The easiest way to contribute is through our GitHub issue template:

1. Go to [Issues](https://github.com/gunjanjaswal/Awesome-Generative-AI-Prompts/issues/new?template=submit-prompt.yml)
2. Click "New Issue" → "Submit a Prompt"
3. Fill out all required fields
4. Submit and wait for review

### Direct Pull Request

For multiple prompts or technical changes:

1. Fork the repository
2. Edit `prompts.json` to add your prompts
3. Follow the JSON structure (see below)
4. Submit a pull request

## Prompt Quality Guidelines

### ✅ Good Prompts

- **Specific and actionable**: Clear instructions with defined outcomes
- **Use variables**: Include [PLACEHOLDERS] for customization
- **Tested**: Verified with at least one AI model
- **Structured**: Use formatting (lists, sections, bold text)
- **Real use cases**: Solve actual problems
- **Examples included**: Show how to use it

### ❌ Avoid

- Too generic ("Write something about X")
- No variables or customization options
- Untested or theoretical prompts
- Duplicate of existing prompts
- Inappropriate or offensive content

## JSON Structure

When adding prompts to `prompts.json`:

```json
{
  "id": "category-###",
  "title": "Short Descriptive Title",
  "prompt": "The actual prompt text with [VARIABLES]...",
  "description": "Brief description of what this does",
  "category": "coding|content-creation|business|learning|creative|productivity|image-generation",
  "difficulty": "beginner|intermediate|advanced",
  "rating": 4.5,
  "models": ["chatgpt", "claude", "gemini"],
  "tags": ["tag1", "tag2", "tag3"],
  "use_cases": ["Use case 1", "Use case 2"],
  "copy_count": 0
}
```

## Review Process

1. **Submission**: Submit via issue or PR
2. **Review**: Maintainers review for quality
3. **Feedback**: You may be asked to make changes
4. **Approval**: Once approved, it's added to the collection
5. **README Update**: The README is regenerated automatically

## Recognition

All contributors are recognized in:
- GitHub contributors page
- Repository acknowledgements
- (Coming soon) Contributor leaderboard

## Questions?

Open an issue or reach out to the maintainers!

## Code of Conduct

Be respectful, constructive, and collaborative. We're building this together!


Thank you for your interest in contributing to the Awesome Generative AI Prompts repository! This document provides guidelines for contributing to this project.

## How to Contribute

### Adding New Prompts

While this repository is primarily updated through automated scripts, we welcome manual contributions of high-quality prompts.

To add a new prompt:

1. Fork the repository
2. Add your prompt to the appropriate category file in the `prompts` directory
3. Follow the existing table format
4. Submit a pull request

### Format for Prompts

Each prompt should include:

- **The prompt text**: The actual text of the prompt
- **Description**: A brief description of what the prompt does or generates
- **Category/Style**: The category or style of the prompt
- **Source**: Where you found or created the prompt
- **Date Added**: The date you're adding the prompt (YYYY-MM-DD)

For image generation prompts, also include:
- **Parameters**: Any specific parameters used with the prompt

### Creating a New Category

If you want to suggest a new category:

1. Create a new markdown file in the `prompts` directory
2. Follow the existing format of other category files
3. Add a link to the new category in the README.md
4. Submit a pull request

## Quality Guidelines

- Prompts should be effective and produce consistent results
- Avoid duplicating existing prompts
- Ensure prompts are appropriate and not offensive
- Provide clear descriptions of what the prompt does
- Test your prompts before submitting

## Code Contributions

If you want to improve the automation scripts:

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request with a clear description of your changes

## Issues and Suggestions

If you find a bug or have a suggestion:

1. Check if the issue already exists
2. Create a new issue with a clear title and description
3. Include steps to reproduce if reporting a bug
4. Label the issue appropriately

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a positive community

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
