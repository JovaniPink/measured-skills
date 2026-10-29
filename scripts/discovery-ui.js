/* Pure local lookup shared by the page and regression checks. */
function searchDiscovery(data, query) {
  const normalize = value => value.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
  const term = normalize(query);
  const contains = (text, phrase) => (` ${text} `).includes(` ${phrase} `);
  // Only reviewed multiword phrases and names match inside longer requests.
  // This is literal lookup, not intent detection or authorization analysis.
  const mentioned = phrases => phrases.some(value => {
    const phrase = normalize(value);
    return phrase.includes(" ") && contains(term, phrase);
  });
  const matching = data.skills.filter(s => {
    const names = [s.id, s.label, ...s.historical_names];
    return contains(normalize([...names, s.description].join(" ")), term) || mentioned(names);
  });
  const routes = data.routes.filter(r => !term ||
    contains(normalize([r.label, r.why, ...r.search_phrases].join(" ")), term) ||
    mentioned([r.label, ...r.search_phrases]) || matching.some(s => r.search_skills.includes(s.id)));
  return {matching, routes};
}
if (typeof module !== "undefined" && module.exports) module.exports = {searchDiscovery};

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
  make("h2", "Find a route", host);
  const label = make("label", "Search a task or skill name ", host);
  const search = make("input", "", label);
  search.type = "search";
  search.autocomplete = "off";
  const cl = make("label", "Client ", host);
  const client = make("select", "", cl);
  Object.entries(data.clients).forEach(([id, title]) => {
    const o = make("option", title, client); o.value = id;
  });
  const sl = make("label", "Stack ", host);
  const stack = make("select", "", sl);
  Object.entries(data.stack_options).forEach(([id, value]) => {
    const o = make("option", value.label, stack); o.value = id;
  });
  const styleLabel = make("label", "Request style ", host);
  const style = make("select", "", styleLabel);
  [["ordinary", "Ordinary request"], ["native", "Verified installed skill"]].forEach(([id, title]) => {
    const o = make("option", title, style); o.value = id;
  });
  const invocationHelp = make("p", "", host);
  const result = make("div", "", host);
  const status = make("p", "", host);
  status.setAttribute("role", "status");
  let viewVersion = 0;
  let copyVersion = 0;
  const render = () => {
    const currentView = ++viewVersion;
    // Keep the live region when replacing cards after a selection change.
    host.append(status);
    result.replaceChildren();
    status.textContent = "";
    style.disabled = !["codex", "claude"].includes(client.value);
    if (style.disabled) style.value = "ordinary";
    invocationHelp.textContent = style.value === "ordinary"
      ? "Copy an ordinary request when the skill is missing or its source is uncertain. This does not claim that a skill loaded. Keep your current constraints when filling in placeholders."
      : "Select this exact installed entry before sending its native command. A matching name alone does not verify its source or loading.";
    const term = search.value.toLowerCase().trim();
    const {matching, routes} = searchDiscovery(data, term);
    make("p", `${routes.length} possible routes. Choose the action scope below; matching words do not grant permission. Search stays on this page.`, result);
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
        const detail = make("details", "", article);
        detail.dataset.actionScope = m.id;
        detail.open = r.id === data.default_route && m.id === "assess";
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
    if (!routes.length && !matching.length) make("p", "No match. Try a shorter task phrase or browse the complete catalog below.", result);
  };
  search.addEventListener("input", render); client.addEventListener("change", render); stack.addEventListener("change", render); style.addEventListener("change", render);
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
