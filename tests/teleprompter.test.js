#!/usr/bin/env node
/**
 * Quick integrity checks for the HTML teleprompter assets.
 *
 * Usage: node tests/teleprompter.test.js
 * Example: npm test -- teleprompter.test.js
 */
const fs = require('fs');
const path = require('path');
const assert = require('assert');

function readProjectFile(relativePath) {
  const target = path.join(__dirname, '..', relativePath);
  return fs.readFileSync(target, 'utf8');
}

try {
  const indexHtml = readProjectFile('public/index.html');
  const manifestRaw = readProjectFile('public/docs/list.json');
  const manifest = JSON.parse(manifestRaw);
  const defaultDocName = 'demo-list.txt';
  const defaultDocPath = path.join(__dirname, '..', 'public', 'docs', defaultDocName);

  // HTML surface sanity checks
  [
    'controlToggleCluster',
    'fileSelect',
    'content',
    'docsFileName',
    'addDocBtn',
    'playBtn',
    'collapsedPlayBtn',
    'projectSelect',
    'projectScriptSelect',
    'saveProjectScriptBtn',
  ].forEach((id) => {
    assert(
      indexHtml.includes(`id="${id}"`),
      `Expected teleprompter UI element with id="${id}" in index.html`
    );
  });

  assert(
    indexHtml.indexOf('id="collapsedControls"') < indexHtml.indexOf('id="toggleControlsBtn"'),
    'Collapsed quick controls should render to the left of the show/hide button for aligned toggles'
  );

  assert(
    indexHtml.includes('DEFAULT_DOC_CONTENT'),
    'Fallback inline demo transcript must be present for preview reliability'
  );
  assert(
    indexHtml.includes('shouldPersistSource'),
    'Teleprompter should guard which transcript sources persist to local storage'
  );
  assert(
    indexHtml.includes('normalizeSource'),
    'Teleprompter should normalize transcript sources when loading saved data'
  );
  assert(
    indexHtml.includes('/api/docs/list'),
    'Teleprompter should request /api/docs/list to refresh docs manifests without a build step'
  );

  // Manifest and docs directory checks
  assert(Array.isArray(manifest), 'docs/list.json must be a JSON array');
  assert(manifest.length > 0, 'docs/list.json must list at least one transcript');
  assert(
    manifest.includes(defaultDocName),
    `docs/list.json should reference the default ${defaultDocName} transcript`
  );

  assert(fs.existsSync(defaultDocPath), `${defaultDocName} should exist in docs/`);

  console.log('All teleprompter integrity checks passed.');
} catch (error) {
  console.error('Test failure:', error.message);
  process.exitCode = 1;
}
