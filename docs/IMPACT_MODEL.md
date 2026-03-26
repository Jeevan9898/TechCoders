# AutonomIQ — Business Impact Model

Team: TechCoders  
Version: 2.0 · ET Gen AI Hackathon 2026

---

## Context & Assumptions

This model estimates the impact of deploying AutonomIQ at a mid-to-large enterprise that actively responds to RFPs — a typical profile in IT services, consulting, or government contracting.

Baseline assumptions:

| Parameter | Value | Rationale |
|---|---|---|
| RFPs received per month | 40 | Typical mid-size IT services firm |
| Average RFP response time (manual) | 12 hours | Industry benchmark; includes reading, matching, pricing, writing |
| Fully-loaded cost of a bid team member | $60/hour | Senior analyst + overhead in India/hybrid team |
| Average team size per RFP response | 3 people | Analyst, pricing lead, technical reviewer |
| Win rate (manual process) | 28% | Industry average for competitive RFP responses |
| Average contract value per won RFP | $350,000 | Mid-market IT services deal |
| RFPs missed or submitted late per month | 4 | Due to bandwidth constraints |
| Error/rework rate in manual pricing | 22% | Internal re-submissions due to pricing errors |

---

## 1. Time Saved

Manual effort per RFP:
```
12 hours × 3 people = 36 person-hours per RFP
```

AutonomIQ effort per RFP:
```
Autonomous steps handle ~94% of the work
Human review needed only for ~6% of steps ≈ ~2 person-hours per RFP
```

Time saved per RFP:
```
36 − 2 = 34 person-hours saved
```

Monthly time saved (40 RFPs):
```
34 × 40 = 1,360 person-hours/month
≈ 170 person-days/month
```

Annualised:
```
1,360 × 12 = 16,320 person-hours/year saved
≈ 8 full-time analyst equivalents freed up per year
```

---

## 2. Cost Reduced

Monthly cost of manual RFP process:
```
36 person-hours × $60/hour × 40 RFPs = $86,400/month
```

Monthly cost with AutonomIQ:
```
2 person-hours × $60/hour × 40 RFPs = $4,800/month
```

Monthly savings:
```
$86,400 − $4,800 = $81,600/month
```

Annual cost reduction:
```
$81,600 × 12 = ~$979,200/year ≈ $1M/year
```

---

## 3. Revenue Recovered

RFPs missed per month due to bandwidth: 4  
Win rate: 28%  
Expected wins recovered per month: `4 × 0.28 = 1.12`  
Average contract value: $350,000

Monthly revenue recovered:
```
1.12 × $350,000 = $392,000/month
```

Annual revenue recovered:
```
$392,000 × 12 = ~$4.7M/year
```

Additionally, faster turnaround improves proposal quality and win rate. A conservative 3% improvement (28% → 31%) on 40 RFPs/month:

```
Extra wins/month: 40 × 0.03 = 1.2
Extra revenue/month: 1.2 × $350,000 = $420,000
Annual uplift: ~$5M/year
```

---

## 4. Error & Rework Reduction

Manual pricing error rate: 22% of RFPs require rework  
Rework cost per RFP: ~8 person-hours × $60 = $480  
Monthly rework cost: `0.22 × 40 × $480 = $4,224/month`

AutonomIQ's pricing agent uses a structured model with market data validation — estimated error rate drops to ~3%.

Monthly rework cost with AutonomIQ: `0.03 × 40 × $480 = $576/month`  
Monthly savings: `$4,224 − $576 = $3,648/month`  
Annual: ~$44,000/year

---

## Summary

| Impact Area | Annual Value |
|---|---|
| Labour cost reduction | ~$979,000 |
| Revenue from recovered missed RFPs | ~$4,700,000 |
| Win rate improvement (conservative 3%) | ~$5,000,000 |
| Rework / error reduction | ~$44,000 |
| Total estimated annual impact | ~$10.7M |

---

## Sensitivity Check

The model is most sensitive to two variables:

1. Win rate improvement — even a 1% lift on 40 RFPs/month at $350K average = $1.68M/year. The assumption of 3% is conservative given faster, higher-quality responses.

2. Missed RFPs recovered — if only 2 of 4 missed RFPs are recovered, the revenue figure halves to ~$2.35M. Total impact still exceeds $7M/year.

Labour savings alone (~$1M/year) are enough to justify deployment costs for most enterprises. The revenue upside is the real multiplier.

---

## Caveats

- Figures are estimates based on industry benchmarks, not audited financials
- Actual impact depends on RFP volume, deal size, and existing team efficiency
- Integration costs (portal connectors, catalog API, market data feed) are not modelled here
- Human review overhead may be higher in regulated industries (government, defence)
