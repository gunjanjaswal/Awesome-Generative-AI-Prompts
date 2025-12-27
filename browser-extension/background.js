// Background service worker for the extension

chrome.runtime.onInstalled.addListener(() => {
    // Create context menu
    chrome.contextMenus.create({
        id: 'insertPrompt',
        title: 'Insert AI Prompt',
        contexts: ['editable']
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'insertPrompt') {
        // Open popup to select prompt
        chrome.action.openPopup();
    }
});

// Handle keyboard shortcuts (if defined in manifest)
chrome.commands.onCommand.addListener((command) => {
    if (command === 'open-prompts') {
        chrome.action.openPopup();
    }
});
