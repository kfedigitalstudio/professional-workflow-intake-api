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
  resultState.textContent = 'Parsed successfully';
}

async function processIntake() {
  const text = intakeText.value.trim();
  formMessage.textContent = '';

  if (!text) {
    formMessage.textContent = 'Enter or load intake notes before processing.';
    intakeText.focus();
    return;
  }

  processButton.disabled = true;
  processButton.firstElementChild.textContent = 'Processing…';
  resultState.textContent = 'Processing';

  try {
    const response = await fetch('/parse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    renderResults(await response.json());
  } catch (error) {
    console.error(error);
    formMessage.textContent = 'The API could not process this note. Please try again.';
    resultState.textContent = 'Request failed';
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
