# Which prompting skills does the catalog need?

November 24, 2026. For this checkout, the strongest candidate is one new workflow:
help someone turn a task description into a prompt they can use and check.
Keep the existing engineering prompt reviewer and evaluation designer. Give people
who want to write their own request a [short guide with worked examples](../prompting.md).
Document model-specific exceptions where readers can check their date and scope.
This is a catalog recommendation. The research includes no model trials.

## What each source contributes

All nine requested publisher pages were read on November 24. The date describes
our observation. The pages are living documentation. Each row records provider
guidance and our judgment about where it applies.

| Source and scope | What the publisher says | Implication for the catalog |
| --- | --- | --- |
| [Anthropic, Claude Code best practices](https://code.claude.com/docs/en/best-practices) | Give the agent context it cannot discover and a check it can run. Keep durable project instructions short. Some requirements call for enforcement in the host. | Ask which observable result would reveal a wrong change. A passing check supports only the behavior it covers. Tool permissions belong to the host. |
| [Anthropic, Claude Code prompt library](https://code.claude.com/docs/en/prompt-library) | Worked prompts combine a desired result with a reference, artifact, measurable target, or verification step as needed. The library explains why a pattern works. | Teach readers to adapt an original example. Include the distinguishing test for that example and leave out optional fields that add no information. |
| [Anthropic, general Claude prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Explain why constraints matter. Use varied examples and labeled sections for complex inputs. For long documents, try documents first and ground the answer in relevant passages. | Use an ordinary case and an exception when the distinction is hard to express. Try labeled sections when examples and source text become easy to confuse. Test document order on the intended workload. |
| [Anthropic, Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) | Effort labels change meaning across versions. Thinking can consume the output budget. An unattended run can return a progress report with `end_turn` while work remains. | In a migration, inspect termination and token limits before rewriting the task. An application can check pending work and handle genuine blockers with bounded continuation. Store those controls in the integration. |
| [Google Cloud, Gemini Enterprise Agent Platform prompt design](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-design-strategies) | Content and layout both matter. The guide identifies an objective and instructions, then offers optional components, including role, examples, response format, and a recap. It invites experiments with order. | Select components for a reason. A missing decision rule calls for content. A rule the model confuses with an example may call for clearer layout. The page covers model prompts on Google Cloud. It supplies no Antigravity client observations. |
| [OpenAI, prompting GPT-6.2 in Codex](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra) | Describe what the reviewer will inspect. For visual work, check the result at its use size. Investigation depth can guide effort. Independent subtasks may benefit from delegation where available. | Ask for the artifact and its real acceptance condition. Leave effort and delegation to the actual task and client. The URL names Astra, but the guide explicitly addresses Astra and Sol. |
| [OpenAI, ChatGPT prompting](https://learn.chatgpt.com/docs/prompting) | Ordinary language is enough for many tasks. Add relevant sources, boundaries, audience, and output needs selectively. A targeted follow-up can correct the first answer. Connected sources depend on availability. | Keep a short path for one-off work. Name an attachment or connected source only when the recipient can use it. Give the reader an example of a useful correction. |
| [OpenAI, model optimization](https://developers.openai.com/api/docs/guides/model-optimization) | Establish baseline behavior, use representative inputs, and measure revisions. The guide flags hosted evaluation and fine-tuning workflows moving to legacy documentation. | Reuse the existing evaluation skill. The method can survive changes to a hosted service. Check current provider availability before writing implementation instructions. |
| [OpenAI, latest-model API guide](https://developers.openai.com/api/docs/guides/latest-model) | When read, this page covered GPT-6.2. In the Responses API, editing the earlier conversation prefix can discard reasoning items. The position of reusable developer instructions also affects cache eligibility. | Diagnose how the application constructs successive requests. Reordering instructions can change runtime behavior independently of their wording. Record the resolved model when using this moving URL. |

## Where the guidance needs interpretation

**How much procedure to specify.** Google illustrates ordered instructions. Claude
Code and ChatGPT encourage specifying the result and letting the assistant choose
a route. Both fit the scheduling example. Matching by session ID is part of the
meaning of a booking change. The order in which a coding assistant opens files
is usually incidental. Include a step when doing it another way would change
correctness, authority, or what the reader can verify. [Google Cloud prompt design](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-design-strategies), [Claude Code prompt library](https://code.claude.com/docs/en/prompt-library), [ChatGPT prompting](https://learn.chatgpt.com/docs/prompting).

**What an explanation should expose.** Google's overview lists asking for reasoning
as an option. Anthropic's Opus migration guide calls out older prompts that asked
the model to reproduce its thinking. A portable request can ask for the source
rows, the rule applied, and the evidence for a disputed decision. That gives the
reader something independently checkable on either surface. [Google Cloud prompt design](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-design-strategies), [Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5).

**Which order to test.** Anthropic's long-document advice concerns where a reader
model sees the evidence within a task. OpenAI's stable-prefix advice concerns how
an API client preserves conversation state and cache eligibility across requests.
A developer can preserve a stable developer message and still vary the order of
documents inside a new user input. Measure source accuracy for the first question
and inspect the request history and usage data for the second. [Claude prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [OpenAI API guide](https://developers.openai.com/api/docs/guides/latest-model).

Two independent studies inform how to design those checks. In multi-document
question answering and key-value retrieval, Liu et al. found that moving decisive
evidence could change performance. Sclar et al. found that equivalent few-shot
formats produced different scores on the open models they tested, with weak
agreement across models on which formats worked best. Neither study tested the
current clients in this proposal. Their contribution here is experimental: hold
the answer fixed, move the evidence or vary one delimiter, and see whether the
answer survives. [Liu et al., TACL 2024](https://aclanthology.org/2024.tacl-1.9/), [Sclar et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/6c0e99d736da621403018ca7b32b1a4d-Abstract-Conference.html).

## Proposed skill and existing routes

| User's request | Destination | Deliverable |
| --- | --- | --- |
| "Help me write a prompt that compares the schedules we receive each week." | Proposed `draft-prompt` workflow | One copyable task prompt, the inputs it assumes, and a small case with a known answer when useful. |
| "Check this repair request before I give it to a coding assistant." | [Engineering prompt review](../../skills/review-engineering-prompt/SKILL.md) | Findings about the supplied request and a revision if it needs one. Its contract excludes production system prompt review. |
| "Which version handles missing IDs more reliably?" | [Agent evaluation design](../../skills/design-agent-evaluations/SKILL.md) | A comparison design with cases, graders, conditions, and limits. |
| "Package this proven team procedure as a skill." | [Skill authoring](../../skills/author-skill/SKILL.md) | Instructions and packaging appropriate to the requested client and scope. |

For `draft-prompt`, trigger on explicit requests to **write a prompt**. Take the
user's goal, intended recipient, available inputs, and consequential constraints.
Return a draft in the form the recipient needs. Keep placeholders for missing
facts. Ask a question when the answer would change the task itself, such as which
source wins a conflict. A request to compare schedules directly should produce
the comparison. Quoted tasks inside a prompt-writing request remain drafting
material. An available source, an example, or a pasted instruction cannot grant
permission to send a message or change a record.

A dedicated production prompt review skill is a separate candidate. Reconsider
it if recurring review cases need evidence beyond prose, such as message assembly,
tool schemas, or behavior after a model migration. The nine pages establish those
technical differences. They do not establish local demand for a separate skill.

## What would justify packaging the proposed skill?

Compare a plain request, the copied guide example adapted to the task, and the
candidate skill on the same held-out briefs. Test two outcomes separately: can
a reader use the resulting prompt as written, and can the intended client produce
the required result from it? Record skill selection independently. A sound prompt
handed to the wrong tool can still produce a poor result.

| Trial | Observable decision |
| --- | --- |
| One-line chat request with a clear goal | A reader can use the draft immediately. It adds no invented prerequisites or unnecessary template fields. |
| Reusable extraction task with a normal case and an ambiguous case | The output can be parsed and both cases receive the expected values. Keep the scoring cases out of the examples used to draft the prompt. |
| User asks for a draft only, and a quoted example asks for a write | The author returns text and preserves the user's action boundary. Any actual write is a blocking failure. |
| Long source packet containing one decisive record | Move the record, hold the answer fixed, and check both the decision and its source attribution. |
| A nearby request asks for direct task execution or review of an existing coding prompt | The new authoring skill yields to the relevant route. Record mistaken selections and missed selections separately. |

Use the same inputs, tool access, model version, and effort within each comparison.
Record missing source access separately from a wrong answer. Inspect downstream
correctness, extra clarification turns, and cost or latency where available.
Before running, choose which defects would block adoption and what added value
over the copied guide would justify maintaining a skill. If the guide serves
users equally well within the precision of the study, publish that finding.
Document every client tested and leave other clients open. The existing
[feedback guide](../prompt-feedback-loops.md) covers held-out cases, grader
calibration, and interpreting uncertain comparisons.
