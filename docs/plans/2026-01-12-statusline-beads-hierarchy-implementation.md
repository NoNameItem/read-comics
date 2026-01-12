# Statusline Beads Hierarchy Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Display in_progress beads tasks in hierarchical tree format in statusline

**Architecture:** Replace existing flat beads display (lines 63-84 in statusline.sh) with hierarchical tree renderer. Use associative arrays for caching parent lookups, jq for parsing bd output.

**Tech Stack:** bash, jq, bd CLI

---

### Task 1: Add helper function to get task info

**Files:**
- Modify: `~/.claude/statusline.sh:61` (after git info section)

**Step 1: Add get_beads_task_info function**

Insert after line 61 (after git info `fi`):

```bash
# Helper: Get task info (title, status) by ID with caching
# Uses associative array BEADS_CACHE as cache
declare -A BEADS_CACHE
get_beads_task_info() {
    local task_id="$1"
    local cache_key="$task_id"

    # Return cached if available
    if [[ -n "${BEADS_CACHE[$cache_key]}" ]]; then
        echo "${BEADS_CACHE[$cache_key]}"
        return
    fi

    # Fetch from bd show
    local bd_output
    bd_output=$(cd "$project_dir" 2>/dev/null && bd show "$task_id" 2>/dev/null)
    if [[ -z "$bd_output" ]]; then
        return 1
    fi

    # Parse: first line is "id: title", Status line has status
    local title status
    title=$(echo "$bd_output" | head -1 | sed 's/^[^:]*: //')
    status=$(echo "$bd_output" | grep '^Status:' | awk '{print $2}')

    # Cache and return as "title|status"
    BEADS_CACHE[$cache_key]="${title}|${status}"
    echo "${title}|${status}"
}
```

**Step 2: Test manually**

```bash
# Source the function and test
source ~/.claude/statusline.sh <<< '{"workspace":{"project_dir":"/Users/artem.vasin/Coding/python/read_comics"}}'
```

Expected: No errors

**Step 3: Commit**

```bash
git -C ~/.claude add statusline.sh
git -C ~/.claude commit -m "feat(statusline): add beads task info helper with caching"
```

---

### Task 2: Add color helper function

**Files:**
- Modify: `~/.claude/statusline.sh` (after get_beads_task_info)

**Step 1: Add get_depth_color and get_status_color functions**

```bash
# Helper: Get color by depth (leaf is always green)
get_depth_color() {
    local depth="$1"
    local is_leaf="$2"

    if [[ "$is_leaf" == "true" ]]; then
        echo "$GREEN"
        return
    fi

    case "$depth" in
        0) echo "$MAGENTA" ;;
        1) echo "$CYAN" ;;
        2) echo "$YELLOW" ;;
        *) echo "$RESET" ;;  # white/default for 3+
    esac
}

# Helper: Get color by status
get_status_color() {
    local status="$1"
    case "$status" in
        in_progress) echo "$GREEN" ;;
        open) echo "$CYAN" ;;
        blocked) echo "$RED" ;;
        closed) echo "$DIM" ;;
        *) echo "$DIM" ;;
    esac
}

# Helper: Shorten task ID (remove project prefix)
shorten_id() {
    local full_id="$1"
    # read_comics-fqr.2 -> fqr.2
    echo "$full_id" | sed 's/^[^-]*-//'
}
```

**Step 2: Commit**

```bash
git -C ~/.claude add statusline.sh
git -C ~/.claude commit -m "feat(statusline): add color and ID helper functions"
```

---

### Task 3: Replace beads section with hierarchy builder

**Files:**
- Modify: `~/.claude/statusline.sh:63-84` (replace existing beads section)

**Step 1: Replace the beads section**

Replace lines 63-84 with:

```bash
# Beads task information - hierarchical tree display
beads_lines=""
if command -v bd &> /dev/null && [[ -d "$project_dir/.beads" ]]; then
    # Get in_progress items
    beads_output=$(cd "$project_dir" 2>/dev/null && bd list --status=in_progress 2>/dev/null)

    if [[ -n "$beads_output" ]]; then
        # Parse in_progress tasks into arrays
        declare -A task_titles task_statuses task_children
        declare -a root_ids all_ids

        while IFS= read -r line; do
            [[ -z "$line" ]] && continue
            # Parse: "read_comics-fqr.2 [P1] [task] in_progress - Password reset confirm page"
            local task_id title status
            task_id=$(echo "$line" | awk '{print $1}')
            status=$(echo "$line" | grep -oE '(in_progress|open|blocked|closed)')
            title=$(echo "$line" | sed 's/.*'"$status"' - //')

            task_titles["$task_id"]="$title"
            task_statuses["$task_id"]="$status"
            all_ids+=("$task_id")

            # Cache for later lookups
            BEADS_CACHE["$task_id"]="${title}|${status}"
        done <<< "$beads_output"

        # Build parent chain for each task, collect all nodes
        declare -A all_nodes  # all nodes we need to display
        for task_id in "${all_ids[@]}"; do
            current="$task_id"
            while [[ -n "$current" ]]; do
                all_nodes["$current"]=1
                # Get parent by removing last .N segment
                if [[ "$current" == *.* ]]; then
                    parent="${current%.*}"
                    # Fetch parent info if not cached
                    if [[ -z "${task_titles[$parent]}" ]]; then
                        local info
                        info=$(get_beads_task_info "$parent")
                        if [[ -n "$info" ]]; then
                            task_titles["$parent"]="${info%%|*}"
                            task_statuses["$parent"]="${info##*|}"
                        fi
                    fi
                    # Track parent-child relationship
                    task_children["$parent"]+="$current "
                    current="$parent"
                else
                    # This is a root
                    root_ids+=("$current")
                    break
                fi
            done
        done

        # Remove duplicate roots
        root_ids=($(printf '%s\n' "${root_ids[@]}" | sort -u))

        # Determine leaves (tasks with no children)
        declare -A is_leaf
        for node in "${!all_nodes[@]}"; do
            if [[ -z "${task_children[$node]}" ]]; then
                is_leaf["$node"]="true"
            fi
        done

        # Render function
        render_node() {
            local node_id="$1"
            local prefix="$2"
            local is_last="$3"
            local depth="$4"

            local title="${task_titles[$node_id]}"
            local status="${task_statuses[$node_id]}"
            local short_id=$(shorten_id "$node_id")
            local leaf="${is_leaf[$node_id]}"

            local title_color=$(get_depth_color "$depth" "$leaf")
            local status_color=$(get_status_color "$status")

            # Build connector
            local connector=""
            if [[ -n "$prefix" ]] || [[ "$depth" -gt 0 ]]; then
                if [[ "$is_last" == "true" ]]; then
                    connector="${DIM}└─${RESET} "
                else
                    connector="${DIM}├─${RESET} "
                fi
            fi

            # Build line
            local line="${prefix}${connector}${title_color}${title}${RESET} ${DIM}(${short_id})${RESET} ${status_color}[${status}]${RESET}"
            beads_lines+="${line}"$'\n'

            # Render children
            local children=(${task_children[$node_id]})
            local num_children=${#children[@]}
            local child_idx=0
            for child in "${children[@]}"; do
                child_idx=$((child_idx + 1))
                local child_is_last="false"
                [[ "$child_idx" -eq "$num_children" ]] && child_is_last="true"

                local child_prefix="$prefix"
                if [[ -n "$prefix" ]] || [[ "$depth" -gt 0 ]]; then
                    if [[ "$is_last" == "true" ]]; then
                        child_prefix="${prefix}   "
                    else
                        child_prefix="${prefix}${DIM}│${RESET}  "
                    fi
                fi

                render_node "$child" "$child_prefix" "$child_is_last" "$((depth + 1))"
            done
        }

        # Check for simplified format (single root, no children, is leaf)
        if [[ ${#root_ids[@]} -eq 1 && "${is_leaf[${root_ids[0]}]}" == "true" ]]; then
            local root="${root_ids[0]}"
            local title="${task_titles[$root]}"
            local status="${task_statuses[$root]}"
            local short_id=$(shorten_id "$root")
            local status_color=$(get_status_color "$status")
            beads_lines="${DIM}Task:${RESET} ${GREEN}${title}${RESET} ${DIM}(${short_id})${RESET} ${status_color}[${status}]${RESET}"
        else
            # Full tree format
            beads_lines="${DIM}Tasks:${RESET}"$'\n'
            local num_roots=${#root_ids[@]}
            local root_idx=0
            for root in "${root_ids[@]}"; do
                root_idx=$((root_idx + 1))
                local root_is_last="false"
                [[ "$root_idx" -eq "$num_roots" ]] && root_is_last="true"
                render_node "$root" "" "$root_is_last" 0
            done
        fi

        # Remove trailing newline
        beads_lines="${beads_lines%$'\n'}"
    fi
fi
```

**Step 2: Test manually**

```bash
echo '{"workspace":{"current_dir":"/Users/artem.vasin/Coding/python/read_comics","project_dir":"/Users/artem.vasin/Coding/python/read_comics"},"model":{"display_name":"Opus 4.5"}}' | ~/.claude/statusline.sh
```

Expected output should include hierarchical tree like:
```
Tasks:
└─ Phase 1: Auth (fqr) [in_progress]
   └─ Password reset confirm page (fqr.2) [in_progress]
```

**Step 3: Commit**

```bash
git -C ~/.claude add statusline.sh
git -C ~/.claude commit -m "feat(statusline): hierarchical beads task tree display"
```

---

### Task 4: Update output section

**Files:**
- Modify: `~/.claude/statusline.sh:604` (output section)

**Step 1: Replace single beads_line output with multi-line**

Change line 604 from:
```bash
[[ -n "$beads_line" ]] && echo -e "$beads_line"
```

To:
```bash
if [[ -n "$beads_lines" ]]; then
    while IFS= read -r beads_line; do
        echo -e "$beads_line"
    done <<< "$beads_lines"
fi
```

**Step 2: Test full output**

```bash
echo '{"workspace":{"current_dir":"/Users/artem.vasin/Coding/python/read_comics","project_dir":"/Users/artem.vasin/Coding/python/read_comics"},"model":{"display_name":"Opus 4.5"}}' | ~/.claude/statusline.sh
```

Expected: Full statusline with hierarchical tasks

**Step 3: Commit**

```bash
git -C ~/.claude add statusline.sh
git -C ~/.claude commit -m "feat(statusline): multi-line beads output support"
```

---

### Task 5: Test edge cases

**Step 1: Test with no in_progress tasks**

```bash
# Temporarily close all tasks or test in a project without .beads
# Should not show Tasks: line at all
```

**Step 2: Test with deep hierarchy**

```bash
# If available, test with 3+ levels of nesting
# Colors should be: magenta -> cyan -> yellow -> green (leaf)
```

**Step 3: Final commit if any fixes needed**

```bash
git -C ~/.claude add statusline.sh
git -C ~/.claude commit -m "fix(statusline): edge case handling for beads tree"
```

---

## Summary

| Task | Description |
|------|-------------|
| 1 | Add get_beads_task_info helper with caching |
| 2 | Add color and ID helper functions |
| 3 | Replace beads section with hierarchy builder |
| 4 | Update output section for multi-line |
| 5 | Test edge cases |
