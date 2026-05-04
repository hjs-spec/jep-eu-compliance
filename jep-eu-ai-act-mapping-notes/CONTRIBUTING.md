# Contributing to JEP EU Multi-Industry Compliance Extensions

Thank you for considering a contribution. This project follows the same narrow-waist philosophy as JEP itself: the core grammar (J/D/T/V) does not change. All contributions must preserve this invariant.

## What We Accept

| Type | Example | Review Priority |
|------|---------|-----------------|
| New industry extension | Education, law enforcement, insurance | High |
| Schema corrections | Bug in JSON Schema pattern or enum | Immediate |
| Additional jurisdictions | UK AI Act, Singapore PDPA mappings | Medium |
| Reference implementations | SDKs in Go, Rust, TypeScript | Medium |
| Documentation translations | French, German, Japanese | Low (community) |

## What We Do Not Accept

- Changes to JEP core verbs or field structure
- Legal compliance guarantees or liability language
- Vendor-specific lock-in (e.g., cloud-provider-only extensions)

## Submission Process

1. **Open an Issue** first describing the gap. Reference the EU AI Act article or national regulation.
2. **Fork and branch** from `main`. Name your branch `industry/xxx` or `fix/xxx`.
3. **Include four files** for any new industry:
   - `extensions/xxx.md` — human-readable specification
   - `schemas/xxx.schema.json` — machine-validatable schema
   - `examples/xxx_j.json` — working example event
   - `examples/xxx_d.json` or `xxx_t.json` — chain continuation example
4. **Run tests**: `python implementations/test_verify_jep_eu.py -v`
5. **Submit PR** with a clear description of the regulatory article mapped and the JEP primitive binding.

## Style Guide

- Use `https://jep-eu-compliance.org/industry/xxx` as the extension namespace
- Hash fields must use `sha256:` or `sm3:` prefix with hex payload
- All DIDs in examples must use `did:example:tmp:` prefix to indicate ephemeral
- Markdown files: keep EU AI Act article references in parentheses, e.g., `(Art. 14)`

## Governance

Yuqiang Wang maintains final merge authority. The project is intentionally small and slow-moving — this is a feature, not a bug.