#!/usr/bin/env node

/**
 * spectrace-init
 * Zero-dependency CLI utility to initialize or upgrade Spectrace in a target repository.
 * Pure Markdown & Git — zero daemons or fragile git hooks.
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, cpSync } from 'node:fs';
import { resolve, join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT_DIR = resolve(__dirname, '..');
const ASSETS_DIR = resolve(ROOT_DIR, 'skills/spectrace-plan/assets');

const CONTRACT_FILES = [
  'PRODUCT.md',
  'ARCHITECTURE.md',
  'ENGINEERING.md',
  'DESIGN.md',
  'TESTING.md',
  'CHANGES.md',
  'AGENTS.md'
];

function printHelp() {
  console.log(`
spectrace-init — Initialize or upgrade Spectrace governance in any repository

Usage:
  node bin/spectrace-init.mjs [target-dir] [options]
  npx spectrace-init [target-dir] [options]

Options:
  --type <ui|docs|backend>   Specify context-aware design type (default: auto-detect)
  --upgrade                  Run migration/upgrade mode on an existing Spectrace repo
  --dry-run                  Preview actions without writing files
  --help, -h                 Show this help message

Examples:
  node bin/spectrace-init.mjs .
  node bin/spectrace-init.mjs ../my-project --type ui
  node bin/spectrace-init.mjs . --upgrade
`);
}

function detectProjectType(targetDir) {
  const pkgPath = join(targetDir, 'package.json');
  if (existsSync(pkgPath)) {
    try {
      const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
      const deps = { ...pkg.dependencies, ...pkg.devDependencies };
      if (deps['react'] || deps['vue'] || deps['svelte'] || deps['next'] || deps['vite'] || deps['tailwindcss']) {
        return 'ui';
      }
      if (deps['docusaurus'] || deps['vitepress'] || deps['astro']) {
        return 'docs';
      }
    } catch {
      // Ignore JSON parse errors
    }
  }

  // Check for common doc or UI indicators
  if (existsSync(join(targetDir, 'docs')) || existsSync(join(targetDir, 'mkdocs.yml'))) {
    return 'docs';
  }

  return 'backend';
}

function run() {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) {
    printHelp();
    process.exit(0);
  }

  const isDryRun = args.includes('--dry-run');
  const isUpgrade = args.includes('--upgrade');
  let customType = null;

  const typeIndex = args.indexOf('--type');
  if (typeIndex !== -1 && args[typeIndex + 1]) {
    customType = args[typeIndex + 1].toLowerCase();
  }

  const targetArg = args.find(a => !a.startsWith('-')) || '.';
  const targetDir = resolve(process.cwd(), targetArg);

  if (!existsSync(targetDir)) {
    console.error(`Error: Target directory does not exist: ${targetDir}`);
    process.exit(1);
  }

  console.log(`\n🚀 Spectrace: Initializing / Upgrading in: ${targetDir}`);
  if (isDryRun) console.log(`[DRY-RUN MODE: No files will be written]\n`);

  const detectedType = customType || detectProjectType(targetDir);
  console.log(`📦 Context-Aware Design archetype: [${detectedType}]`);

  const hasAgents = existsSync(join(targetDir, 'AGENTS.md'));
  const hasPlanning = existsSync(join(targetDir, 'planning'));
  const mode = (isUpgrade || hasAgents || hasPlanning) ? 'UPGRADE' : 'GREENFIELD';

  console.log(`🔍 Mode: ${mode}\n`);

  const created = [];
  const updated = [];
  const skipped = [];

  function safeWrite(relPath, content) {
    const fullPath = join(targetDir, relPath);
    const parent = dirname(fullPath);
    if (!existsSync(parent) && !isDryRun) {
      mkdirSync(parent, { recursive: true });
    }

    if (existsSync(fullPath)) {
      if (mode === 'UPGRADE') {
        // In upgrade mode, we don't overwrite user content blindly
        skipped.push(`${relPath} (already exists, preserved)`);
      } else {
        skipped.push(`${relPath} (already exists)`);
      }
    } else {
      if (!isDryRun) {
        writeFileSync(fullPath, content.trim() + '\n', 'utf8');
      }
      created.push(relPath);
    }
  }

  // 1. Scaffold missing root contracts
  const templates = {
    'PRODUCT.md': join(ASSETS_DIR, 'product-template.md'),
    'ARCHITECTURE.md': join(ASSETS_DIR, 'architecture-template.md'),
    'ENGINEERING.md': join(ASSETS_DIR, 'engineering-template.md'),
    'DESIGN.md': detectedType === 'docs' 
      ? join(ASSETS_DIR, 'design-docs-template.md') 
      : join(ASSETS_DIR, 'design-template.md'),
    'TESTING.md': join(ASSETS_DIR, 'testing-template.md'),
    'CHANGES.md': join(ASSETS_DIR, 'changes-template.md'),
    'AGENTS.md': join(ASSETS_DIR, 'agents-block.md'),
    '.agentignore': join(ASSETS_DIR, 'agentignore-template')
  };

  for (const [file, templatePath] of Object.entries(templates)) {
    if (existsSync(templatePath)) {
      const content = readFileSync(templatePath, 'utf8');
      safeWrite(file, content);
    }
  }

  // 2. Scaffold planning/roadmap.md if missing
  const roadmapPath = join(targetDir, 'planning/roadmap.md');
  if (!existsSync(roadmapPath)) {
    const roadmapTemplate = `# Roadmap

Specs in execution order. \`Status\` (\`todo\`, \`in progress\`, \`done\`) is maintained directly by agents and humans as specs progress.

| ID  | Spec | Status | Depends on |
|-----|------|--------|------------|

## Ideas

Anything worth doing later, including small fixes not done right away. Ideas can be added freely without debate; they are converted into specs (or fixed directly, if trivial) when prioritized.
`;
    safeWrite('planning/roadmap.md', roadmapTemplate);
  }

  // 3. Ensure planning/specs directory exists
  const specsDir = join(targetDir, 'planning/specs');
  if (!existsSync(specsDir) && !isDryRun) {
    mkdirSync(specsDir, { recursive: true });
    created.push('planning/specs/');
  }

  // 4. In UPGRADE mode, record migration entry in CHANGES.md if possible
  if (mode === 'UPGRADE') {
    const changesPath = join(targetDir, 'CHANGES.md');
    const today = new Date().toISOString().split('T')[0];
    const migrationEntry = `| ${today} | Governance | Upgraded repository to Spectrace 7-contract progressive disclosure suite | Standardize decoupled contracts |\n`;

    if (existsSync(changesPath) && !isDryRun) {
      const currentChanges = readFileSync(changesPath, 'utf8');
      if (!currentChanges.includes('Upgraded repository to Spectrace 7-contract')) {
        const tableHeader = '| Date | Scope | What changed | Why |\n|:---|:---|:---|:---|';
        if (currentChanges.includes(tableHeader)) {
          const updatedContent = currentChanges.replace(tableHeader, `${tableHeader}\n${migrationEntry.trim()}`);
          writeFileSync(changesPath, updatedContent, 'utf8');
          updated.push('CHANGES.md (added upgrade entry)');
        }
      }
    }
  }

  // Output summary
  console.log('--- Summary of Changes ---');
  if (created.length > 0) {
    console.log(`\n✨ Created:`);
    created.forEach(f => console.log(`  + ${f}`));
  }
  if (updated.length > 0) {
    console.log(`\n📝 Updated:`);
    updated.forEach(f => console.log(`  ~ ${f}`));
  }
  if (skipped.length > 0) {
    console.log(`\n🔒 Preserved / Unchanged:`);
    skipped.forEach(f => console.log(`  . ${f}`));
  }

  console.log(`\n✅ Spectrace successfully configured!`);
  console.log(`Next step: Run 'spectrace-plan' with your agent or review your newly scaffolded contracts in the root directory.\n`);
}

run();
