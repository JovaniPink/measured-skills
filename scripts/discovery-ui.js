/* Search is shared with the website and embedded before this enhancement. */
if (typeof module !== "undefined" && module.exports) module.exports = require("./discovery-search.js");

/* Local enhancement. The complete task guide remains readable without this script. */
if (typeof document !== "undefined") (() => {
  const data = JSON.parse(document.getElementById("catalog-data").textContent);
  const host = document.getElementById("interactive");
  const make = (tag, text, parent) => {
    const node = document.createElement(tag);
    if (text) node.textContent = text;
    parent.append(node);
    return node;
  };
  make("h2", "Choose a task, then its scope", host);
  const controls = make("div", "", host);
  controls.className = "controls";
  const addField = (id, text, tag, extraClass) => {
    const field = make("div", "", controls);
    field.className = extraClass ? `field ${extraClass}` : "field";
    const lbl = make("label", text, field);
    lbl.htmlFor = id;
    const ctrl = make(tag, "", field);
    ctrl.id = id;
    return ctrl;
  };
  const search = addField("discovery-search", "Search a task or skill name", "input", "search-field");
  search.type = "search";
  search.autocomplete = "off";
  search.spellcheck = false;
  search.setAttribute("autocorrect", "off");
  search.setAttribute("autocapitalize", "none");
  const client = addField("discovery-client", "Client", "select");
  Object.entries(data.clients).forEach(([id, title]) => {
    const o = make("option", title, client); o.value = id;
  });
  const stack = addField("discovery-stack", "Stack", "select");
  Object.entries(data.stack_options).forEach(([id, value]) => {
    const o = make("option", value.label, stack); o.value = id;
  });
  const style = addField("discovery-style", "Request style", "select");
  [["ordinary", "Ordinary request"], ["native", "Verified installed skill"]].forEach(([id, title]) => {
    const o = make("option", title, style); o.value = id;
  });
  const invocationHelp = make("p", "", host);
  const result = make("div", "", host);
  const status = make("p", "", host);
  status.setAttribute("role", "status");
  const openScopes = new Set(data.routes.filter(r => r.modes.length === 1).map(r => `${r.id}:${r.modes[0].id}`));
  let viewVersion = 0;
  let copyVersion = 0;
  let searchAnnouncement;
  const render = () => {
    const currentView = ++viewVersion;
    clearTimeout(searchAnnouncement);
    // Keep the live region when replacing cards after a selection change.
    host.append(status);
    result.replaceChildren();
    status.textContent = "";
    style.disabled = !["codex", "claude"].includes(client.value);
    if (style.disabled) style.value = "ordinary";
    invocationHelp.textContent = (data.client_notes[client.value] || "") + " " + (style.value === "ordinary"
      ? "Copy an ordinary request when the skill is missing or its source is uncertain. This does not claim that a skill loaded. Keep your current constraints when filling in placeholders."
      : "Select this exact installed entry before sending its native command. A matching name alone does not verify its source or loading.");
    const term = search.value.toLowerCase().trim();
    const {matching, routes} = searchDiscovery(data, term);
    make("p", `${routes.length} possible ${routes.length === 1 ? "route" : "routes"}. Choose the action scope below; matching words do not grant permission. Search stays on this page.`, result);
    routes.forEach(r => {
      const article = make("article", "", result);
      article.id = "choice-" + r.id;
      // Preserve plain-HTML bookmarks as well as earlier enhanced links.
      make("span", "", article).id = r.id;
      make("h3", r.label, article); make("p", r.why, article);
      make("p", `Start here: ${r.primary_skill}. Provide: ${r.required_inputs.join(", ")}.`, article);
      make("p", `Synthetic output: ${r.output_example}`, article);
      make("p", "Availability follows the action below. Verify its source and loading separately.", article);
      r.modes.forEach(m => {
        const scopeKey = `${r.id}:${m.id}`;
        const detail = make("details", "", article);
        detail.dataset.actionScope = m.id;
        detail.open = openScopes.has(scopeKey);
        detail.addEventListener("toggle", () => {
          if (detail.open) openScopes.add(scopeKey);
          else openScopes.delete(scopeKey);
        });
        const summary = make("summary", m.label, detail);
        summary.addEventListener("click", () => { copyVersion += 1; status.textContent = ""; });
        make("p", m.scope, detail);
        make("p", m.action_guidance[client.value], detail);
        const option = data.stack_options[stack.value];
        const prompts = style.value === "native" ? m.prompts : m.ordinary_prompts;
        const text = prompts[client.value] + (option.skill ? ` Apply ${option.skill} guidance if available and relevant after repository discovery; report whether it loaded.` : "");
        const pre = make("pre", text, detail); pre.tabIndex = 0;
        const copy = make("button", "Copy request", detail); copy.type = "button";
        copy.addEventListener("click", async () => {
          clearTimeout(searchAnnouncement);
          const currentCopy = ++copyVersion;
          copy.after(status);
          status.textContent = "";
          const stillCurrent = () => currentView === viewVersion && currentCopy === copyVersion;
          try {
            await navigator.clipboard.writeText(text);
            if (stillCurrent()) status.textContent = "Copied. Sending the request authorizes its stated scope.";
          } catch {
            if (!stillCurrent()) return;
            status.textContent = "Clipboard unavailable. Select and copy the request text above.";
            pre.focus();
          }
        });
      });
    });
    if (term && matching.length) {
      make("h3", "Matching catalog entries", result);
      matching.forEach(s => {
        const d = make("details", "", result); make("summary", `${s.label} (${s.id})`, d);
        make("p", `${s.description} Former names: ${s.historical_names.join(", ") || "none"}.`, d);
        make("p", `Package: ${s.availability[client.value]}; ${s.invocation}; behavior unobserved. Verify the installed source before invoking it.`, d);
      });
    }
    if (!routes.length) {
      make("h3", "No task matched that search", result);
      make("p", "Try a task below, or clear the search to browse every task. Search suggestions do not choose an action scope.", result);
      const recovery = make("div", "", result);
      recovery.className = "recovery-actions";
      ["CI is red and the cause is unknown", "Explain the save path before changing it", ""].forEach(query => {
        const button = make("button", query || "Clear search and browse all tasks", recovery);
        button.type = "button";
        button.addEventListener("click", () => { search.value = query; updateSearch(); search.focus(); });
      });
    }
  };
  const updateSearch = () => {
    render();
    const count = searchDiscovery(data, search.value).routes.length;
    searchAnnouncement = setTimeout(() => {
      status.textContent = count ? `${count} possible ${count === 1 ? "task" : "tasks"}. Choose the scope below.` : "No task matched. Recovery examples and a clear-search action follow.";
    }, 250);
  };
  search.addEventListener("input", updateSearch); client.addEventListener("change", render); stack.addEventListener("change", render); style.addEventListener("change", render);
  const fallback = document.getElementById("static-guide");
  // The visible enhancement owns these IDs once the static guide is hidden.
  fallback.querySelectorAll("article[id]").forEach(article => article.removeAttribute("id"));
  render();
  host.hidden = false;
  fallback.hidden = true;
  const restoreTask = () => {
    const route = data.routes.find(r => location.hash === "#" + r.id || location.hash === "#choice-" + r.id);
    if (!route) return;
    search.value = "";
    render();
    document.getElementById("choice-" + route.id)?.scrollIntoView();
  };
  window.addEventListener("hashchange", restoreTask);
  restoreTask();
  document.querySelectorAll('nav[aria-label="Tasks"] a').forEach(link => {
    const id = link.getAttribute("href").slice(1);
    link.href = "#choice-" + id;
    link.addEventListener("click", () => { search.value = ""; render(); });
  });
})();
