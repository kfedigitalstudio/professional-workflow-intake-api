const intakeText = document.getElementById('intakeText');
const charCount = document.getElementById('charCount');
const processButton = document.getElementById('processButton');
const sampleButton = document.getElementById('sampleButton');
const clearButton = document.getElementById('clearButton');
const formMessage = document.getElementById('formMessage');
const emptyState = document.getElementById('emptyState');
const results = document.getElementById('results');
const resultState = document.getElementById('resultState');
const summaryText = document.getElementById('summaryText');
const contactsList = document.getElementById('contactsList');
const datesList = document.getElementById('datesList');
const actionsList = document.getElementById('actionsList');
const actionCount = document.getElementById('actionCount');
const engineStatus = document.getElementById('engineStatus');
const engineDetail = document.getElementById('engineDetail');
const statusDot = document.getElementById('statusDot');

const PYODIDE_BASE = 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/';
let pyodide = null;
let parseWorkflowJson = null;

const sampleText = `Client email: maria.santos@example.com
Phone: (317) 555-0148
Meeting date: October 6, 2026
- Call client today to confirm missing documents.
- Review supporting records by October 8, 2026.
- Submit completed packet by October 15, 2026.`;

function updateCharCount() {
  const count = intakeText.value.length;
  charCount.textContent = `${count} ${count === 1 ? 'character' : 'characters'}`;
}

function clearNode(node) {
  while (node.firstChild) node.removeChild(node.firstChild);
}

function addPill(container, value) {
  const pill = document.createElement('span');
  pill.className = 'data-pill';
  pill.textContent = value;
  container.appendChild(pill);
}

function displayDate(value) {
  if (!value) return '';
  const parsed = new Date(`${value}T00:00:00`);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

function renderResults(data) {
  clearNode(contactsList);
  clearNode(datesList);
  clearNode(actionsList);

  const emails = data.contact?.emails ?? [];
  const phones = data.contact?.phone_numbers ?? [];
  emails.forEach((email) => addPill(contactsList, email));
  phones.forEach((phone) => addPill(contactsList, phone));

  (data.dates_mentioned ?? []).forEach((date) => addPill(datesList, displayDate(date)));

  const actions = data.action_items ?? [];
  actions.forEach((action) => {
    const row = document.createElement('div');
    row.className = 'action-row';

    const description = document.createElement('p');
    description.className = 'action-description';
    description.textContent = action.description;

    const meta = document.createElement('div');
    meta.className = 'action-meta';

    const priority = document.createElement('span');
    priority.className = `badge${action.priority === 'high' ? ' high' : ''}`;
    priority.textContent = action.priority === 'high' ? 'HIGH PRIORITY' : 'NORMAL';
    meta.appendChild(priority);

    if (action.due_date) {
      const due = document.createElement('span');
      due.className = 'badge';
      due.textContent = `DUE ${displayDate(action.due_date).toUpperCase()}`;
      meta.appendChild(due);
    }

    row.append(description, meta);
    actionsList.appendChild(row);
  });

  summaryText.textContent = data.summary || 'No summary returned.';
  actionCount.textContent = `${actions.length} ${actions.length === 1 ? 'item' : 'items'}`;
  emptyState.classList.add('hidden');
  results.classList.remove('hidden');
  resultState.textContent = 'Parsed with Python';
}

async function initializePython() {
  try {
    pyodide = await loadPyodide({ indexURL: PYODIDE_BASE });
    const response = await fetch('parser.py', { cache: 'no-store' });
    if (!response.ok) throw new Error(`Could not load parser.py (${response.status})`);

    const parserSource = await response.text();
    await pyodide.runPythonAsync(parserSource);
    parseWorkflowJson = pyodide.globals.get('parse_workflow_json');

    engineStatus.textContent = 'Python ready';
    engineDetail.textContent = 'Running locally in this browser with Pyodide.';
    statusDot.classList.remove('loading');
    processButton.disabled = false;
    processButton.firstElementChild.textContent = 'Process intake';
  } catch (error) {
    console.error(error);
    engineStatus.textContent = 'Python failed to load';
    engineDetail.textContent = 'Refresh the page and check your internet connection.';
    statusDot.classList.remove('loading');
    statusDot.classList.add('error');
    processButton.disabled = true;
    processButton.firstElementChild.textContent = 'Python unavailable';
    formMessage.textContent = 'The browser Python runtime could not initialize.';
  }
}

async function processIntake() {
  const text = intakeText.value.trim();
  formMessage.textContent = '';

  if (!text) {
    formMessage.textContent = 'Enter or load intake notes before processing.';
    intakeText.focus();
    return;
  }

  if (!parseWorkflowJson) {
    formMessage.textContent = 'Python is still loading. Please try again in a moment.';
    return;
  }

  processButton.disabled = true;
  processButton.firstElementChild.textContent = 'Processing…';
  resultState.textContent = 'Running Python';

  try {
    const jsonResult = parseWorkflowJson(text);
    const data = JSON.parse(jsonResult);
    renderResults(data);
  } catch (error) {
    console.error(error);
    formMessage.textContent = 'Python could not process this note. Please try another input.';
    resultState.textContent = 'Processing failed';
  } finally {
    processButton.disabled = false;
    processButton.firstElementChild.textContent = 'Process intake';
  }
}

intakeText.addEventListener('input', updateCharCount);
processButton.addEventListener('click', processIntake);
sampleButton.addEventListener('click', () => {
  intakeText.value = sampleText;
  updateCharCount();
  formMessage.textContent = '';
  intakeText.focus();
});
clearButton.addEventListener('click', () => {
  intakeText.value = '';
  updateCharCount();
  formMessage.textContent = '';
  emptyState.classList.remove('hidden');
  results.classList.add('hidden');
  resultState.textContent = 'Waiting for input';
  intakeText.focus();
});

updateCharCount();
initializePython();
