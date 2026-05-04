> **Exploratory / Not Legal Advice**
>
> This document contains exploratory mapping notes only. It is not legal advice, not a compliance guarantee, and not part of JEP-Core.
>
> JEP can provide technical event records that may support auditability or traceability workflows. It does not itself determine EU AI Act compliance.

# EU AI Act ↔ JEP Primitive Mapping

## Regulation (EU) 2024/1689 — Article Level Mapping

| EU AI Act Article | Requirement | JEP Verb | JEP Extension | Notes |
|-------------------|-------------|----------|---------------|-------|
| Art. 9 | Risk management system | J (chain root) | `risk_level`, `risk_assessment_hash` | Continuous lifecycle |
| Art. 10 | Data governance | V | `data_provenance_hash` | Training/validation/test data |
| Art. 11 | Technical documentation | J + V | `doc_reference`, `annex_iv_hash` | Pre-market, 10-year retention |
| Art. 12 | Automatic logging | J/D/T/V | — | Core protocol already satisfies |
| Art. 13 | Transparency to deployers | J | `deployer_instructions_hash` | Instructions for use |
| Art. 14 | Human oversight | D / T | `human_override`, `supervisor_did` | Effective intervention |
| Art. 15 | Accuracy, robustness, cybersecurity | V | `performance_benchmark_hash` | Documented levels |
| Art. 16 | CE marking | J (root) | `ce_marking_reference` | Pre-market |
| Art. 26 | Deployer obligations | D / T / V | `monitoring_interval`, `incident_flag` | Oversight + reporting |
| Art. 27 | FRIA (public sector) | J (root) | `fria_reference` | Fundamental Rights Impact Assessment |
| Art. 50 | Transparency to users | V | `disclosure_flag`, `synthetic_content_label` | Chatbots, deepfakes, emotion recognition |
| Art. 52 | GPAI systemic risk | J + V | `gpai_model_id`, `red_team_exercise_hash` | If applicable |

## Annex III Sector Mapping

| Annex III Section | Sector | JEP Industry Extension |
|-------------------|--------|------------------------|
| Annex III (1)(a) | Biometrics + medical diagnosis | `medical` |
| Annex III (2) | Critical infrastructure | `critical-infra` |
| Annex III (3) | Education & vocational training | *(future release)* |
| Annex III (4)(a) | Employment & recruitment | `hr` |
| Annex III (5)(b) | Credit scoring / essential services | `fintech` |
| Annex III (6) | Law enforcement | *(future release)* |
| Annex III (7) | Migration & border control | *(future release)* |
| Annex III (8) | Administration of justice | *(future release)* |

## Annex I Product Safety Mapping (Effective 2027-08-02)

| Product Category | EU Harmonisation Legislation | JEP Extension |
|------------------|------------------------------|---------------|
| Medical devices | MDR/IVDR | `medical` (enhanced) |
| Machinery | Machinery Regulation | *(future release)* |
| Vehicles | Type-approval frameworks | `automotive` (enhanced) |
| Toys | Toy Safety Directive | *(future release)* |

## Log Retention Requirements

| System Type | Minimum Retention | JEP Extension |
|-------------|-------------------|---------------|
| High-risk (Annex III) | 6 months (Art. 26) | `retention_policy: 6m` |
| High-risk in regulated products (Annex I) | Per sector legislation | `retention_policy: per_sector` |
| Public sector (pre-2026 systems) | Until 2030-08-02 (Art. 111) | `retention_policy: legacy_public` |
| Transparency-only (Art. 50) | Not specified | `retention_policy: deployer_defined` |