# Browser Extension

A Chrome/Firefox extension for quick access to AI prompts directly in your browser.

## Features

- 🚀 **Quick Access**: Popup interface with search and filters
- 📋 **One-Click Copy**: Copy prompts to clipboard instantly
- ✨ **Auto-Insert**: Automatically insert prompts into ChatGPT, Claude, or Gemini
- 🎨 **Beautiful UI**: Modern, gradient design with smooth animations
- 💾 **Offline Cache**: Works offline with cached prompts
- 🔍 **Smart Search**: Find prompts by title, description, or tags
- 🏷️ **Category Filters**: Browse by category

## Installation

### Chrome/Edge

1. Download or clone this repository
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode" (top right)
4. Click "Load unpacked"
5. Select the `browser-extension` folder

### Firefox

1. Download or clone this repository
2. Open Firefox and go to `about:debugging#/runtime/this-firefox`
3. Click "Load Temporary Add-on"
4. Select the `manifest.json` file in the `browser-extension` folder

## Usage

### Basic Usage

1. Click the extension icon in your browser toolbar
2. Search or browse for a prompt
3. Click "Copy Prompt" to copy to clipboard
4. Or click the prompt card to auto-insert into the active AI chat

### On AI Platforms

When using ChatGPT, Claude, or Gemini:
1. Click the extension icon
2. Select a prompt
3. It will automatically insert into the chat input
4. Customize the variables and send!

### Keyboard Shortcut (Coming Soon)

- `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac) to open prompts

## Supported Platforms

- ✅ ChatGPT (chat.openai.com)
- ✅ Claude (claude.ai)
- ✅ Gemini (gemini.google.com)

## Privacy

This extension:
- ✅ Does NOT collect any personal data
- ✅ Does NOT track your usage
- ✅ Only accesses AI chat pages to insert prompts
- ✅ Caches prompts locally for offline use
- ✅ Fetches prompts from GitHub (public repository)

## Development

### Structure

```
browser-extension/
├── manifest.json       # Extension configuration
├── popup.html         # Popup interface
├── popup.js           # Popup logic
├── content.js         # Content script for AI sites
├── background.js      # Background service worker
└── icons/             # Extension icons
```

### Building

No build step required! The extension uses vanilla JavaScript.

### Testing

1. Load the extension in developer mode
2. Open ChatGPT, Claude, or Gemini
3. Click the extension icon
4. Test prompt insertion

## Contributing

Found a bug or have a feature request? Please open an issue on GitHub!

## License

MIT License - see LICENSE file for details
