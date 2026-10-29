# MCP for Google Ads 🚀
**The World-Class Media Buyer, Funnel Strategy & Unit Economics Engine for Google Ads**

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Protocol](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green)](https://modelcontextprotocol.io/)

**MCP for Google Ads** is an autonomous Model Context Protocol (MCP) server engineered by **Edd Vásquez** for AI coding assistants (Claude Desktop, OpenAI Codex, Antigravity) to act as senior media buyers, acquisition strategists, and unit economics auditors.

Unlike minimal query wrappers, this engine provides a complete **37-tool operating system** combining deterministic mutations under Two-Phase Commit safety, auction quality scoring, orphaned negative governance, algorithmic bidding maturity audits, and closed-loop CRM qualification tracking.

---

## 🛠️ Complete 37-Tool Catalog

### 1. Account Discovery & Direct GAQL (3 Tools)
- `customers_list_accessible_customers`: Retrieve accessible Google Ads customer IDs.
- `search_search`: Structured Google Ads Query Language (GAQL) query execution.
- `metadata_get_resource_metadata`: Discover selectable fields, metrics, and segments for resources.

### 2. Transactional Mutation Engine — Two-Phase Commit (12 Tools)
- `editing_prepare_campaign`: Budget, status, bidding strategy changes.
- `editing_prepare_ad_group`: Ad group creation, status, and target CPA overrides.
- `editing_prepare_ad`: Responsive Search Ad (RSA) creation with multi-headline/description validation.
- `editing_prepare_keywords`: Positive keywords, manual bids, match types, and campaign negatives.
- `editing_prepare_budget`: Daily campaign budget updates and delivery methods.
- `editing_prepare_negative_list`: Shared negative keyword list creation, renaming, adding terms, removing terms, and campaign attachment.
- `editing_list_negative_lists`: Query existing shared negative sets in the account.
- `editing_get_negative_list`: Detailed term-by-term and campaign link inspection.
- `editing_apply_proposal`: Immutable commit execution (`confirmed=True`).
- `editing_get_proposal`: Pre-execution diff inspection (`validate_only=True`).
- `editing_cancel_proposal`: Abort and discard draft proposal.
- `editing_reconcile_proposal`: Sync and reconcile executed changes.

### 3. Media Buying Intelligence, Unit Economics & Funnel Strategy (22 Tools)
- `intelligence_audit_search_terms`: Mine bleeding search terms and quantify wasted spend.
- `intelligence_prepare_mined_negatives`: Convert wasted search queries directly into negative keyword proposals.
- `intelligence_analyze_impression_share`: Lost IS to Budget vs. Lost IS to Rank breakdown.
- `intelligence_audit_devices_and_geos`: Device bid modifier efficiency (Mobile vs. Desktop) and geo-targeting friction.
- `intelligence_audit_budget_pacing`: Month-to-date run rate and end-of-month budget projection.
- `intelligence_check_account_health`: Disapproved ads, billing issues, and account delivery status.
- `intelligence_audit_campaign_assets`: Sitelinks, callouts, structured snippets, and price extension coverage.
- `intelligence_audit_creative_fatigue`: CTR degradation detection over 14-day rolling windows.
- `intelligence_audit_conversion_health`: Zero-conversion campaigns and tracking health.
- `intelligence_audit_copy_persuasion`: Heuristic audit of RSA headlines against Pain, Unique Mechanism, Offer, and Repellent.
- `intelligence_classify_intent_funnel`: Informational vs. Commercial vs. Transactional intent classification.
- `intelligence_prepare_high_ticket_negative_shield`: 8-category universal repellent shield (free-seekers, jobs, students, DIY).
- `intelligence_audit_quality_score_triad`: Keyword-level Quality Score (1-10), Expected CTR, Ad Relevance, and Landing Page Experience.
- `intelligence_audit_lead_dropoff`: Ad Clicks -> Landing Page Visits -> Qualified Contacts (WhatsApp/Calls) conversion tracking.
- `intelligence_calculate_high_ticket_unit_economics`: P&L viability: Ticket Size, Gross Margin, and Closing Rate to determine Max Allowable CPA.
- `intelligence_audit_shared_negative_governance`: Identify orphaned negative lists (`reference_count == 0`) and unprotected active campaigns.
- `intelligence_inspect_negative_list_terms`: Fast search and filter within large negative keyword lists (2,000+ terms).
- `intelligence_audit_bidding_strategy_readiness`: Evaluate monthly conversion volume (30+ threshold) to prevent premature Smart Bidding swings.
- `intelligence_audit_lead_to_sale_discrepancy`: Detect *Algorithmic Poisoning* when Google conversions fail to convert to qualified CRM sales calls (<20% rate).
- `intelligence_audit_landing_page_message_match`: Scrapes and compares destination H1/H2/CTA against active RSA headlines to detect post-click friction.
- `intelligence_upload_offline_conversion_call`: Upload offline qualified calls/sales with GCLID and real revenue to cure Algorithmic Poisoning.
- `intelligence_simulate_budget_scaling_elasticity`: Models Lost IS (Budget vs. Rank) and CPC elasticity before scaling spend.

---

## 🔒 Legal Notice & Trademark Disclaimer

* **Author:** Edd Vásquez. All rights reserved.
* **Disclaimer:** *MCP for Google Ads* is an independent open-source project. It is **not** affiliated with, endorsed by, or sponsored by Google LLC. *Google Ads* is a registered trademark of Google LLC.
* **License:** Apache License 2.0. See [LICENSE](LICENSE) for details.
