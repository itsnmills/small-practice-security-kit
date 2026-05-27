let csrfToken = "";
let catalogs = null;
let profile = null;
let connectorState = null;
let incidentScenarios = [];
let activeIncidentIndex = 0;
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

function requestedSection() {
  const params = new URLSearchParams(window.location.search);
  const section = params.get("section") || window.location.hash.replace("#", "");
  return $(`.rail button[data-section="${section}"]`) ? section : null;
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
    complete: false,
    owner_lane: "Owner/MSP",
    source_alignment: ["Practice incident-response procedure"],
    plain_english_goal: "Answer one sanitized decision question and create a private evidence reference.",
    owner_prompt: "What decision is needed now, and who owns the next step?",
    staff_script: "Report the workflow category and time observed only. Do not paste patient details, screenshots, logs, URLs, or credentials.",
    do_now: ["Record category, owner, time, affected workflow, and private evidence reference."],
    ask_msp_or_vendor: ["What should be checked first, and what evidence reference should the practice record?"],
    allowed_inputs: ["category", "owner", "time observed", "affected workflow", "private evidence reference"],
    blocked_inputs: ["PHI", "patient identifiers", "screenshots", "raw logs", "credentials", "private URLs"],
    evidence_required: ["private evidence reference", "owner", "date observed"],
    completion_criteria: ["owner assigned", "evidence reference recorded", "next action chosen"],
    escalation_triggers: ["active compromise", "patient-care disruption", "ransomware concern", "qualified review needed"],
    primary_question: "What decision must be made, and who owns it?",
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

function asList(value) {
  if (Array.isArray(value)) return value.filter(Boolean);
  if (!value) return [];
  return [String(value)];
}

function guidanceList(title, items) {
  const list = asList(items);
  if (!list.length) return "";
  return `
    <section class="guidance-block">
      <strong>${escapeHtml(title)}</strong>
      <ul>${list.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
    </section>
  `;
}

function phaseStatusLabel(entry) {
  if (entry.complete) return "Complete";
  if (entry.status === "closed") return "Closed";
  return entry.status || "requested";
}

const READINESS_LABELS = {
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

const READINESS_PRIORITY = [
  "mfa_email",
  "mfa_ehr",
  "tested_backups",
  "quarterly_access_review",
  "incident_contact_list",
  "downtime_plan",
  "baa_register",
  "log_review_cadence",
];

const SECTION_PLAYBOOKS = {
  start: {
    lane: "Scope first",
    question: "Which practice shape are we building for?",
    goal: "Start from the closest operating model so every later question is tied to real systems, owners, vendors, evidence, and downtime needs.",
    doNow: [
      "Pick the closest preset and size tier; precision comes after the workspace exists.",
      "Use the practice name or a working nickname only.",
      "Create the workspace, then verify systems before editing vendor or flow rows.",
    ],
    ask: [
      "Who owns security decisions for this practice?",
      "Who can produce technical evidence: MSP, EHR admin, office manager, billing lead, or vendor support?",
      "Which locations and service lines are in scope for this first packet?",
    ],
    evidence: [
      "Practice profile owner and review period.",
      "Current system list from staff or MSP.",
      "Named contact for MSP/vendor evidence requests.",
    ],
    doNot: [
      "Do not enter patient examples or incident specifics.",
      "Do not turn the preset into a compliance conclusion.",
    ],
    sourceAlignment: [
      "NIST CSF Govern: define scope, roles, and risk responsibility before control work.",
      "HHS small-practice risk assessment guidance: gather context that supports a risk review, not a certification claim.",
    ],
  },
  basics: {
    lane: "Accountability",
    question: "Who can decide, who can prove, and who can fix?",
    goal: "Make the packet usable in a real practice meeting by naming the owner, technical lead, review period, staff size, and locations.",
    doNow: [
      "Fill in the security owner and technical owner.",
      "Confirm staff count, locations, and review period.",
      "Keep names at the role/contact level; do not add patients, staff secrets, or clinical examples.",
    ],
    ask: [
      "Who can approve MFA, access-review, backup, and downtime changes?",
      "Who has admin access to email, EHR, billing, phones, network, and backups?",
      "Who signs vendor BAAs or routes contract questions?",
    ],
    evidence: [
      "Named owner for the review period.",
      "MSP or technical contact reference.",
      "Practice scope note covering staff count and locations.",
    ],
    doNot: [
      "Do not store credentials, MFA backup codes, or private admin URLs.",
      "Do not use this page for HR notes or patient-specific context.",
    ],
    sourceAlignment: [
      "HIPAA Security Rule administrative safeguards: assign responsibility and manage risk.",
      "NIST CSF Govern: cybersecurity risk decisions need visible accountable roles.",
    ],
  },
  systems: {
    lane: "Asset reality",
    question: "Which technology could affect care, billing, access, or ePHI?",
    goal: "Build an owner-grade asset picture from the systems staff actually rely on, then let that drive evidence and vendor questions.",
    doNow: [
      "Select every system category the practice uses today.",
      "Include boring but critical systems: phones, shared drives, email, backups, identity, billing, and network devices.",
      "Apply systems before reviewing vendors, flows, or evidence.",
    ],
    ask: [
      "Which systems are impossible to work without for one business day?",
      "Which systems have named admins and MFA?",
      "Which systems are owned by the MSP versus the practice versus a vendor?",
    ],
    evidence: [
      "System inventory or MSP asset export reference.",
      "Admin/user access export reference for major systems.",
      "Backup coverage or service agreement reference for critical systems.",
    ],
    doNot: [
      "Do not enter device serials if they expose private infrastructure.",
      "Do not paste raw logs, screenshots, or private URLs.",
    ],
    sourceAlignment: [
      "NIST CSF Identify: maintain asset inventory and business-environment context.",
      "HHS Security Rule: safeguards depend on understanding where ePHI is created, received, used, or maintained.",
    ],
  },
  connectors: {
    lane: "Proof without exposure",
    question: "Which evidence can be collected from safe metadata instead of screenshots?",
    goal: "Replace manual proof chasing with local, metadata-only evidence runs that keep the packet useful without storing sensitive material.",
    doNow: [
      "Start with DNS/email-authentication and MSP response import.",
      "Use Google Workspace or Microsoft 365 only for admin metadata needed for MFA/account posture.",
      "Refresh evidence before generating the packet.",
    ],
    ask: [
      "Can the MSP return structured answers with owners, dates, status, and ticket references?",
      "Which connector output should be reviewed by the owner before it enters the packet?",
      "Which evidence is too sensitive and should be referenced only by private ticket or folder ID?",
    ],
    evidence: [
      "Connector run summary and collection date.",
      "MFA/admin/access posture counts, not user-level secrets.",
      "DNS/email-authentication references and follow-up status.",
    ],
    doNot: [
      "Do not collect mailbox contents, drive contents, patient files, raw contracts, raw logs, or credentials.",
      "Do not treat connector output as proof that all users or systems are safe.",
    ],
    sourceAlignment: [
      "NIST CSF Detect and Identify: use observable evidence while preserving boundaries.",
      "HIPAA Security Rule technical safeguards: access posture evidence should support risk management without exposing ePHI.",
    ],
  },
  vendors: {
    lane: "Vendor pressure",
    question: "Which outside companies touch ePHI, downtime, identity, or recovery?",
    goal: "Turn vendor review into specific owner/MSP/vendor asks: BAA status, security evidence, AI data use, subcontractors, and incident terms.",
    doNow: [
      "Mark which vendors touch ePHI or critical operations.",
      "Set BAA and security evidence status honestly: signed, unknown, requested, or not applicable.",
      "Push high-risk or unknown vendors into the next action queue.",
    ],
    ask: [
      "Is there a signed BAA or documented reason one is not needed?",
      "Does the vendor use customer data for AI training, model improvement, analytics, or subcontractor processing?",
      "What are the incident notification terms and support escalation path?",
    ],
    evidence: [
      "BAA reference or contract owner.",
      "Vendor trust/security page or SOC 2/HITRUST reference when available.",
      "AI/data-use terms and subcontractor reference.",
    ],
    doNot: [
      "Do not paste full contracts or patient examples.",
      "Do not mark a vendor low-risk because it is familiar or widely used.",
    ],
    sourceAlignment: [
      "HIPAA Security Rule organizational requirements: business associate relationships need documented safeguards.",
      "NIST CSF Govern supply-chain emphasis: supplier risk must be visible to owners.",
    ],
  },
  flows: {
    lane: "Data movement",
    question: "Where can ePHI move, and who controls the path?",
    goal: "Make invisible data movement concrete enough for a practice owner to decide what needs a BAA, control, vendor answer, or downtime workaround.",
    doNow: [
      "Confirm each source, destination, vendor, transmission method, and evidence need.",
      "Flag flows with unknown vendor ownership or missing BAA status.",
      "Remove flows that do not exist so the packet stays credible.",
    ],
    ask: [
      "Which system initiates the flow and which vendor receives it?",
      "Is the flow portal-based, integration-based, email/fax-based, or manual?",
      "What breaks if this flow is unavailable for a day?",
    ],
    evidence: [
      "Workflow owner and transmission method.",
      "BAA or vendor agreement reference when ePHI is involved.",
      "Access control, integration, or policy reference for the flow.",
    ],
    doNot: [
      "Do not paste patient examples, claim narratives, clinical notes, or raw messages.",
      "Do not assume email, fax, or portal workflows are safe without owner review.",
    ],
    sourceAlignment: [
      "HHS risk analysis guidance: identify where ePHI is created, received, maintained, or transmitted.",
      "NIST CSF Identify: map assets, data, vendors, and business processes together.",
    ],
  },
  readiness: {
    lane: "Controls that matter",
    question: "Which missing basics would hurt the practice this week?",
    goal: "Keep the checklist short, concrete, and evidence-backed so the owner can fund or assign real fixes.",
    doNow: [
      "Answer each item based on evidence, not memory.",
      "Prioritize MFA, unique accounts, backup restore proof, access review, downtime, and incident contacts.",
      "Leave items unchecked when the evidence is missing.",
    ],
    ask: [
      "When was the last access review completed and by whom?",
      "When was a restore test completed for critical systems?",
      "Who reviews logs or alerts, and what happens when something looks wrong?",
    ],
    evidence: [
      "MFA/account posture summary.",
      "Access review date and owner.",
      "Backup restore test reference and downtime plan reference.",
    ],
    doNot: [
      "Do not check a box because the MSP says it is probably handled.",
      "Do not store screenshots or exports with sensitive account details here.",
    ],
    sourceAlignment: [
      "HHS 405(d) HICP: focus on practical, high-impact practices for healthcare organizations.",
      "NIST CSF Protect, Detect, Respond, and Recover: controls must reduce real operational risk.",
    ],
  },
  ai: {
    lane: "AI boundary",
    question: "Where could staff accidentally put patient-level data into an AI tool?",
    goal: "Separate low-risk internal productivity ideas from workflows that need BAA, data-use, policy, and qualified review.",
    doNow: [
      "List every AI workflow staff want to use or already use.",
      "Default to restricted unless the data boundary and vendor terms are understood.",
      "Mark public AI use with patient-level data as prohibited unless separately reviewed and approved outside this kit.",
    ],
    ask: [
      "What data goes into the tool and what output is used for decisions?",
      "Does the vendor offer a BAA and contract terms that prohibit training on customer data?",
      "Who reviews AI outputs before they affect patients, billing, or staff action?",
    ],
    evidence: [
      "AI policy or staff guidance reference.",
      "Vendor data-use and retention terms.",
      "BAA or qualified review reference for patient-data workflows.",
    ],
    doNot: [
      "Do not paste prompts, notes, claims, messages, or examples that contain patient-level data.",
      "Do not call an AI workflow approved because a vendor has a marketing security page.",
    ],
    sourceAlignment: [
      "HIPAA Security Rule safeguards apply when ePHI is created, received, maintained, or transmitted.",
      "NIST CSF Govern: technology risk decisions need policy, oversight, and accountability.",
    ],
  },
  downtime: {
    lane: "Care continuity",
    question: "Can the practice keep operating if a core tool fails?",
    goal: "Turn downtime from a binder exercise into a list of critical systems, owners, restore evidence, and staff-ready fallbacks.",
    doNow: [
      "Name critical systems in plain language.",
      "Set the downtime plan and tabletop status honestly.",
      "Record the last restore test or leave it missing for follow-up.",
    ],
    ask: [
      "Which workflows stop first if EHR, phones, billing, email, internet, or identity fails?",
      "Where are downtime forms or alternate workflows kept?",
      "Who decides when to switch to downtime mode and when to resume normal operations?",
    ],
    evidence: [
      "Downtime procedure reference.",
      "Backup restore test reference.",
      "Tabletop date, owner, and lessons reference.",
    ],
    doNot: [
      "Do not store patient schedules, message contents, or operational emergency details.",
      "Do not mark tested unless staff actually exercised the workflow.",
    ],
    sourceAlignment: [
      "HIPAA Security Rule contingency planning: availability of ePHI matters during disruption.",
      "NIST CSF Recover: recovery planning and communication should be ready before failure.",
    ],
  },
  evidence: {
    lane: "Proof index",
    question: "Can the owner prove the claim without exposing the sensitive artifact?",
    goal: "Build a reference-only evidence index that lets MSPs, vendors, reviewers, and owners find proof without copying sensitive records into the packet.",
    doNow: [
      "Use references, ticket IDs, folder paths, dates, and owners.",
      "Scan folder metadata only when the folder is appropriate for local indexing.",
      "Mark expired or needed evidence clearly instead of hiding gaps.",
    ],
    ask: [
      "Who owns each evidence item and how stale can it be?",
      "Which evidence must stay in a restricted folder or vendor portal?",
      "What proof can be safely summarized for the owner packet?",
    ],
    evidence: [
      "Reference title, type, owner, status, and related control.",
      "Date observed or review period when available.",
      "Private location reference, not copied sensitive contents.",
    ],
    doNot: [
      "Do not upload or paste records, screenshots, raw logs, full contracts, or private URLs.",
      "Do not let missing proof become hidden narrative text.",
    ],
    sourceAlignment: [
      "HHS recognized security practices: evidence matters when demonstrating security practices over time.",
      "NIST CSF Govern and Identify: risk communication improves when evidence is current and traceable.",
    ],
  },
  generate: {
    lane: "Owner packet",
    question: "What can the practice hand to the owner, MSP, vendor, or reviewer today?",
    goal: "Generate a focused packet that separates completed evidence from open decisions, without pretending the kit has made legal or compliance conclusions.",
    doNow: [
      "Review the open queue before generating.",
      "Refresh connector evidence if the packet depends on it.",
      "Generate locally, then use owner/MSP/vendor views for handoff.",
    ],
    ask: [
      "What are the top three decisions the owner must make after this packet?",
      "Which questions go to the MSP, vendors, or qualified reviewers?",
      "Which evidence should be refreshed before the next review period?",
    ],
    evidence: [
      "Completion summary and open-action queue.",
      "Connector summary and evidence freshness report.",
      "Owner, MSP, vendor, and reviewer views generated from the same profile.",
    ],
    doNot: [
      "Do not use the generated packet as a certification or legal conclusion.",
      "Do not send sensitive source evidence when a reference-only packet is enough.",
    ],
    sourceAlignment: [
      "NIST CSF: communicate risk across Govern, Identify, Protect, Detect, Respond, and Recover.",
      "HHS Security Rule: documentation and risk management should support appropriate safeguards over time.",
    ],
  },
};

function renderSectionPlaybook(sectionKey) {
  const playbook = SECTION_PLAYBOOKS[sectionKey];
  if (!playbook) return "";
  return `
    <section class="service-brief" aria-label="${escapeHtml(playbook.lane)} playbook">
      <div class="brief-head">
        <span class="step-pill">${escapeHtml(playbook.lane)}</span>
        <div>
          <strong>${escapeHtml(playbook.question)}</strong>
          <p>${escapeHtml(playbook.goal)}</p>
        </div>
      </div>
      <div class="guidance-grid compact-guidance">
        ${guidanceList("Do now", playbook.doNow)}
        ${guidanceList("Ask owner/MSP/vendor", playbook.ask)}
        ${guidanceList("Evidence required", playbook.evidence)}
        ${guidanceList("Do not enter", playbook.doNot)}
        ${guidanceList("Source alignment", playbook.sourceAlignment)}
      </div>
    </section>
  `;
}

function renderSectionPlaybooks() {
  $$("[data-playbook]").forEach((node) => {
    node.innerHTML = renderSectionPlaybook(node.dataset.playbook);
  });
}

function commandMetric(label, value, detail = "", tone = "") {
  return `
    <article class="command-metric ${tone}">
      <small>${escapeHtml(label)}</small>
      <strong>${escapeHtml(value)}</strong>
      ${detail ? `<span>${escapeHtml(detail)}</span>` : ""}
    </article>
  `;
}

function commandList(title, items) {
  const list = asList(items).slice(0, 5);
  if (!list.length) return "";
  return `
    <div class="command-list">
      <strong>${escapeHtml(title)}</strong>
      <ul>${list.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
    </div>
  `;
}

function renderCommandStrip(selector, eyebrow, title, body, metrics = [], actions = []) {
  const node = $(selector);
  if (!node) return;
  node.innerHTML = `
    <section class="owner-command" aria-label="${escapeHtml(eyebrow)}">
      <div class="command-copy">
        <span class="eyebrow">${escapeHtml(eyebrow)}</span>
        <strong>${escapeHtml(title)}</strong>
        <p>${escapeHtml(body)}</p>
      </div>
      <div class="command-metrics">${metrics.join("")}</div>
      ${actions.length ? commandList("Next owner moves", actions) : ""}
    </section>
  `;
}

function missingLabel(value) {
  const text = String(value ?? "").trim();
  return text || "Missing";
}

function countWhere(items, predicate) {
  return (items || []).filter(predicate).length;
}

function isHighRisk(value) {
  return ["high", "critical"].includes(String(value || "").toLowerCase());
}

function baaNeedsAttention(vendor) {
  return Boolean(vendor?.touches_ephi) && !["signed", "not applicable", "payer relationship"].includes(vendor.baa_status);
}

function evidenceNeedsAttention(item) {
  return ["needed", "requested", "expired"].includes(String(item?.status || "").toLowerCase());
}

function readinessGapLabels() {
  return READINESS_PRIORITY.filter((key) => !profile.readiness?.[key]).map((key) => READINESS_LABELS[key]);
}

function packetOpenActions() {
  const actions = [];
  if (!profile.practice?.security_owner || profile.practice.security_owner === "Practice Owner") actions.push("Name the real security owner for decisions and follow-up.");
  if (!(profile.systems || []).length) actions.push("Select systems before relying on vendor, flow, or evidence suggestions.");
  const baaCount = countWhere(profile.vendors, baaNeedsAttention);
  if (baaCount) actions.push(`Resolve ${baaCount} vendor BAA or contract status item${baaCount === 1 ? "" : "s"}.`);
  const highFlows = countWhere(profile.flows, (flow) => isHighRisk(flow.risk));
  if (highFlows) actions.push(`Review ${highFlows} high-risk ePHI flow${highFlows === 1 ? "" : "s"} with owner/MSP.`);
  const readinessGaps = readinessGapLabels();
  if (readinessGaps.length) actions.push(`Close readiness proof gaps starting with ${readinessGaps.slice(0, 2).join(" and ")}.`);
  const aiReview = countWhere(profile.ai_workflows, (workflow) => workflow.decision !== "allowed");
  if (aiReview) actions.push(`Review ${aiReview} restricted or prohibited AI workflow${aiReview === 1 ? "" : "s"}.`);
  const evidenceGaps = countWhere(profile.evidence, evidenceNeedsAttention);
  if (evidenceGaps) actions.push(`Update ${evidenceGaps} evidence reference${evidenceGaps === 1 ? "" : "s"} that are needed, requested, or expired.`);
  return actions.slice(0, 5);
}

function renderBasicsCommand() {
  renderCommandStrip(
    "#basics-command",
    "Owner decision map",
    "The packet is only useful if responsibility is explicit.",
    "A small practice does not need a giant committee; it needs one business owner, one technical owner, and a review window everyone can point to.",
    [
      commandMetric("Security owner", missingLabel(profile.practice?.security_owner), "Decision lane"),
      commandMetric("Technical owner", missingLabel(profile.practice?.technical_owner), "Evidence lane"),
      commandMetric("Practice size", `${profile.practice?.staff_count || 0} staff`, `${profile.practice?.locations || 0} location${profile.practice?.locations === 1 ? "" : "s"}`),
      commandMetric("Review period", missingLabel(profile.practice?.review_period), "Packet scope"),
    ],
    [
      "Confirm the owner can approve access, vendor, backup, downtime, and AI decisions.",
      "Confirm the technical owner can produce admin evidence without sending sensitive material.",
    ],
  );
}

function renderSystemsCommand() {
  const systems = profile.systems || [];
  const categories = new Set(systems.map((system) => system.category).filter(Boolean));
  const ephiSystems = countWhere(systems, (system) => String(system.ephi_role || "").toLowerCase() !== "none");
  renderCommandStrip(
    "#systems-command",
    "Operating surface",
    "This is the practice's practical attack and downtime map.",
    "If a system touches access, scheduling, billing, phones, files, backups, or ePHI, it belongs in the conversation before evidence is generated.",
    [
      commandMetric("Systems selected", systems.length, "Drives all suggestions", systems.length ? "" : "needs-work"),
      commandMetric("Categories", categories.size, "Care, admin, access, recovery"),
      commandMetric("ePHI touchpoints", ephiSystems, "Need safeguards and evidence"),
      commandMetric("Generated vendors", (profile.vendors || []).length, "After applying systems"),
    ],
    systems.length
      ? ["Ask the MSP which selected systems have admin MFA and backup coverage.", "Apply the list again after edits so suggestions stay aligned."]
      : ["Select the systems the practice uses, then apply them before vendor and flow review."],
  );
}

function renderVendorsCommand() {
  const vendors = profile.vendors || [];
  const ephiVendors = countWhere(vendors, (vendor) => vendor.touches_ephi);
  const baaCount = countWhere(vendors, baaNeedsAttention);
  const highRisk = countWhere(vendors, (vendor) => isHighRisk(vendor.risk));
  const aiUnknown = countWhere(vendors, (vendor) => ["unknown", "not reviewed"].includes(vendor.ai_training_use));
  renderCommandStrip(
    "#vendors-command",
    "Vendor pressure queue",
    "Every unknown vendor term becomes an owner decision.",
    "The valuable output here is not a vendor list; it is a short queue of BAAs, data-use terms, subcontractor questions, and incident-notice terms to chase.",
    [
      commandMetric("Vendors", vendors.length, "Generated plus manual"),
      commandMetric("Touch ePHI", ephiVendors, "Needs contract clarity"),
      commandMetric("BAA follow-up", baaCount, "Unknown or missing", baaCount ? "needs-work" : ""),
      commandMetric("High risk", highRisk, "Owner attention", highRisk ? "needs-work" : ""),
      commandMetric("AI/data unknown", aiUnknown, "Terms to ask"),
    ],
    [
      "Send high-risk vendors the evidence request before low-risk vendors.",
      "Ask whether customer data is used for AI training, model improvement, analytics, or subcontractors.",
      "Record incident notification terms for vendors that support care, identity, billing, or recovery.",
    ],
  );
}

function renderFlowsCommand() {
  const flows = profile.flows || [];
  const baaNeeded = countWhere(flows, (flow) => flow.baa_needed);
  const highRisk = countWhere(flows, (flow) => isHighRisk(flow.risk));
  const unconfirmed = countWhere(flows, (flow) => flow.confirmed === false);
  renderCommandStrip(
    "#flows-command",
    "ePHI movement map",
    "The hard question is not whether ePHI exists; it is where it moves.",
    "Use this page to force plain-English answers about source, destination, vendor, transmission method, and what proof is needed.",
    [
      commandMetric("Flows mapped", flows.length, "Generated plus manual"),
      commandMetric("Need BAA review", baaNeeded, "Contract lane"),
      commandMetric("High risk", highRisk, "Owner/MSP attention", highRisk ? "needs-work" : ""),
      commandMetric("Unconfirmed", unconfirmed, "Verify workflow", unconfirmed ? "needs-work" : ""),
    ],
    [
      "Review high-risk flows with the owner and MSP before packet generation.",
      "For each ePHI flow, identify the evidence reference that proves the safeguard or contract status.",
    ],
  );
}

function renderReadinessCommand() {
  const total = Object.keys(READINESS_LABELS).length;
  const ready = Object.values(profile.readiness || {}).filter(Boolean).length;
  const gaps = readinessGapLabels();
  renderCommandStrip(
    "#readiness-command",
    "Control proof sprint",
    "Unchecked is not failure; unchecked means no evidence yet.",
    "This turns the owner meeting into a focused sprint around the basics that usually reduce the most small-practice risk fastest.",
    [
      commandMetric("Ready", `${ready}/${total}`, "Evidence-backed items", ready < total ? "needs-work" : ""),
      commandMetric("Priority gaps", gaps.length, "High-value follow-up"),
      commandMetric("MFA posture", profile.readiness?.mfa_email && profile.readiness?.mfa_ehr ? "Both checked" : "Needs review", "Email and EHR"),
      commandMetric("Recovery proof", profile.readiness?.tested_backups ? "Recorded" : "Missing", "Restore test"),
    ],
    gaps.length
      ? gaps.slice(0, 4).map((gap) => `Get proof for ${gap}.`)
      : ["Keep evidence dates current and rerun this checklist next review period."],
  );
}

function renderAICommand() {
  const workflows = profile.ai_workflows || [];
  const allowed = countWhere(workflows, (workflow) => workflow.decision === "allowed");
  const restricted = countWhere(workflows, (workflow) => workflow.decision === "restricted");
  const prohibited = countWhere(workflows, (workflow) => workflow.decision === "prohibited");
  renderCommandStrip(
    "#ai-command",
    "AI safety boundary",
    "Most small practices need one simple rule staff can remember.",
    "Public AI tools are not the place for patient-level data unless a separate qualified review, contract path, and policy path have been handled outside this quick packet.",
    [
      commandMetric("Workflows", workflows.length, "Known AI uses"),
      commandMetric("Allowed", allowed, "Low-risk lane"),
      commandMetric("Restricted", restricted, "Needs terms or policy", restricted ? "needs-work" : ""),
      commandMetric("Prohibited", prohibited, "Do not use", prohibited ? "needs-work" : ""),
    ],
    [
      "Ask what staff actually paste into AI tools today.",
      "Require vendor terms and BAA review before any patient-data workflow moves out of restricted status.",
    ],
  );
}

function renderDowntimeCommand() {
  const criticalSystems = profile.downtime?.critical_systems || [];
  const planStatus = missingLabel(profile.downtime?.downtime_plan_status);
  const tabletopStatus = missingLabel(profile.downtime?.tabletop_status);
  const restoreTest = missingLabel(profile.downtime?.last_restore_test);
  renderCommandStrip(
    "#downtime-command",
    "Care continuity",
    "If this page is vague, the plan will fail under stress.",
    "The owner should be able to name what staff do when EHR, phones, internet, email, billing, identity, or backups are unavailable.",
    [
      commandMetric("Critical systems", criticalSystems.length, "Named by workflow", criticalSystems.length ? "" : "needs-work"),
      commandMetric("Plan status", planStatus, "Downtime lane", planStatus === "not documented" ? "needs-work" : ""),
      commandMetric("Restore test", restoreTest, "Recovery proof", restoreTest === "Missing" ? "needs-work" : ""),
      commandMetric("Tabletop", tabletopStatus, "Practice evidence", tabletopStatus === "not run" ? "needs-work" : ""),
    ],
    [
      "Ask staff how they handle scheduling, intake, prescribing, claims, phones, and messages during outage.",
      "Ask the MSP for the last restore-test reference and what systems it covered.",
    ],
  );
}

function renderEvidenceCommand() {
  const evidence = profile.evidence || [];
  const open = countWhere(evidence, evidenceNeedsAttention);
  const collected = countWhere(evidence, (item) => ["collected", "reviewed"].includes(String(item.status || "").toLowerCase()));
  const sensitiveFlags = countWhere(evidence, (item) => item.stores_sensitive_content);
  renderCommandStrip(
    "#evidence-command",
    "Evidence discipline",
    "References are the product; sensitive source material stays where it belongs.",
    "This index should tell a reviewer where proof exists, who owns it, whether it is stale, and what still has to be requested.",
    [
      commandMetric("References", evidence.length, "Total evidence rows"),
      commandMetric("Collected/reviewed", collected, "Usable now"),
      commandMetric("Needs attention", open, "Needed, requested, expired", open ? "needs-work" : ""),
      commandMetric("Sensitive flags", sensitiveFlags, "Keep restricted", sensitiveFlags ? "needs-work" : ""),
    ],
    [
      "Replace narrative claims with evidence references wherever possible.",
      "Use metadata-only inventory for folders; keep sensitive contents outside the packet.",
    ],
  );
}

function renderPacketCommand() {
  const actions = packetOpenActions();
  renderCommandStrip(
    "#packet-command",
    "Handoff quality gate",
    actions.length ? "The packet is useful now, but the open queue is where the value is." : "The packet is ready for a clean owner/MSP handoff.",
    "Generate only after the owner queue is visible. The best packet separates what is known, what is missing, and who owns each next move.",
    [
      commandMetric("Systems", (profile.systems || []).length, "Selected"),
      commandMetric("Vendors", (profile.vendors || []).length, "To review"),
      commandMetric("Flows", (profile.flows || []).length, "Mapped"),
      commandMetric("Open actions", actions.length, "Before handoff", actions.length ? "needs-work" : ""),
    ],
    actions.length ? actions : ["Generate the packet and use the owner/MSP/vendor views for follow-up."],
  );
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
  renderBasicsCommand();
  $("#basics-form").innerHTML = fields.map(([label, path, type]) => `<label>${label}${textInput(path.split(".").reduce((o, k) => o[k], profile), path, type || "text")}</label>`).join("");
}

function renderSystems() {
  const selected = new Set(profile.systems.map((system) => system.catalog_key));
  renderSystemsCommand();
  $("#systems-list").innerHTML = Object.entries(catalogs.system_catalog.systems).map(([key, item]) => `
    <label class="check-card">
      <input type="checkbox" data-system-key="${key}" ${selected.has(key) ? "checked" : ""}>
      <span><strong>${escapeHtml(item.name)}</strong><small>${escapeHtml(item.description)}</small><small><b>Evidence:</b> ${escapeHtml(item.evidence_needed)}</small></span>
    </label>
  `).join("");
}

function renderVendors() {
  renderVendorsCommand();
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
  renderFlowsCommand();
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
  renderReadinessCommand();
  $("#readiness-list").innerHTML = Object.entries(READINESS_LABELS).map(([key, label]) => `
    <label class="task-row"><input type="checkbox" ${profile.readiness[key] ? "checked" : ""} data-path="readiness.${key}"><span><strong>${label}</strong><small>Use an evidence reference instead of storing sensitive screenshots here.</small></span></label>
  `).join("");
}

function renderAI() {
  renderAICommand();
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
  if (!timeline.length) {
    $("#incident-timeline").innerHTML = `<div class="empty-state">No incident phases yet. Load a scenario template or add a timeline event.</div>`;
  } else {
    activeIncidentIndex = Math.min(Math.max(activeIncidentIndex, 0), timeline.length - 1);
    const active = timeline[activeIncidentIndex];
    const completeCount = timeline.filter((entry) => entry.complete || entry.status === "closed").length;
    const phaseNav = timeline.map((entry, index) => `
      <button class="phase-step ${index === activeIncidentIndex ? "active" : ""} ${entry.complete ? "done" : ""}" type="button" data-incident-phase="${index}">
        <span>${escapeHtml(entry.time || `Step ${index + 1}`)}</span>
        <strong>${escapeHtml(entry.phase || `Event ${index + 1}`)}</strong>
        <small>${escapeHtml(phaseStatusLabel(entry))}</small>
      </button>
    `).join("");
    $("#incident-timeline").innerHTML = `
      <div class="phase-workflow">
        <div class="phase-nav" aria-label="Incident phases">${phaseNav}</div>
        <article class="runner-card active-phase">
          <div class="runner-card-head">
            <div>
              <span class="step-pill">${escapeHtml(active.phase || `Event ${activeIncidentIndex + 1}`)}</span>
              <h3>${escapeHtml(active.primary_question || active.decision_gate || "What decision needs to be made now?")}</h3>
              <p>${escapeHtml(active.plain_english_goal || "Confirm facts, owner, evidence reference, and next action.")}</p>
            </div>
            <button class="danger compact" type="button" data-incident-remove="timeline:${activeIncidentIndex}">Remove</button>
          </div>

          <div class="phase-progress">
            <span><b>${completeCount}/${timeline.length}</b> phases complete</span>
            <label class="checkline">
              <input type="checkbox" ${active.complete ? "checked" : ""} data-path="incident_timeline.timeline.${activeIncidentIndex}.complete">
              Phase complete
            </label>
          </div>

          <div class="phase-question-strip">
            <span><b>Owner lane:</b> ${escapeHtml(active.owner_lane || "Owner/MSP")}</span>
            <span><b>Current owner:</b> ${escapeHtml(active.owner || "Practice owner")}</span>
          </div>

          <div class="guidance-grid">
            ${guidanceList("Source alignment", active.source_alignment)}
            ${guidanceList("Do now", active.do_now)}
            ${guidanceList("Ask MSP/vendor", active.ask_msp_or_vendor)}
            ${guidanceList("Evidence required", active.evidence_required)}
            ${guidanceList("Completion criteria", active.completion_criteria)}
            ${guidanceList("Escalation triggers", active.escalation_triggers)}
            ${guidanceList("Safe to record", active.allowed_inputs)}
            ${guidanceList("Do not record", active.blocked_inputs)}
          </div>

          <div class="phase-script">
            <strong>Staff script</strong>
            <p>${escapeHtml(active.staff_script || "Keep details sanitized and route private evidence to the owner.")}</p>
          </div>

          <div class="form-grid runner-grid">
            <label>Time${textInput(active.time, `incident_timeline.timeline.${activeIncidentIndex}.time`)}</label>
            <label>Phase${textInput(active.phase, `incident_timeline.timeline.${activeIncidentIndex}.phase`)}</label>
            <label>Owner${textInput(active.owner, `incident_timeline.timeline.${activeIncidentIndex}.owner`)}</label>
            <label>Owner lane${textInput(active.owner_lane || "Owner/MSP", `incident_timeline.timeline.${activeIncidentIndex}.owner_lane`)}</label>
            <label>Status${selectInput(active.status, `incident_timeline.timeline.${activeIncidentIndex}.status`, ["requested", "open", "needs review", "in progress", "closed"])}</label>
            <label>Private evidence reference${textInput(active.evidence_ref, `incident_timeline.timeline.${activeIncidentIndex}.evidence_ref`)}</label>
            <label class="wide">System or workflow category<textarea data-incident-systems="${activeIncidentIndex}">${escapeHtml((active.systems || []).join("\n"))}</textarea></label>
            <label class="wide">Sanitized event category${textareaInput(active.event, `incident_timeline.timeline.${activeIncidentIndex}.event`)}</label>
            <label class="wide">Decision gate${textareaInput(active.decision_gate, `incident_timeline.timeline.${activeIncidentIndex}.decision_gate`)}</label>
          </div>
        </article>
      </div>
    `;
  }

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
  renderDowntimeCommand();
  $("#downtime-form").innerHTML = `
    <label>Downtime plan status${selectInput(profile.downtime.downtime_plan_status, "downtime.downtime_plan_status", ["not documented", "draft", "documented", "tested"])}</label>
    <label>Last restore test${textInput(profile.downtime.last_restore_test, "downtime.last_restore_test")}</label>
    <label>Tabletop status${selectInput(profile.downtime.tabletop_status, "downtime.tabletop_status", ["not run", "scheduled", "run", "lessons recorded"])}</label>
    <label>Critical systems<textarea data-critical-systems>${escapeHtml(profile.downtime.critical_systems.join("\n"))}</textarea></label>
  `;
}

function renderEvidence() {
  renderEvidenceCommand();
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
  renderPacketCommand();
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
  renderSectionPlaybooks();
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
  profile.incident_timeline = data.incident_timeline;
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
  const initialSection = requestedSection();
  if (initialSection) navTo(initialSection);

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
      activeIncidentIndex = 0;
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
    const incidentPhase = target.closest("[data-incident-phase]");
    const incidentRemove = target.closest("[data-incident-remove]");
    if (incidentPhase) {
      collectCurrentEdits();
      activeIncidentIndex = Number(incidentPhase.dataset.incidentPhase) || 0;
      renderIncidentRunner();
      return;
    }
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
    activeIncidentIndex = profile.incident_timeline.timeline.length - 1;
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
