"""
Generic Gantt Chart Generator
=============================

This script generates a professional-looking Gantt chart based on a YAML configuration file.
It is designed to be reusable across different projects by simply modifying the config file.

Usage
-----
1.  Create a `gantt_config.yaml` file in the same directory (or modify the default one).
2.  Run the script: `python3 generate-gantt_chart.py`

Configuration File Structure (YAML)
-----------------------------------
project:
  title: "Project Title"
  start_date: "YYYY-MM-DD"
  end_date: "YYYY-MM-DD"

output:
  filename: "output_image.png"
  dpi: 300

tasks:
  - name: "Task Name"
    duration_weeks: 2          # Number of weeks OR "start2end"
    start_date: "YYYY-MM-DD"   # Optional: Fixed start date

Task Logic
----------
- **Sequential:** If `start_date` is omitted, the task starts immediately after the previous task ends.
- **Fixed Start:** If `start_date` is provided, the task starts on that specific date.
- **Duration:** 
    - Can be a number (weeks).
    - Can be "start2end" to span the entire project duration.

Dependencies
------------
- matplotlib
- pandas
- PyYAML (install via `pip install pyyaml`)
"""

import os
import sys
import yaml
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# ----------------------------
# Defaults & Constants
# ----------------------------
CONFIG_FILE = "./gantt_config.yaml"
DEFAULT_BAR_HEIGHT = 0.8
FIG_SIZE = (15, 6)

# Colors
STYLE = {
    "bar_color": "#4A90E2",       # Professional Blue
    "bar_edge_color": "#357ABD",
    "text_color": "#2C3E50",
    "highlight_color": "#E74C3C", # Red (End)
    "success_color": "#27AE60",   # Green (Start)
    "today_color": "#9B59B6",     # Purple (Today)
    "grid_color": "#BDC3C7",
    "bg_color_alt": "#F7F9F9",    # Alternating month shade
    "border_color": "#2C3E50"
}

def load_config(config_path):
    """Loads and validates the YAML configuration."""
    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' not found.")
        print("Please create a YAML config file as described in the script documentation.")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            sys.exit(1)

def parse_date(date_str):
    """Helper to parse YYYY-MM-DD string to datetime."""
    return datetime.strptime(str(date_str), "%Y-%m-%d")

def calculate_schedule(config):
    """Calculates start and end dates for all tasks."""
    project_start = parse_date(config["project"]["start_date"])
    project_end = parse_date(config["project"]["end_date"])
    
    # Check total duration and warn if too long
    total_duration_days = (project_end - project_start).days
    if total_duration_days > 450: # Approx 15 months
        print(f"WARNING: Project duration is {total_duration_days} days (> 15 months).")
        print("The Gantt chart might look crowded or weird. Consider shortening the timeline.")
    
    tasks_data = []
    current_date = project_start
    
    for task in config["tasks"]:
        name = task["name"]
        duration_val = task["duration_weeks"]
        manual_start = task.get("start_date")
        
        # Determine Start Date
        if manual_start:
            start_date = parse_date(manual_start)
        else:
            start_date = current_date
            
        # Determine End Date
        if duration_val == "start2end":
            if manual_start:
                start_date = parse_date(manual_start)
                end_date = project_end
            else:
                start_date = project_start
                end_date = project_end
        else:
            # Standard duration in weeks
            try:
                weeks = float(duration_val)
                end_date = start_date + timedelta(weeks=weeks)
            except ValueError:
                 print(f"Error: Invalid duration '{duration_val}' for task '{name}'")
                 sys.exit(1)
        
        # Update current_date for the *next* task
        if duration_val != "start2end":
             current_date = end_date
             
        tasks_data.append({
            "Task": name,
            "Start": start_date,
            "End": end_date,
            "DurationDays": (end_date - start_date).days
        })
        
    return pd.DataFrame(tasks_data), project_start, project_end

def create_gantt_chart(df, project_start, project_end, config):
    """Generates the matplotlib chart."""
    
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Roboto', 'Arial', 'sans-serif']
    
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    
    # Border
    fig.patch.set_edgecolor(STYLE["border_color"])
    fig.patch.set_linewidth(2)
    
    # ----------------------------
    # Draw Bars
    # ----------------------------
    y_pos = range(len(df))
    
    bars = ax.barh(
        y_pos,
        df["DurationDays"],
        left=df["Start"],
        height=DEFAULT_BAR_HEIGHT,
        align='center',
        color=STYLE["bar_color"],
        alpha=0.9,
        edgecolor=STYLE["bar_edge_color"],
        linewidth=1,
        zorder=3
    )
    
    # ----------------------------
    # Annotations & Lines
    # ----------------------------
    plot_start_lim = datetime(project_start.year, project_start.month, 1)
    plot_end_lim = project_end + timedelta(weeks=3)
    
    ax.set_xlim(left=plot_start_lim, right=plot_end_lim)
    
    for i, bar in enumerate(bars):
        start = df.loc[i, "Start"]
        end = df.loc[i, "End"]
        
        # Grid connection line
        ax.hlines(y=i, xmin=plot_start_lim, xmax=start, 
                  color=STYLE["grid_color"], linestyle=':', linewidth=1, zorder=2)
        
        # Label text
        date_str = f"{start.strftime('%d %b')} - {end.strftime('%d %b')}"
        duration_days = (end - start).days
        
        if duration_days > 40:
            text_x = start + (end - start) / 2
            ha = 'center'
            color = 'white'
            fw = 'bold'
        else:
            text_x = end + timedelta(days=3)
            ha = 'left'
            color = STYLE["text_color"]
            fw = 'normal'
            
        ax.text(text_x, i, date_str, ha=ha, va='center', 
                color=color, fontsize=9, fontweight=fw, zorder=4)

    # ----------------------------
    # Axis & Grid
    # ----------------------------
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df["Task"], fontsize=11, color=STYLE["text_color"], fontweight='500')
    ax.invert_yaxis() 
    
    # X-Axis
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(plt.NullFormatter()) 
    
    month_range = pd.date_range(start=plot_start_lim, end=plot_end_lim, freq='MS')
    midpoints = []
    labels = []
    
    # Heuristic: If we have many months, use short names to avoid overlap
    use_short_names = len(month_range) > 10
    
    for i in range(len(month_range) - 1):
        m_start = month_range[i]
        m_end = month_range[i+1]
        
        bg_color = STYLE["bg_color_alt"] if i % 2 == 0 else "#FFFFFF"
        ax.axvspan(m_start, m_end, facecolor=bg_color, alpha=1.0, zorder=0)
        
        midpoints.append(m_start + (m_end - m_start) / 2)
        
        if use_short_names:
            # Short: "Jan '26"
            labels.append(m_start.strftime("%b '%y"))
        else:
            # Long: "January '26"
            labels.append(m_start.strftime("%B '%y"))
        
    ax.set_xticks(midpoints, minor=True)
    ax.set_xticklabels(labels, minor=True, fontsize=11, 
                       color=STYLE["text_color"], fontweight='bold')
    
    ax.tick_params(axis='x', which='minor', length=0)
    ax.tick_params(axis='x', which='major', length=5, color=STYLE["grid_color"])
    ax.tick_params(axis='y', length=0)
    
    ax.grid(axis='x', which='major', linestyle='-', alpha=0.5, 
            color=STYLE["grid_color"], zorder=1)
    ax.set_axisbelow(True)
    
    # Spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['left'].set_linewidth(2)
    ax.spines['left'].set_color(STYLE["text_color"])
    ax.spines['bottom'].set_color(STYLE["grid_color"])
    
    # ----------------------------
    # Project Markers
    # ----------------------------
    ax.axvline(project_start, color=STYLE["success_color"], linestyle='--', 
               linewidth=1.5, alpha=0.8, zorder=5)
    ax.axvline(project_end, color=STYLE["highlight_color"], linestyle='--', 
               linewidth=1.5, alpha=0.8, zorder=5)
    
    # Today's date marker
    # PRINT TODAY LINE ONLY IF THE TODAY DATE IS PROVIDED IN THE CONFIG
    if config["project"]["today_date"] != "":
        today = parse_date(config["project"]["today_date"])
        
        if plot_start_lim <= today <= plot_end_lim:
            ax.axvline(today, color=STYLE["today_color"], linestyle='-', 
                    linewidth=2, alpha=0.7, zorder=5)
            today_label = today.strftime("%d-%b'%y")
            ax.text(today, -0.06, f"Today: {today_label}", 
                    color=STYLE["today_color"], ha='center', va='top', 
                    transform=ax.get_xaxis_transform(), fontsize=9, fontweight='bold')
                
    # Bottom Date Labels (below X axis)
    ax.text(project_start, -0.06, project_start.strftime("%d-%b'%y"), 
            color=STYLE["success_color"], ha='center', va='top', 
            transform=ax.get_xaxis_transform(), fontsize=10, fontweight='bold')
    ax.text(project_end, -0.06, project_end.strftime("%d-%b'%y"), 
            color=STYLE["highlight_color"], ha='center', va='top', 
            transform=ax.get_xaxis_transform(), fontsize=10, fontweight='bold')
    
    # ----------------------------
    # Title & Save
    # ----------------------------
    ax.set_title(config["project"]["title"], fontsize=18, pad=25, 
                 color=STYLE["text_color"], fontweight='bold', loc='center')
    plt.tight_layout()
    
    output_path = config["output"]["filename"]
    
    plt.savefig(output_path, dpi=config["output"].get("dpi", 300), bbox_inches="tight")
    print(f"Chart saved successfully to: {output_path}")

def main():
    print(f"Reading configuration from {CONFIG_FILE}...")
    config = load_config(CONFIG_FILE)
    
    print("Calculating schedule...")
    df, p_start, p_end = calculate_schedule(config)
    
    print("Generating Gantt chart...")
    create_gantt_chart(df, p_start, p_end, config)

if __name__ == "__main__":
    main()
