const PROMPTS_URL = 'https://raw.githubusercontent.com/gunjanjaswal/Awesome-Generative-AI-Prompts/main/prompts.json';

let allPrompts = [];
let filteredPrompts = [];
let currentCategory = 'all';

// Load prompts on popup open
document.addEventListener('DOMContentLoaded', async () => {
    await loadPrompts();
    renderCategories();
    renderPrompts();

    // Setup search
    document.getElementById('searchInput').addEventListener('input', (e) => {
        filterPrompts(e.target.value);
    });
});

async function loadPrompts() {
    try {
        // Try to get from cache first
        const cached = await chrome.storage.local.get(['prompts', 'lastUpdate']);
        const now = Date.now();
        const cacheAge = now - (cached.lastUpdate || 0);

        // Use cache if less than 24 hours old
        if (cached.prompts && cacheAge < 24 * 60 * 60 * 1000) {
            allPrompts = cached.prompts.prompts;
            filteredPrompts = allPrompts;
            return;
        }

        // Fetch fresh data
        const response = await fetch(PROMPTS_URL);
        const data = await response.json();
        allPrompts = data.prompts;
        filteredPrompts = allPrompts;

        // Cache the data
        await chrome.storage.local.set({
            prompts: data,
            lastUpdate: now
        });
    } catch (error) {
        console.error('Error loading prompts:', error);
        showError('Failed to load prompts. Please try again.');
    }
}

function renderCategories() {
    const categoriesEl = document.getElementById('categories');
    const categories = ['all', ...new Set(allPrompts.map(p => p.category))];

    categoriesEl.innerHTML = categories.map(cat => `
    <button class="category-btn ${cat === currentCategory ? 'active' : ''}" 
            data-category="${cat}">
      ${cat === 'all' ? '📋 All' : cat.replace('-', ' ')}
    </button>
  `).join('');

    // Add click handlers
    categoriesEl.querySelectorAll('.category-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            currentCategory = btn.dataset.category;
            document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterPrompts(document.getElementById('searchInput').value);
        });
    });
}

function filterPrompts(query) {
    filteredPrompts = allPrompts.filter(p => {
        const matchesCategory = currentCategory === 'all' || p.category === currentCategory;
        const matchesSearch = !query ||
            p.title.toLowerCase().includes(query.toLowerCase()) ||
            p.description.toLowerCase().includes(query.toLowerCase()) ||
            p.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()));

        return matchesCategory && matchesSearch;
    });

    renderPrompts();
}

function renderPrompts() {
    const promptsList = document.getElementById('promptsList');

    if (filteredPrompts.length === 0) {
        promptsList.innerHTML = `
      <div class="empty-state">
        <p>No prompts found</p>
        <p style="font-size: 12px; margin-top: 10px;">Try a different search or category</p>
      </div>
    `;
        return;
    }

    promptsList.innerHTML = filteredPrompts.map(prompt => `
    <div class="prompt-card" data-id="${prompt.id}">
      <div class="prompt-title">${prompt.title}</div>
      <div class="prompt-meta">
        ${getDifficultyEmoji(prompt.difficulty)} ${prompt.difficulty} • 
        ${'⭐'.repeat(Math.round(prompt.rating))}
      </div>
      <div class="prompt-description">${prompt.description}</div>
      <button class="copy-btn" data-prompt="${escapeHtml(prompt.prompt)}">
        📋 Copy Prompt
      </button>
    </div>
  `).join('');

    // Add click handlers for copy buttons
    promptsList.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const prompt = btn.dataset.prompt;
            await copyToClipboard(prompt);
            btn.textContent = '✓ Copied!';
            setTimeout(() => {
                btn.textContent = '📋 Copy Prompt';
            }, 2000);
        });
    });

    // Add click handlers for cards (to insert into page)
    promptsList.querySelectorAll('.prompt-card').forEach(card => {
        card.addEventListener('click', async () => {
            const promptId = card.dataset.id;
            const prompt = allPrompts.find(p => p.id === promptId);
            await insertPromptIntoPage(prompt.prompt);
            window.close();
        });
    });
}

function getDifficultyEmoji(difficulty) {
    const map = {
        'beginner': '🟢',
        'intermediate': '🟡',
        'advanced': '🔴'
    };
    return map[difficulty] || '⚪';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
    } catch (err) {
        console.error('Failed to copy:', err);
    }
}

async function insertPromptIntoPage(prompt) {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        await chrome.tabs.sendMessage(tab.id, {
            action: 'insertPrompt',
            prompt: prompt
        });
    } catch (err) {
        console.error('Failed to insert prompt:', err);
        await copyToClipboard(prompt);
    }
}

function showError(message) {
    const promptsList = document.getElementById('promptsList');
    promptsList.innerHTML = `
    <div class="empty-state">
      <p>⚠️ ${message}</p>
    </div>
  `;
}
