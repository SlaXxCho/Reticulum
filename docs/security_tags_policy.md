# Security Tags and Policy Engine

## Tags
| Tag | Objective | PQC required | Downgrade allowed | Action if unmet |
|---|---|---|---|---|
| STANDARD | normal delivery | no | policy-dependent | allow best available |
| PREFERRED_SECURE | try stronger profile | preferred | controlled | fallback/block by policy |
| MUST_DELIVER | prioritize delivery | no (unless node minimum requires) | controlled | allow if minimum met |
| MAX_SECURITY | strict strongest path | yes in practice | no | block if requirement unmet |

## Policy inputs
- `security_tag`
- current link profile
- node minimum profile
- remote capabilities
- medium/network conditions
- downgrade allowance

## Policy outputs
- `allow_send`
- `block`
- `require_pqc_upgrade`
- selected/target profile
- `reason`

## Pseudocode
```text
required = map_tag_to_required_profile(tag)
best = choose_best_common(remote_caps, medium)
if no best: block
if best < required:
  block for MAX_SECURITY
  allow controlled fallback for lower tags (policy dependent)
else:
  allow; if current < required then require upgrade
```
