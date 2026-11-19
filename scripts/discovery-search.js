/* Shared deterministic lookup. Matches suggest tasks, never authorize actions. */
function searchDiscovery(data, query) {
  const normalize = value => value.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
  const term = normalize(query);
  if (!term) return {matching: query.trim() ? [] : data.skills, routes: query.trim() ? [] : data.routes};
  const stop = new Set("a an and are as at be before by can did do does for from how i in is it me my of on or please the this to was what when with you your".split(" "));
  const tokens = value => new Set(normalize(value).split(" ").filter(word => !stop.has(word)));
  const words = tokens(term);
  const contains = (text, phrase) => (` ${text} `).includes(` ${phrase} `);
  const score = phrase => {
    const normalized = normalize(phrase);
    if (term === normalized) return 100;
    if (normalized.includes(term)) return 60;
    if (normalized.includes(" ") && contains(term, normalized)) return 80;
    const candidate = tokens(normalized);
    const overlap = [...candidate].filter(word => words.has(word)).length;
    // Two meaningful words prevent broad one-word guesses in full sentences.
    return overlap >= 2 ? 20 + 20 * overlap / Math.max(candidate.size, words.size) : 0;
  };
  const matching = data.skills.filter(s => [s.id, s.label, ...s.historical_names].some(name => {
    const normalized = normalize(name);
    return normalized.includes(term) || (normalized.includes(" ") && contains(term, normalized));
  }) || normalize(s.description).includes(term));
  const ranked = data.routes.map((route, index) => {
    const phrases = [route.label, ...route.search_phrases];
    const scores = phrases.map(score);
    const best = Math.max(...scores, matching.some(s => route.search_skills.includes(s.id)) ? 10 : 0);
    // A specific task inside a sentence outranks its generic phrase, such as
    // "prepare my change for code review" before "code review". Keep the
    // existing thresholds and registry order for equally specific matches.
    const specificity = best === 80 ? Math.max(...phrases.map((phrase, i) =>
      scores[i] === best ? tokens(phrase).size : 0)) : 0;
    return {route, index, score: best, specificity};
  }).filter(item => item.score > 0);
  ranked.sort((a,b) => b.score - a.score || b.specificity - a.specificity || a.index - b.index);
  const confident = ranked.some(item => item.score >= 60);
  const named = matching.length > 0;
  return {matching, routes: ranked.filter(item => confident ? item.score >= 60 : (!named || matching.some(s => item.route.search_skills.includes(s.id)))).map(item => item.route)};
}
if (typeof module !== "undefined" && module.exports) module.exports = {searchDiscovery};
