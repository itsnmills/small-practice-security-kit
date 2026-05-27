let csrfToken = "";
let catalogs = null;
let profile = null;
let connectorState = null;
let incidentScenarios = [];
let selectedPreset = "dental";

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

function showAlert(message, isError = true) {
  const alert = $("#alert");
  alert.hidden = false;
  alert.textContent = message;
  alert.style.background = isError ? "var(--danger-soft)" : "var(--success-soft)";
  alert.style.color = isError ? "var(--danger)" : "var(--success)";
}

function clearAlert() {
  $("#alert").hidden = true;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-SPSK-Token": csrfToken,
      ...(options.headers || {}),
    },
  });
  const data = await response.json();
  if (!response.ok || data.ok === false) {
    const extra = data.findings ? ` ${data.findings.map((f) => `${f.path}: ${f.message}`).join("; ")}` : "";
    throw new Error(`${data.error || "Request failed"}${extra}`);
  }
  return data;
}

function navTo(section) {
  $$(".rail button").forEach((button) => button.classList.toggle("active", button.dataset.section === section));
  $$(".intake-section").forEach((panel) => panel.classList.toggle("active", panel.id === `section-${section}`));
  clearAlert();
}

function textInput(value, path, type = "text") {
  return `<input type="${type}" value="${escapeHtml(value ?? "")}" data-path="${path}">`;
}

function textareaInput(value, path, extra = "") {
  return `<textarea data-path="${path}" ${extra}>${escapeHtml(value ?? "")}</textarea>`;
}

function selectInput(value, path, options) {
  return `<select data-path="${path}">${options.map((item) => `<option value="${escapeHtml(item)}" ${item === value ? "selected" : ""}>${escapeHtml(item)}</option>`).join("")}</select>`;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
}

function setPath(object, path, value) {
  const parts = path.split(".");
  let current = object;
  parts.slice(0, -1).forEach((part) => { current = current[part]; });
  const key = parts[parts.length - 1];
  if (typeof current[key] === "number") current[key] = Number(value) || 0;
  else if (typeof current[key] === "boolean") current[key] = Boolean(value);
  else current[key] = value;
}

function collectInputs(root = document) {
  root.querySelectorAll("[data-path]").forEach((input) => {
    const value = input.type === "checkbox" ? input.checked : input.value;
    setPath(profile, input.dataset.path, value);
  });
}

function collectCriticalSystems() {
  const criticalSystems = document.querySelector("[data-critical-systems]");
  if (criticalSystems) {
    profile.downtime.critical_systems = criticalSystems.value.split("\n").map((item) => item.trim()).filter(Boolean);
  }
}

function collectIncidentRunnerEdits() {
  if (!profile?.incident_timeline) return;
  $$("[data-incident-systems]").forEach((field) => {
    const index = Number(field.dataset.incidentSystems);
    if (!Number.isFinite(index) || !profile.incident_timeline.timeline?.[index]) return;
    profile.incident_timeline.timeline[index].systems = field.value.split("\n").map((item) => item.trim()).filter(Boolean);
  });
}

function collectCurrentEdits() {
  collectInputs();
  collectCriticalSystems();
  collectIncidentRunnerEdits();
}

function nextNumberedId(prefix, rows) {
  const numbers = rows
    .map((row) => Number(String(row.id || "").replace(/\D/g, "")))
    .filter((number) => Number.isFinite(number));
  const next = Math.max(0, ...numbers) + 1;
  return `${prefix}-${String(next).padStart(3, "0")}`;
}

function newVendor() {
  const next = (profile.vendors || []).length + 1;
  return {
    id: `vendor-manual-${next}`,
    category: "manual",
    name: "New vendor",
    service: "Describe service",
    touches_ephi: true,
    baa_status: "unknown",
    soc2_status: "not provided",
    hitrust_status: "not provided",
    ai_training_use: "not reviewed",
    subcontractors_known: "unknown",
    incident_notification_terms: "unknown",
    risk: "medium",
  };
}

function newFlow() {
  return {
    id: nextNumberedId("FLOW", profile.flows || []),
    source: "New source",
    destination: "New destination",
    ephi_type: "Describe ePHI category",
    vendor: "Vendor to confirm",
    transmission: "portal, integration, email, fax, or manual process",
    baa_needed: true,
    risk: "medium",
    evidence_needed: "BAA, owner, access controls, workflow evidence",
    confirmed: false,
  };
}

function newAIWorkflow() {
  return {
    name: "New AI workflow",
    proposed_use: "Describe the proposed use",
    data_used: "No patient data unless approved",
    vendor: "Vendor to review",
    decision: "restricted",
    evidence_needed: "AI policy, BAA/data-use review if patient data is involved",
  };
}

function newEvidence() {
  return {
    id: nextNumberedId("EVID", profile.evidence || []),
    title: "New evidence reference",
    type: "signed_baa",
    area: "Evidence",
    owner: "Security Owner",
    reference: "",
    status: "needed",
    related: "",
    stores_sensitive_content: false,
    notes: "Reference location only; do not paste PHI.",
  };
}

function newIncidentEvent() {
  const index = (profile.incident_timeline?.timeline || []).length + 1;
  return {
    time: `T+${index * 15}`,
    phase: "Custom event",
    event: "Describe the sanitized event category.",
    systems: ["System or workflow category"],
    owner: profile.practice?.security_owner || "Practice owner",
    evidence_ref: `restricted-evidence/incidents/manual-event-${index}`,
    status: "requested",
    decision_gate: "What decision must be made, and who owns it?",
  };
}

function newIncidentAfterAction() {
  const index = (profile.incident_timeline?.after_actions || []).length + 1;
  return {
    id: `INC-AA-${String(index).padStart(3, "0")}`,
    priority: "medium",
    owner: profile.practice?.technical_owner || "MSP Lead",
    action: "Assign a concrete remediation or evidence-refresh action.",
    evidence_needed: "Reference-only evidence needed to close this action.",
    due: "30 days",
  };
}

function renderPresets() {
  const sizeSelect = $("#size-tier");
  sizeSelect.innerHTML = Object.entries(catalogs.practice_presets.size_tiers)
    .map(([key, item]) => `<option value="${key}">${escapeHtml(item.label)} - ${escapeHtml(item.setup_hint)}</option>`)
    .join("");
  const cards = $("#preset-cards");
  cards.innerHTML = Object.entries(catalogs.practice_presets.presets).map(([key, item]) => `
    <article class="preset-card ${key === selectedPreset ? "selected" : ""}" data-preset="${key}">
      <strong>${escapeHtml(item.name)}</strong>
      <span>${escapeHtml(item.description)}</span>
      <small>Estimated setup: ${escapeHtml(item.estimated_setup)}</small>
      <small>Likely systems: ${item.systems.length}</small>
    </article>
  `).join("");
  $$(".preset-card").forEach((card) => card.addEventListener("click", () => {
    selectedPreset = card.dataset.preset;
    renderPresets();
  }));
}

function scenarioByKey(key) {
  return incidentScenarios.find((scenario) => scenario.key === key);
}

function renderBasics() {
  const fields = [
    ["Practice name", "practice.name"],
    ["Practice type", "practice.type"],
    ["Staff count", "practice.staff_count", "number"],
    ["Locations", "practice.locations", "number"],
    ["Review period", "practice.review_period"],
    ["Security owner", "practice.security_owner"],
    ["Technical owner", "practice.technical_owner"],
  ];
  $("#basics-form").innerHTML = fields.map(([label, path, type]) => `<label>${label}${textInput(path.split(".").reduce((o, k) => o[k], profile), path, type || "text")}</label>`).join("");
}

function renderSystems() {
  const selected = new Set(profile.systems.map((system) => system.catalog_key));
  $("#systems-list").innerHTML = Object.entries(catalogs.system_catalog.systems).map(([key, item]) => `
    <label class="check-card">
      <input type="checkbox" data-system-key="${key}" ${selected.has(key) ? "checked" : ""}>
      <span><strong>${escapeHtml(item.name)}</strong><small>${escapeHtml(item.description)}</small><small><b>Evidence:</b> ${escapeHtml(item.evidence_needed)}</small></span>
    </label>
  `).join("");
}

function renderVendors() {
  $("#vendors-table").innerHTML = `<table><thead><tr><th>Vendor</th><th>Service</th><th>Touches ePHI</th><th>BAA</th><th>SOC 2</th><th>HITRUST</th><th>AI data use</th><th>Subcontractors</th><th>Incident terms</th><th>Risk</th><th>Remove</th></tr></thead><tbody>
    ${profile.vendors.map((vendor, index) => `<tr>
      <td>${textInput(vendor.name, `vendors.${index}.name`)}</td>
      <td>${textInput(vendor.service, `vendors.${index}.service`)}</td>
      <td><input type="checkbox" ${vendor.touches_ephi ? "checked" : ""} data-path="vendors.${index}.touches_ephi"></td>
      <td>${selectInput(vendor.baa_status, `vendors.${index}.baa_status`, ["signed", "unknown", "missing review date", "not applicable", "payer relationship"])}</td>
      <td>${selectInput(vendor.soc2_status || "not provided", `vendors.${index}.soc2_status`, ["not provided", "provided", "absent", "not applicable", "requested"])}</td>
      <td>${selectInput(vendor.hitrust_status || "not provided", `vendors.${index}.hitrust_status`, ["not provided", "provided", "absent", "not applicable", "requested"])}</td>
      <td>${selectInput(vendor.ai_training_use, `vendors.${index}.ai_training_use`, ["not reviewed", "unknown", "prohibited", "allowed by contract", "not applicable"])}</td>
      <td>${selectInput(vendor.subcontractors_known, `vendors.${index}.subcontractors_known`, ["known", "partial", "unknown", "not applicable"])}</td>
      <td>${textInput(vendor.incident_notification_terms, `vendors.${index}.incident_notification_terms`)}</td>
      <td>${selectInput(vendor.risk, `vendors.${index}.risk`, ["low", "medium", "high", "critical"])}</td>
      <td class="actions-cell"><button class="danger compact" type="button" data-remove="vendors:${index}">Remove</button></td>
    </tr>`).join("")}
  </tbody></table>`;
}

function renderFlows() {
  $("#flows-table").innerHTML = `<table><thead><tr><th>Flow</th><th>Source</th><th>Destination</th><th>Vendor</th><th>ePHI type</th><th>Transmission</th><th>BAA</th><th>Risk</th><th>Evidence</th><th>Remove</th></tr></thead><tbody>
    ${profile.flows.map((flow, index) => `<tr>
      <td>${textInput(flow.id, `flows.${index}.id`)}</td>
      <td>${textInput(flow.source, `flows.${index}.source`)}</td>
      <td>${textInput(flow.destination, `flows.${index}.destination`)}</td>
      <td>${textInput(flow.vendor, `flows.${index}.vendor`)}</td>
      <td>${textInput(flow.ephi_type, `flows.${index}.ephi_type`)}</td>
      <td>${textInput(flow.transmission, `flows.${index}.transmission`)}</td>
      <td><input type="checkbox" ${flow.baa_needed ? "checked" : ""} data-path="flows.${index}.baa_needed"></td>
      <td>${selectInput(flow.risk, `flows.${index}.risk`, ["low", "medium", "high", "critical"])}</td>
      <td>${textInput(flow.evidence_needed, `flows.${index}.evidence_needed`)}</td>
      <td class="actions-cell"><button class="danger compact" type="button" data-remove="flows:${index}">Remove</button></td>
    </tr>`).join("")}
  </tbody></table>`;
}

function renderReadiness() {
  const labels = {
    mfa_email: "Email MFA enabled",
    mfa_ehr: "EHR MFA enabled",
    unique_accounts: "Unique accounts",
    quarterly_access_review: "Quarterly access review recorded",
    tested_backups: "Backups restore-tested",
    vendor_inventory: "Vendor inventory started",
    baa_register: "BAA register reviewed",
    incident_contact_list: "Incident contact list ready",
    downtime_plan: "Downtime plan documented",
    security_training_current: "Training current",
    log_review_cadence: "Log review cadence set",
  };
  $("#readiness-list").innerHTML = Object.entries(labels).map(([key, label]) => `
    <label class="task-row"><input type="checkbox" ${profile.readiness[key] ? "checked" : ""} data-path="readiness.${key}"><span><strong>${label}</strong><small>Use an evidence reference instead of storing sensitive screenshots here.</small></span></label>
  `).join("");
}

function renderAI() {
  $("#ai-table").innerHTML = `<table><thead><tr><th>Workflow</th><th>Use</th><th>Data</th><th>Vendor</th><th>Decision</th><th>Evidence</th><th>Remove</th></tr></thead><tbody>
    ${profile.ai_workflows.map((workflow, index) => `<tr>
      <td>${textInput(workflow.name, `ai_workflows.${index}.name`)}</td>
      <td>${textInput(workflow.proposed_use, `ai_workflows.${index}.proposed_use`)}</td>
      <td>${textInput(workflow.data_used, `ai_workflows.${index}.data_used`)}</td>
      <td>${textInput(workflow.vendor, `ai_workflows.${index}.vendor`)}</td>
      <td>${selectInput(workflow.decision, `ai_workflows.${index}.decision`, ["allowed", "restricted", "prohibited"])}</td>
      <td>${textInput(workflow.evidence_needed, `ai_workflows.${index}.evidence_needed`)}</td>
      <td class="actions-cell"><button class="danger compact" type="button" data-remove="ai_workflows:${index}">Remove</button></td>
    </tr>`).join("")}
  </tbody></table>`;
}

function renderIncidentRunner() {
  if (!profile.incident_timeline) return;
  const incident = profile.incident_timeline;
  const selectedKey = incident.scenario_key || incidentScenarios[0]?.key || "suspicious_login";
  $("#incident-scenario").innerHTML = incidentScenarios.map((scenario) => (
    `<option value="${escapeHtml(scenario.key)}" ${scenario.key === selectedKey ? "selected" : ""}>${escapeHtml(scenario.label)}</option>`
  )).join("");
  const scenario = scenarioByKey(selectedKey);
  $("#incident-summary").innerHTML = `
    <article class="summary-card runner-scenario">
      <strong>${escapeHtml(incident.scenario_name || scenario?.label || "Incident tabletop")}</strong>
      <small>${escapeHtml(incident.summary || scenario?.summary || "Sanitized incident timeline for owner/MSP handoff.")}</small>
      <small><b>Boundary:</b> ${escapeHtml(incident.sensitive_data_boundary || "Use categories and evidence references only.")}</small>
    </article>
  `;
  const timeline = incident.timeline || [];
  $("#incident-timeline").innerHTML = timeline.map((entry, index) => `
    <article class="runner-card">
      <div class="runner-card-head">
        <span class="step-pill">${escapeHtml(entry.phase || `Event ${index + 1}`)}</span>
        <button class="danger compact" type="button" data-incident-remove="timeline:${index}">Remove</button>
      </div>
      <div class="form-grid runner-grid">
        <label>Time${textInput(entry.time, `incident_timeline.timeline.${index}.time`)}</label>
        <label>Phase${textInput(entry.phase, `incident_timeline.timeline.${index}.phase`)}</label>
        <label>Owner${textInput(entry.owner, `incident_timeline.timeline.${index}.owner`)}</label>
        <label>Status${selectInput(entry.status, `incident_timeline.timeline.${index}.status`, ["requested", "open", "needs review", "in progress", "closed"])}</label>
        <label>System or workflow category<textarea data-incident-systems="${index}">${escapeHtml((entry.systems || []).join("\n"))}</textarea></label>
        <label>Private evidence reference${textInput(entry.evidence_ref, `incident_timeline.timeline.${index}.evidence_ref`)}</label>
        <label class="wide">Sanitized event category${textareaInput(entry.event, `incident_timeline.timeline.${index}.event`)}</label>
        <label class="wide">Decision gate${textareaInput(entry.decision_gate, `incident_timeline.timeline.${index}.decision_gate`)}</label>
      </div>
    </article>
  `).join("");

  const actions = incident.after_actions || [];
  $("#incident-after-actions").innerHTML = actions.map((item, index) => `
    <article class="runner-card">
      <div class="runner-card-head">
        <span class="step-pill">${escapeHtml(item.id || `INC-AA-${index + 1}`)}</span>
        <button class="danger compact" type="button" data-incident-remove="after_actions:${index}">Remove</button>
      </div>
      <div class="form-grid runner-grid">
        <label>ID${textInput(item.id, `incident_timeline.after_actions.${index}.id`)}</label>
        <label>Priority${selectInput(item.priority, `incident_timeline.after_actions.${index}.priority`, ["low", "medium", "high", "critical"])}</label>
        <label>Owner${textInput(item.owner, `incident_timeline.after_actions.${index}.owner`)}</label>
        <label>Due${textInput(item.due, `incident_timeline.after_actions.${index}.due`)}</label>
        <label class="wide">Action${textareaInput(item.action, `incident_timeline.after_actions.${index}.action`)}</label>
        <label class="wide">Evidence needed${textareaInput(item.evidence_needed, `incident_timeline.after_actions.${index}.evidence_needed`)}</label>
      </div>
    </article>
  `).join("");
}

function renderDowntime() {
  $("#downtime-form").innerHTML = `
    <label>Downtime plan status${selectInput(profile.downtime.downtime_plan_status, "downtime.downtime_plan_status", ["not documented", "draft", "documented", "tested"])}</label>
    <label>Last restore test${textInput(profile.downtime.last_restore_test, "downtime.last_restore_test")}</label>
    <label>Tabletop status${selectInput(profile.downtime.tabletop_status, "downtime.tabletop_status", ["not run", "scheduled", "run", "lessons recorded"])}</label>
    <label>Critical systems<textarea data-critical-systems>${escapeHtml(profile.downtime.critical_systems.join("\n"))}</textarea></label>
  `;
}

function renderEvidence() {
  const evidence = profile.evidence || [];
  $("#evidence-table").innerHTML = `<table><thead><tr><th>Evidence</th><th>Type</th><th>Area</th><th>Owner</th><th>Reference</th><th>Status</th><th>Notes</th><th>Remove</th></tr></thead><tbody>
    ${evidence.map((item, index) => `<tr>
      <td>${textInput(item.title, `evidence.${index}.title`)}</td>
      <td>${selectInput(item.type, `evidence.${index}.type`, Object.keys(catalogs.evidence_catalog.evidence_types))}</td>
      <td>${textInput(item.area, `evidence.${index}.area`)}</td>
      <td>${textInput(item.owner, `evidence.${index}.owner`)}</td>
      <td>${textInput(item.reference, `evidence.${index}.reference`)}</td>
      <td>${selectInput(item.status, `evidence.${index}.status`, ["needed", "requested", "collected", "reviewed", "expired"])}</td>
      <td>${textInput(item.notes, `evidence.${index}.notes`)}</td>
      <td class="actions-cell"><button class="danger compact" type="button" data-remove="evidence:${index}">Remove</button></td>
    </tr>`).join("")}
  </tbody></table>`;
}

function renderSummary() {
  const ready = Object.values(profile.readiness).filter(Boolean).length;
  const connectorItems = connectorState?.summary?.total_items || 0;
  const incidentEvents = profile.incident_timeline?.timeline?.length || 0;
  $("#completion-summary").innerHTML = `
    <article class="summary-card"><strong>${profile.systems.length}</strong><small>systems selected</small></article>
    <article class="summary-card"><strong>${profile.vendors.length}</strong><small>vendors to review</small></article>
    <article class="summary-card"><strong>${profile.flows.length}</strong><small>ePHI flows mapped</small></article>
    <article class="summary-card"><strong>${incidentEvents}</strong><small>incident runner events</small></article>
    <article class="summary-card"><strong>${ready}/11</strong><small>readiness items ready</small></article>
    <article class="summary-card"><strong>${connectorItems}</strong><small>connector evidence items</small></article>
  `;
}

function formatCountMap(map) {
  const entries = Object.entries(map || {});
  if (!entries.length) return "None yet";
  return entries.map(([key, count]) => `${key.replaceAll("_", " ")}: ${count}`).join(" | ");
}

function statusClass(status) {
  const value = String(status || "unknown");
  if (value.includes("warning") || value === "needs_review" || value === "requested") return "status-warn";
  if (value === "missing" || value === "stale") return "status-danger";
  return "status-ok";
}

function renderConnectors() {
  if (!$("#connector-summary")) return;
  const summary = connectorState?.summary || {};
  const items = connectorState?.items || [];
  const total = Number(summary.total_items || 0);
  const needsAttention = Number(summary.needs_attention || 0);
  const runCount = Number((summary.runs || []).length || items.length || 0);
  const boundary = summary.data_boundary || "metadata_only_no_phi_expected";
  $("#connector-summary").innerHTML = `
    <div class="summary-grid connector-stat-grid">
      <article class="summary-card"><strong>${total}</strong><small>evidence items</small></article>
      <article class="summary-card"><strong>${runCount}</strong><small>connector runs</small></article>
      <article class="summary-card"><strong>${needsAttention}</strong><small>needs follow-up</small></article>
      <article class="summary-card"><strong>${connectorState?.build_uses_connectors ? "Yes" : "No"}</strong><small>included in next build</small></article>
    </div>
    <div class="connector-detail-strip">
      <span><b>Boundary:</b> ${escapeHtml(boundary.replaceAll("_", " "))}</span>
      <span><b>Owner lanes:</b> ${escapeHtml(formatCountMap(summary.by_owner_lane))}</span>
      <span><b>Status:</b> ${escapeHtml(formatCountMap(summary.by_status))}</span>
    </div>
  `;

  if (!items.length) {
    $("#connector-evidence-table").innerHTML = `<div class="empty-state">No connector evidence collected yet.</div>`;
    return;
  }
  $("#connector-evidence-table").innerHTML = `<table><thead><tr><th>Connector</th><th>Mode</th><th>Status</th><th>Evidence</th><th>PHI expected</th><th>Warnings</th><th>File</th></tr></thead><tbody>
    ${items.map((item) => {
      const warnings = (item.warnings || []).join("; ") || "None";
      return `<tr>
        <td>${escapeHtml(item.connector)}</td>
        <td>${escapeHtml(item.mode || "metadata")}</td>
        <td><span class="status-pill ${statusClass(item.status)}">${escapeHtml(item.status || "unknown")}</span></td>
        <td>${escapeHtml(item.evidence_count)}</td>
        <td>${item.phi_expected ? "Yes" : "No"}</td>
        <td>${escapeHtml(warnings)}</td>
        <td><span class="mono">${escapeHtml(item.file)}</span></td>
      </tr>`;
    }).join("")}
  </tbody></table>`;
}

function renderAll() {
  renderBasics();
  renderSystems();
  renderVendors();
  renderFlows();
  renderReadiness();
  renderAI();
  renderIncidentRunner();
  renderDowntime();
  renderEvidence();
  renderSummary();
  renderConnectors();
}

const INCIDENT_UNSAFE_PATTERNS = [
  /patient name\s*:/i,
  /\bMRN\s*:/i,
  /\bDOB\s*:/i,
  /\bdiagnosis\s*:/i,
  /\bpassword\s*[:=]/i,
  /\b(token|secret|api[_ -]?key)\s*[:=]/i,
  /https?:\/\/\S+(token=|secret=|signature=|X-Amz-Signature|sig=|key=|password=|private)/i,
  /-----BEGIN [A-Z ]*PRIVATE KEY-----/,
];

function walkStrings(value, path = "incident_timeline") {
  if (Array.isArray(value)) {
    return value.flatMap((item, index) => walkStrings(item, `${path}[${index}]`));
  }
  if (value && typeof value === "object") {
    return Object.entries(value).flatMap(([key, child]) => walkStrings(child, `${path}.${key}`));
  }
  if (typeof value === "string") return [{ path, value }];
  return [];
}

function unsafeIncidentFields(incident) {
  const findings = [];
  for (const item of walkStrings(incident)) {
    if (INCIDENT_UNSAFE_PATTERNS.some((pattern) => pattern.test(item.value))) findings.push(item.path);
  }
  return findings;
}

async function saveProfile() {
  collectCurrentEdits();
  const data = await api("/api/profile", { method: "POST", body: JSON.stringify({ profile }) });
  profile = data.profile;
  renderAll();
  showAlert("Saved locally. No data left this machine.", false);
}

async function loadConnectors() {
  const data = await api("/api/connectors");
  connectorState = data.connectors;
  renderConnectors();
  renderSummary();
  return connectorState;
}

async function loadIncidentRunner() {
  const data = await api("/api/incident-runner");
  incidentScenarios = data.scenarios || [];
  profile.incident_timeline = profile.incident_timeline || data.incident_timeline;
  return data.incident_timeline;
}

async function saveIncidentRunner() {
  collectCurrentEdits();
  const unsafe = unsafeIncidentFields(profile.incident_timeline);
  if (unsafe.length) {
    showAlert(`Incident runner blocked unsafe detail. Replace with categories and private evidence refs: ${unsafe.slice(0, 4).join(", ")}`);
    return;
  }
  const data = await api("/api/incident-runner", {
    method: "POST",
    body: JSON.stringify({ incident_timeline: profile.incident_timeline, build: true }),
  });
  profile = data.profile;
  renderAll();
  showAlert("Saved the incident runner and rebuilt the local packet.", false);
}

async function connectorAction(path, payload, successMessage, button) {
  const originalText = button?.textContent;
  if (button) {
    button.disabled = true;
    button.textContent = "Working...";
  }
  try {
    const data = await api(path, { method: "POST", body: JSON.stringify(payload || {}) });
    if (data.connectors) {
      connectorState = data.connectors;
      renderConnectors();
      renderSummary();
    } else {
      await loadConnectors();
    }
    showAlert(successMessage, false);
    return data;
  } finally {
    if (button) {
      button.disabled = false;
      button.textContent = originalText;
    }
  }
}

async function init() {
  $$(".rail button").forEach((button) => button.addEventListener("click", () => navTo(button.dataset.section)));
  const status = await api("/api/status");
  csrfToken = status.csrf_token;
  $("#network-status").textContent = status.network_status;
  catalogs = (await api("/api/catalogs")).catalogs;
  profile = (await api("/api/profile")).profile;
  connectorState = (await api("/api/connectors")).connectors;
  await loadIncidentRunner();
  renderPresets();
  renderAll();

  $("#create-workspace").addEventListener("click", async () => {
    try {
      const data = await api("/api/workspaces", {
        method: "POST",
        body: JSON.stringify({
          practice_name: $("#practice-name").value || "My Practice",
          preset: selectedPreset,
          size_tier: $("#size-tier").value,
        }),
      });
      profile = data.profile;
      await loadConnectors();
      renderAll();
      navTo("systems");
      showAlert("Created a local profile from the selected healthcare preset.", false);
    } catch (error) {
      showAlert(error.message);
    }
  });

  $("#apply-systems").addEventListener("click", async () => {
    try {
      const selected = new Set($$("[data-system-key]").filter((input) => input.checked).map((input) => input.dataset.systemKey));
      profile.systems = Object.entries(catalogs.system_catalog.systems)
        .filter(([key]) => selected.has(key))
        .map(([key, item]) => ({
          id: `system-${key}`,
          catalog_key: key,
          name: item.name,
          category: item.category,
          ephi_role: item.ephi_role,
          owner: item.owner,
          vendor: `Example ${catalogs.vendor_catalog.vendors[item.vendor_category].label}`,
          vendor_category: item.vendor_category,
          access_method: item.access_method,
          evidence_needed: item.evidence_needed,
          selected: true,
        }));
      const data = await api("/api/suggestions/rebuild", { method: "POST", body: JSON.stringify({ profile }) });
      profile = data.profile;
      renderAll();
      navTo("connectors");
      showAlert("Systems applied. Connector evidence can now replace the slowest manual checks.", false);
    } catch (error) {
      showAlert(error.message);
    }
  });

  $$(".save-profile").forEach((button) => button.addEventListener("click", async () => {
    try { await saveProfile(); } catch (error) { showAlert(error.message); }
  }));

  $("#generate-packet").addEventListener("click", async () => {
    try {
      await saveProfile();
      const data = await api("/api/build", { method: "POST", body: JSON.stringify({}) });
      $("#dashboard-link").href = data.links.dashboard;
      $("#packet-link").href = data.links.packet;
      $("#command-center-link").href = data.links.command_center || "/sprint-command-center.html";
      $("#connector-summary-link").href = data.links.connector_summary || "/connector-evidence-summary.json";
      $("#packet-refresh-link").href = data.links.evidence_refresh || "/evidence-refresh.json";
      $("#owner-view-link").href = data.links.views || "/views/owner-view.md";
      await loadConnectors();
      showAlert("Built the local packet and included connector evidence where available.", false);
    } catch (error) {
      showAlert(error.message);
    }
  });

  $("#load-incident-template").addEventListener("click", async (event) => {
    const button = event.currentTarget;
    const originalText = button.textContent;
    try {
      collectCurrentEdits();
      button.disabled = true;
      button.textContent = "Loading...";
      const scenario_key = $("#incident-scenario").value || "suspicious_login";
      const data = await api("/api/incident-runner/template", { method: "POST", body: JSON.stringify({ scenario_key }) });
      profile.incident_timeline = data.incident_timeline;
      renderIncidentRunner();
      renderSummary();
      showAlert("Loaded the scenario template locally. Review and save when ready.", false);
    } catch (error) {
      showAlert(error.message);
    } finally {
      button.disabled = false;
      button.textContent = originalText;
    }
  });

  $("#save-incident-runner").addEventListener("click", async () => {
    try { await saveIncidentRunner(); } catch (error) { showAlert(error.message); }
  });

  $("#write-connector-wizard").addEventListener("click", async (event) => {
    try {
      const data = await connectorAction("/api/connectors/wizard", {}, "Created the local MSP connector checklist.", event.currentTarget);
      $("#connector-wizard-link").href = data.href || "/connector-wizard.html";
    } catch (error) {
      showAlert(error.message);
    }
  });

  $("#collect-dns").addEventListener("click", async (event) => {
    try {
      const domain = $("#dns-domain").value.trim();
      if (!domain) {
        showAlert("Enter the practice domain first.");
        return;
      }
      await connectorAction("/api/connectors/dns", { domain }, "Collected public DNS and email-authentication evidence.", event.currentTarget);
    } catch (error) {
      showAlert(error.message);
    }
  });

  $("#collect-vendor-public").addEventListener("click", async (event) => {
    try {
      const vendor = $("#vendor-name").value.trim();
      const domain = $("#vendor-domain").value.trim();
      if (!vendor || !domain) {
        showAlert("Enter the vendor name and public domain first.");
        return;
      }
      await connectorAction("/api/connectors/vendor-public", { vendor, domain }, "Collected public vendor evidence references.", event.currentTarget);
    } catch (error) {
      showAlert(error.message);
    }
  });

  $("#import-msp-response").addEventListener("click", async (event) => {
    try {
      const path = $("#msp-response-path").value.trim();
      if (!path) {
        showAlert("Enter the local MSP response YAML path first.");
        return;
      }
      await connectorAction("/api/connectors/msp-response", { path }, "Imported the MSP response as metadata-only evidence.", event.currentTarget);
    } catch (error) {
      showAlert(error.message);
    }
  });

  $("#connect-google-workspace").addEventListener("click", async (event) => {
    try {
      const client_id = $("#google-client-id").value.trim();
      if (!client_id) {
        showAlert("Enter the Google OAuth client ID first.");
        return;
      }
      await connectorAction(
        "/api/connectors/google-workspace/connect",
        { client_id },
        "Google Workspace OAuth tokens were stored in the local secret store.",
        event.currentTarget,
      );
    } catch (error) {
      showAlert(error.message);
    }
  });

  $("#collect-google-workspace").addEventListener("click", async (event) => {
    try {
      const domain = $("#google-domain").value.trim();
      await connectorAction("/api/connectors/google-workspace/collect", { domain }, "Collected Google Workspace metadata evidence.", event.currentTarget);
    } catch (error) {
      showAlert(error.message);
    }
  });

  $("#connect-microsoft-365").addEventListener("click", async (event) => {
    try {
      const client_id = $("#microsoft-client-id").value.trim();
      const tenant = $("#microsoft-tenant").value.trim() || "organizations";
      if (!client_id) {
        showAlert("Enter the Microsoft application client ID first.");
        return;
      }
      await connectorAction(
        "/api/connectors/microsoft-365/connect",
        { client_id, tenant },
        "Microsoft 365 OAuth tokens were stored in the local secret store.",
        event.currentTarget,
      );
    } catch (error) {
      showAlert(error.message);
    }
  });

  $("#collect-microsoft-365").addEventListener("click", async (event) => {
    try {
      await connectorAction("/api/connectors/microsoft-365/collect", {}, "Collected Microsoft 365 metadata evidence.", event.currentTarget);
    } catch (error) {
      showAlert(error.message);
    }
  });

  $("#refresh-connectors").addEventListener("click", async (event) => {
    try {
      const data = await connectorAction("/api/connectors/refresh", {}, "Wrote the evidence freshness report.", event.currentTarget);
      $("#evidence-refresh-link").href = data.href || "/evidence-refresh.json";
      $("#packet-refresh-link").href = data.href || "/evidence-refresh.json";
    } catch (error) {
      showAlert(error.message);
    }
  });

  $("#generate-views").addEventListener("click", async (event) => {
    try {
      const data = await connectorAction("/api/connectors/views", {}, "Generated owner, MSP, vendor, and legal/compliance views.", event.currentTarget);
      $("#owner-view-link").href = (data.hrefs || ["/views/owner-view.md"])[0];
    } catch (error) {
      showAlert(error.message);
    }
  });

  document.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;
    const remove = target.closest("[data-remove]");
    const incidentRemove = target.closest("[data-incident-remove]");
    if (incidentRemove) {
      collectCurrentEdits();
      const [collection, index] = incidentRemove.dataset.incidentRemove.split(":");
      if (Array.isArray(profile.incident_timeline?.[collection])) {
        profile.incident_timeline[collection].splice(Number(index), 1);
        renderIncidentRunner();
        renderSummary();
        showAlert("Removed incident runner row locally. Save when ready.", false);
      }
      return;
    }
    if (!remove) return;
    collectCurrentEdits();
    const [collection, index] = remove.dataset.remove.split(":");
    if (!Array.isArray(profile[collection])) return;
    profile[collection].splice(Number(index), 1);
    renderAll();
    showAlert("Removed row locally. Save when ready.", false);
  });

  $("#add-vendor").addEventListener("click", () => {
    collectCurrentEdits();
    profile.vendors.push(newVendor());
    renderVendors();
    showAlert("Added a vendor row. Save when ready.", false);
  });

  $("#add-flow").addEventListener("click", () => {
    collectCurrentEdits();
    profile.flows.push(newFlow());
    renderFlows();
    renderSummary();
    showAlert("Added an ePHI flow row. Save when ready.", false);
  });

  $("#add-ai-workflow").addEventListener("click", () => {
    collectCurrentEdits();
    profile.ai_workflows.push(newAIWorkflow());
    renderAI();
    showAlert("Added an AI workflow row. Save when ready.", false);
  });

  $("#add-incident-event").addEventListener("click", () => {
    collectCurrentEdits();
    profile.incident_timeline = profile.incident_timeline || { timeline: [], after_actions: [] };
    profile.incident_timeline.timeline = profile.incident_timeline.timeline || [];
    profile.incident_timeline.timeline.push(newIncidentEvent());
    renderIncidentRunner();
    renderSummary();
    showAlert("Added a timeline event. Save the runner when ready.", false);
  });

  $("#add-incident-after-action").addEventListener("click", () => {
    collectCurrentEdits();
    profile.incident_timeline = profile.incident_timeline || { timeline: [], after_actions: [] };
    profile.incident_timeline.after_actions = profile.incident_timeline.after_actions || [];
    profile.incident_timeline.after_actions.push(newIncidentAfterAction());
    renderIncidentRunner();
    renderSummary();
    showAlert("Added an after-action item. Save the runner when ready.", false);
  });

  $("#add-evidence").addEventListener("click", () => {
    collectCurrentEdits();
    profile.evidence = profile.evidence || [];
    profile.evidence.push(newEvidence());
    renderEvidence();
    showAlert("Added an evidence reference row. Save when ready.", false);
  });

  $("#inventory-folder").addEventListener("click", async () => {
    try {
      const folderPath = $("#inventory-path").value.trim();
      if (!folderPath) {
        showAlert("Enter a local folder path first.");
        return;
      }
      const data = await api("/api/evidence/inventory-folder", { method: "POST", body: JSON.stringify({ path: folderPath }) });
      const imported = data.inventory.evidence || [];
      profile.evidence = [...(profile.evidence || []), ...imported];
      renderEvidence();
      showAlert(`Imported ${imported.length} metadata-only evidence references. ${data.inventory.skipped.length} files skipped.`, false);
    } catch (error) {
      showAlert(error.message);
    }
  });
}

init().catch((error) => showAlert(error.message));
