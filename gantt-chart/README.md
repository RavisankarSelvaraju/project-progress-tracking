# Gantt Chart Generator

Python script to generate a styled Gantt chart from a YAML config.

## Requirements

- Python 3.8+
- `matplotlib`
- `pandas`
- `PyYAML`

Install dependencies:

```bash
pip install matplotlib pandas pyyaml
```

## Files

- Script: `generate-gantt_chart.py`
- Config: `gantt_config.yaml`

> Note: `CONFIG_FILE` is currently set to  
> `progress-tracking/gantt-chart/gantt_config.yaml`  
> so run from the `docs_thesis` root, or adjust `CONFIG_FILE` if needed.

## Configuration Example (`gantt_config.yaml`)

```yaml
project:
  title: "My Project Plan"
  start_date: "2026-01-01"
  end_date: "2026-06-30"
  today_date: "today"            # "today", "", or "YYYY-MM-DD"
  show_title: true
  show_elapsed_overlay: true     # red overlay: start -> today
  show_remaining_overlay: true   # green overlay: today -> end

output:
  filename: "gantt_output.png"
  dpi: 300

tasks:
  - name: "Requirement Analysis"
    duration_weeks: 3

  - name: "Prototype Development"
    duration_weeks: 6

  - name: "Integration"
    duration_weeks: 4
    start_date: "2026-03-10"     # fixed start override

  - name: "Project Window"
    duration_weeks: "start2end"  # spans project start to end

milestones:
  show_milestones: true
  items:
    - name: "Mid Review"
      date: "2026-03-20"
    - name: "Final Demo"
      date: "2026-06-25"
```

## Run

From `progress-tracking`:

```bash
python3 gantt-chart/generate-gantt_chart.py
```

## Task Scheduling Rules

- If `start_date` is omitted, task starts after the previous task ends.
- If `start_date` is set, that date is used directly.
- `duration_weeks` can be:
  - numeric (`2`, `3.5`, etc.), or
  - `"start2end"` to span full project duration.

## Output

The chart is saved to `output.filename` with the configured DPI.
