/* Local enhancement. The complete task guide remains readable without this script. */
(() => {
  const data = JSON.parse(document.getElementById("catalog-data").textContent);
  const host = document.getElementById("interactive");
  const make = (tag, text, parent) => {
    const node = document.createElement(tag);
    if (text) node.textContent = text;
    parent.append(node);
    return node;
  };
  make("h2", "Find a route", host);
  const label = make("label", "Search tasks or old skill names ", host);
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
  const result = make("div", "", host);
  const status = make("p", "", host);
  status.setAttribute("role", "status");
  const render = () => {
    result.replaceChildren();
    const term = search.value.toLowerCase().trim();
    const matching = data.skills.filter(s => [s.id, s.label, s.description, ...s.historical_names].join(" ").toLowerCase().includes(term));
    const routes = data.routes.filter(r => !term || [r.label, r.why, ...r.search_phrases].join(" ").toLowerCase().includes(term) || matching.some(s => r.primary_skill === s.id || r.optional_skills.includes(s.id)));
    make("p", `${routes.length} routes. Search stays on this page.`, result);
    routes.forEach(r => {
      const article = make("article", "", result);
      article.id = "choice-" + r.id;
      make("h3", r.label, article); make("p", r.why, article);
      make("p", `Start here: ${r.primary_skill}. Provide: ${r.required_inputs.join(", ")}.`, article);
      make("p", `Synthetic output: ${r.output_example}`, article);
      make("p", "Availability follows the action below. Verify its source and loading separately.", article);
      r.modes.forEach(m => {
        const detail = make("details", "", article);
        detail.dataset.actionScope = m.id;
        make("summary", m.label, detail); make("p", m.scope, detail);
        make("p", m.action_guidance[client.value], detail);
        const option = data.stack_options[stack.value];
        const text = m.prompts[client.value] + (option.skill ? ` Apply ${option.skill} guidance if available and relevant after repository discovery; report whether it loaded.` : "");
        const pre = make("pre", text, detail); pre.tabIndex = 0;
        const copy = make("button", "Copy request", detail); copy.type = "button";
        copy.addEventListener("click", async () => {
          try { await navigator.clipboard.writeText(text); status.textContent = "Copied. Sending the request authorizes its stated scope."; }
          catch { status.textContent = "Clipboard unavailable. Select and copy the request text above."; pre.focus(); }
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
  search.addEventListener("input", render); client.addEventListener("change", render); stack.addEventListener("change", render);
  render();
  host.hidden = false;
  document.getElementById("static-guide").hidden = true;
  document.querySelectorAll('nav[aria-label="Tasks"] a').forEach(link => {
    const id = link.getAttribute("href").slice(1);
    link.href = "#choice-" + id;
    link.addEventListener("click", () => { search.value = ""; render(); });
  });
})();
