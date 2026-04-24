# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-24

### Added

- Initial release with six EU AI Act high-risk industry mappings:
  - `medical` — Annex III (1)(a) + Annex I (MDR/IVDR)
  - `fintech` — Annex III (5)(b) credit scoring
  - `automotive` — Annex III (2) traffic safety
  - `hr` — Annex III (4)(a) recruitment
  - `governance` — Article 50 transparency + deepfakes
  - `critical-infra` — Annex III (2) energy, water, transport
- JSON Schema definitions for all six industries
- Reference Python verifier (`verify_jep_eu.py`) with zero dependencies
- Unit tests covering valid/invalid core and extension cases
- Working JSON examples for all six industries
- Bilingual README (EN/ZH)
- MIT License

### Notes

- JEP Core verbs (J/D/T/V) remain unchanged across all industries
- All extensions are optional and non-intrusive
- Technical audit infrastructure only; no legal compliance guarantees