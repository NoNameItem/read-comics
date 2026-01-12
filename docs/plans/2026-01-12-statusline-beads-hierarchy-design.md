# Statusline Beads Hierarchy Display

Display in_progress beads tasks in hierarchical format in Claude Code statusline.

## Output Format

### Multiple trees
```
Tasks:
├─ Phase 1: Auth (fqr) [in_progress]
│  └─ Password reset confirm page (fqr.2) [in_progress]
└─ User Profile (0d4) [open]
   └─ Profile settings (0d4.3) [in_progress]
```

### Single task without hierarchy
```
Task: Password reset confirm page (fqr.2) [in_progress]
```

## Node Format

```
{title} ({short_id}) [{status}]
```

- **short_id**: Strip project prefix (`read_comics-fqr.2` → `fqr.2`)
- **status**: `in_progress`, `open`, or `closed`

## Color Scheme

### Title colors by depth (leaf always green)
| Depth | Color | Example |
|-------|-------|---------|
| 0 (root) | magenta | `fqr` |
| 1 | cyan | `fqr.2` |
| 2 | yellow | `fqr.2.1` |
| 3+ | white | `fqr.2.1.1` |
| leaf | green | (deepest node in branch) |

### Status colors
| Status | Color |
|--------|-------|
| `[in_progress]` | green |
| `[open]` | cyan |
| `[blocked]` | red |
| `[closed]` | dim |

### Other elements
- ID `(fqr.2)`: dim
- Tree symbols `├─ └─ │`: dim

## Algorithm

1. Get `bd list --status=in_progress` — these are leaf tasks
2. For each task, climb hierarchy by ID:
   - `fqr.2.1` → check `fqr.2` → check `fqr`
   - If parent not in in_progress list, call `bd show <parent_id>` to get title and status
   - Cache results to avoid duplicate calls
3. Build trees from roots to leaves
4. Sort trees by root priority (P0 first)
5. Render with proper tree symbols and colors

## Edge Cases

- Parent not in_progress (status open) — show in tree with open status
- Parent closed — show with closed status (anomaly detection)
- Empty list — don't show `Tasks:` line at all
- Single root task, no children — use simplified format `Task: ...`

## Implementation

- Language: bash + jq (jq already used in statusline)
- Location: `~/.claude/statusline.sh`, replace existing beads section
- Cache `bd show` results in associative array within single script run
