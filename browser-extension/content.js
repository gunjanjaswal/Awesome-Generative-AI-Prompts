// Content script to insert prompts into AI chat interfaces

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'insertPrompt') {
        insertPromptIntoTextarea(request.prompt);
        sendResponse({ success: true });
    }
    return true;
});

function insertPromptIntoTextarea(prompt) {
    // Try to find the textarea/input field on different AI platforms
    const selectors = [
        'textarea[placeholder*="message"]', // ChatGPT
        'textarea[placeholder*="Message"]', // ChatGPT
        'div[contenteditable="true"]', // Claude
        'textarea', // Generic fallback
        'input[type="text"]' // Generic fallback
    ];

    for (const selector of selectors) {
        const element = document.querySelector(selector);
        if (element) {
            // Set the value
            if (element.tagName === 'TEXTAREA' || element.tagName === 'INPUT') {
                element.value = prompt;
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
            } else if (element.contentEditable === 'true') {
                element.textContent = prompt;
                element.dispatchEvent(new Event('input', { bubbles: true }));
            }

            // Focus the element
            element.focus();

            // Trigger any necessary events for the platform
            const inputEvent = new InputEvent('input', {
                bubbles: true,
                cancelable: true,
            });
            element.dispatchEvent(inputEvent);

            return true;
        }
    }

    // If no textarea found, copy to clipboard as fallback
    navigator.clipboard.writeText(prompt);
    showNotification('Prompt copied to clipboard!');
    return false;
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 10000;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 14px;
    animation: slideIn 0.3s ease-out;
  `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from {
      transform: translateX(400px);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(400px);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);
