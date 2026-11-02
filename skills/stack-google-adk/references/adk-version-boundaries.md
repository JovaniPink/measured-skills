# Google ADK Version Boundaries

Use this reference to keep framework claims tied to exact evidence.

## Discovery record

| Boundary | Evidence to record |
| --- | --- |
| Language | Python, TypeScript, or Go project evidence |
| ADK package | Exact package name, resolved version, and lockfile |
| Model | Provider, model identifier, configuration, and authority |
| Agents | Agent types, hierarchy, delegation, and stopping rules |
| Tools | Registered tool names, schemas, effects, identity, and policy |
| State | Session service, state scopes, persistence, and retention |
| Memory | Memory service, retrieval policy, provenance, and deletion |
| Runtime skills | `SkillToolset` version, allowed bundle contents, integrity, and revocation |
| Evaluation | Case set, trajectory checks, final-output checks, and thresholds |
| Deployment | Proposed environment and separate deployment authority |

## Primary resources

- [Google ADK documentation](https://adk-labs.github.io/adk-docs/)
- [ADK Agent Skills](https://adk-labs.github.io/adk-docs/skills/)
- [ADK sessions and state](https://adk-labs.github.io/adk-docs/sessions/)
- [ADK evaluation](https://adk-labs.github.io/adk-docs/evaluate/)
- [ADK safety and security](https://adk-labs.github.io/adk-docs/safety/)
- [ADK tool confirmation](https://adk-labs.github.io/adk-docs/tools-custom/confirmation/)

Confirm the installed version before relying on an API or experimental feature. Documentation for a newer release is not evidence about an older locked environment.
