#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const https = require('https');

const PROMPTS_URL = 'https://raw.githubusercontent.com/gunjanjaswal/Awesome-Generative-AI-Prompts/main/prompts.json';
const CACHE_FILE = path.join(__dirname, '.prompts-cache.json');
const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours

// ANSI color codes
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    green: '\x1b[32m',
    blue: '\x1b[34m',
    yellow: '\x1b[33m',
    cyan: '\x1b[36m',
    red: '\x1b[31m'
};

async function fetchPrompts() {
    // Check cache first
    if (fs.existsSync(CACHE_FILE)) {
        const cache = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
        if (Date.now() - cache.timestamp < CACHE_DURATION) {
            return cache.data;
        }
    }

    // Fetch from GitHub
    return new Promise((resolve, reject) => {
        https.get(PROMPTS_URL, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                const prompts = JSON.parse(data);
                // Cache the data
                fs.writeFileSync(CACHE_FILE, JSON.stringify({
                    timestamp: Date.now(),
                    data: prompts
                }));
                resolve(prompts);
            });
        }).on('error', reject);
    });
}

function displayPrompt(prompt) {
    console.log(`\n${colors.bright}${colors.blue}${prompt.title}${colors.reset}`);
    console.log(`${colors.cyan}ID: ${prompt.id}${colors.reset}`);
    console.log(`${colors.yellow}Category: ${prompt.category} | Difficulty: ${prompt.difficulty}${colors.reset}`);
    console.log(`${colors.green}Rating: ${'⭐'.repeat(Math.round(prompt.rating))} (${prompt.rating})${colors.reset}`);
    console.log(`\n${prompt.description}`);
    console.log(`\n${colors.bright}Prompt:${colors.reset}`);
    console.log(prompt.prompt);
    if (prompt.use_cases) {
        console.log(`\n${colors.cyan}Use Cases:${colors.reset} ${prompt.use_cases.join(', ')}`);
    }
    console.log('─'.repeat(80));
}

async function searchPrompts(query) {
    const data = await fetchPrompts();
    const results = data.prompts.filter(p =>
        p.title.toLowerCase().includes(query.toLowerCase()) ||
        p.description.toLowerCase().includes(query.toLowerCase()) ||
        p.category.toLowerCase().includes(query.toLowerCase()) ||
        p.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
    );

    if (results.length === 0) {
        console.log(`${colors.red}No prompts found matching "${query}"${colors.reset}`);
        return;
    }

    console.log(`${colors.green}Found ${results.length} prompt(s):${colors.reset}`);
    results.forEach(displayPrompt);
}

async function getPromptById(id) {
    const data = await fetchPrompts();
    const prompt = data.prompts.find(p => p.id === id);

    if (!prompt) {
        console.log(`${colors.red}Prompt with ID "${id}" not found${colors.reset}`);
        return;
    }

    displayPrompt(prompt);
}

async function copyPrompt(id) {
    const data = await fetchPrompts();
    const prompt = data.prompts.find(p => p.id === id);

    if (!prompt) {
        console.log(`${colors.red}Prompt with ID "${id}" not found${colors.reset}`);
        return;
    }

    // Copy to clipboard (requires clipboard package)
    try {
        const clipboardy = require('clipboardy');
        await clipboardy.write(prompt.prompt);
        console.log(`${colors.green}✓ Copied "${prompt.title}" to clipboard!${colors.reset}`);
    } catch (err) {
        console.log(`${colors.yellow}Clipboard not available. Here's the prompt:${colors.reset}`);
        console.log(prompt.prompt);
    }
}

async function listByCategory(category) {
    const data = await fetchPrompts();
    const results = data.prompts.filter(p =>
        p.category.toLowerCase() === category.toLowerCase()
    );

    if (results.length === 0) {
        console.log(`${colors.red}No prompts found in category "${category}"${colors.reset}`);
        console.log(`\nAvailable categories:`);
        Object.entries(data.categories).forEach(([key, value]) => {
            console.log(`  ${colors.cyan}${key}${colors.reset}: ${value}`);
        });
        return;
    }

    console.log(`${colors.green}${results.length} prompt(s) in "${category}":${colors.reset}`);
    results.forEach(displayPrompt);
}

async function randomPrompt(category) {
    const data = await fetchPrompts();
    let prompts = data.prompts;

    if (category) {
        prompts = prompts.filter(p => p.category.toLowerCase() === category.toLowerCase());
    }

    if (prompts.length === 0) {
        console.log(`${colors.red}No prompts found${colors.reset}`);
        return;
    }

    const random = prompts[Math.floor(Math.random() * prompts.length)];
    console.log(`${colors.green}🎲 Random Prompt:${colors.reset}`);
    displayPrompt(random);
}

function showHelp() {
    console.log(`
${colors.bright}${colors.blue}Awesome AI Prompts CLI${colors.reset}

${colors.bright}Usage:${colors.reset}
  prompts <command> [options]

${colors.bright}Commands:${colors.reset}
  ${colors.cyan}search <query>${colors.reset}          Search prompts by keyword
  ${colors.cyan}get <id>${colors.reset}                Get a specific prompt by ID
  ${colors.cyan}copy <id>${colors.reset}               Copy a prompt to clipboard
  ${colors.cyan}list <category>${colors.reset}         List prompts in a category
  ${colors.cyan}random [category]${colors.reset}       Get a random prompt
  ${colors.cyan}help${colors.reset}                    Show this help message

${colors.bright}Examples:${colors.reset}
  prompts search "code review"
  prompts get code-001
  prompts copy code-001
  prompts list coding
  prompts random coding

${colors.bright}Categories:${colors.reset}
  coding, content-creation, business, learning,
  creative, productivity, image-generation
`);
}

// Main CLI logic
async function main() {
    const args = process.argv.slice(2);
    const command = args[0];

    try {
        switch (command) {
            case 'search':
                if (!args[1]) {
                    console.log(`${colors.red}Please provide a search query${colors.reset}`);
                    return;
                }
                await searchPrompts(args[1]);
                break;

            case 'get':
                if (!args[1]) {
                    console.log(`${colors.red}Please provide a prompt ID${colors.reset}`);
                    return;
                }
                await getPromptById(args[1]);
                break;

            case 'copy':
                if (!args[1]) {
                    console.log(`${colors.red}Please provide a prompt ID${colors.reset}`);
                    return;
                }
                await copyPrompt(args[1]);
                break;

            case 'list':
                if (!args[1]) {
                    console.log(`${colors.red}Please provide a category${colors.reset}`);
                    return;
                }
                await listByCategory(args[1]);
                break;

            case 'random':
                await randomPrompt(args[1]);
                break;

            case 'help':
            default:
                showHelp();
        }
    } catch (error) {
        console.error(`${colors.red}Error: ${error.message}${colors.reset}`);
    }
}

main();
