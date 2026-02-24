#!/usr/bin/env python3
"""
M&V Plan Builder — Interactive CLI

Replicates the OEH M&V Planning Tool spreadsheet as an interactive
command-line tool that generates a structured M&V plan document.

Sections:
1. ECM Project Background (site info, ECM description, stakeholders)
2. M&V Requirements (team, budget, timeline)
3. M&V Design (approach, boundary, baseline/reporting periods)
4. M&V Budget (resource hours and costs)
5. M&V Task List (structured task breakdown)
6. M&V Results Template (savings reporting format)

Usage:
    python mv_plan_builder.py                    # Interactive mode
    python mv_plan_builder.py --template         # Print blank template
    python mv_plan_builder.py --greenfield       # Pre-fill with Greenfield Municipal Center data
"""
import argparse
import json
import os
from datetime import datetime


def prompt(label, default=None):
    """Prompt user for input with optional default."""
    suffix = f" [{default}]" if default else ""
    val = input(f"  {label}{suffix}: ").strip()
    return val if val else default


def prompt_number(label, default=None):
    """Prompt for a numeric input."""
    while True:
        val = prompt(label, default)
        if val is None:
            return None
        try:
            return float(val)
        except ValueError:
            print("    Please enter a number.")


def section_header(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def collect_project_background(defaults=None):
    d = defaults or {}
    section_header("1. ECM PROJECT BACKGROUND")
    return {
        'site_name': prompt("Site name", d.get('site_name')),
        'site_address': prompt("Site address", d.get('site_address')),
        'site_overview': prompt("Site overview (type, area, use)", d.get('site_overview')),
        'ecm_description': prompt("ECM description", d.get('ecm_description')),
        'estimated_energy_savings': prompt("Estimated annual energy savings", d.get('estimated_energy_savings')),
        'estimated_cost_savings': prompt("Estimated annual cost savings ($)", d.get('estimated_cost_savings')),
        'implementation_cost': prompt("Implementation cost ($)", d.get('implementation_cost')),
        'implementation_date': prompt("Implementation date", d.get('implementation_date')),
        'contract_type': prompt("Contract type (ESPC, utility, internal)", d.get('contract_type')),
    }


def collect_team(defaults=None):
    d = defaults or {}
    section_header("2. M&V TEAM & REQUIREMENTS")
    team = []
    default_team = d.get('team', [])
    print("  Enter team members (blank name to stop):")
    i = 0
    while True:
        dt = default_team[i] if i < len(default_team) else {}
        name = prompt(f"  Team member {i+1} name", dt.get('name'))
        if not name:
            break
        role = prompt(f"    Role", dt.get('role'))
        rate = prompt_number(f"    Hourly rate ($)", dt.get('rate'))
        team.append({'name': name, 'role': role, 'rate': rate})
        i += 1

    budget = prompt_number("Preliminary M&V budget ($)", d.get('budget'))
    return {'team': team, 'budget': budget}


def collect_design(defaults=None):
    d = defaults or {}
    section_header("3. M&V DESIGN")
    return {
        'approach': prompt("M&V approach (e.g., whole facility regression, retrofit isolation)", d.get('approach')),
        'desired_accuracy': prompt("Desired accuracy (%)", d.get('desired_accuracy')),
        'measurement_boundary': prompt("Measurement boundary description", d.get('measurement_boundary')),
        'baseline_period': prompt("Baseline period (e.g., Jan 2024 – Dec 2024)", d.get('baseline_period')),
        'reporting_period': prompt("Reporting period (e.g., Jan 2025 – Dec 2025)", d.get('reporting_period')),
        'independent_variables': prompt("Independent variables (e.g., OAT, occupancy)", d.get('independent_variables')),
        'data_sources': prompt("Data sources (e.g., utility bills, BAS, sub-meters)", d.get('data_sources')),
        'model_type': prompt("Model type (e.g., 5P change-point, 3PH, TOWT)", d.get('model_type')),
        'validation_criteria': prompt("Validation criteria", d.get('validation_criteria', "ASHRAE G14: NMBE +/-5%, CV(RMSE) <=15%")),
        'nra_protocol': prompt("Non-routine adjustment protocol", d.get('nra_protocol')),
    }


def collect_tasks(defaults=None):
    d = defaults or {}
    section_header("5. M&V TASK LIST")
    default_tasks = d.get('tasks', [
        {'task': 'Project management & coordination', 'hours': 20},
        {'task': 'Baseline data collection & review', 'hours': 16},
        {'task': 'Baseline model development', 'hours': 24},
        {'task': 'Baseline model validation', 'hours': 8},
        {'task': 'Post-retrofit data collection', 'hours': 12},
        {'task': 'Savings calculation & NRA review', 'hours': 16},
        {'task': 'Uncertainty analysis', 'hours': 8},
        {'task': 'Draft M&V report', 'hours': 24},
        {'task': 'Report review & finalization', 'hours': 12},
        {'task': 'Stakeholder presentation', 'hours': 8},
    ])
    print("  Default task list (press Enter to accept, or type new value):")
    tasks = []
    for dt in default_tasks:
        task_name = prompt(f"  Task", dt['task'])
        if task_name:
            hours = prompt_number(f"    Hours", dt['hours'])
            tasks.append({'task': task_name, 'hours': hours or 0})
    return {'tasks': tasks}


def generate_report(bg, team_info, design, task_info):
    """Generate formatted M&V plan report."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  M&V PLAN — {bg['site_name']}")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 70)

    lines.append("\n1. ECM PROJECT BACKGROUND")
    lines.append("-" * 40)
    for k, v in bg.items():
        label = k.replace('_', ' ').title()
        lines.append(f"  {label:<30} {v or 'TBD'}")

    lines.append("\n2. M&V TEAM")
    lines.append("-" * 40)
    if team_info['team']:
        lines.append(f"  {'Name':<25} {'Role':<25} {'Rate':<10}")
        lines.append("  " + "-" * 60)
        for m in team_info['team']:
            lines.append(f"  {m['name']:<25} {m['role']:<25} ${m['rate'] or 0:,.0f}/hr")
    lines.append(f"\n  Preliminary Budget: ${team_info['budget'] or 0:,.0f}")

    lines.append("\n3. M&V DESIGN")
    lines.append("-" * 40)
    for k, v in design.items():
        label = k.replace('_', ' ').title()
        lines.append(f"  {label:<30} {v or 'TBD'}")

    lines.append("\n4. M&V BUDGET")
    lines.append("-" * 40)
    total_hours = sum(t['hours'] for t in task_info['tasks'])
    avg_rate = sum(m['rate'] or 0 for m in team_info['team']) / max(len(team_info['team']), 1)
    lines.append(f"  Total estimated hours: {total_hours:.0f}")
    lines.append(f"  Average blended rate:  ${avg_rate:,.0f}/hr")
    lines.append(f"  Estimated labor cost:  ${total_hours * avg_rate:,.0f}")

    lines.append("\n5. M&V TASK LIST")
    lines.append("-" * 40)
    lines.append(f"  {'#':<4} {'Task':<45} {'Hours':<8}")
    lines.append("  " + "-" * 57)
    for i, t in enumerate(task_info['tasks'], 1):
        lines.append(f"  {i:<4} {t['task']:<45} {t['hours']:<8.0f}")
    lines.append(f"  {'':4} {'TOTAL':<45} {total_hours:<8.0f}")

    lines.append("\n6. M&V RESULTS TEMPLATE")
    lines.append("-" * 40)
    lines.append(f"  {'Metric':<35} {'Baseline':<12} {'Post':<12} {'Savings':<12} {'%':<8}")
    lines.append("  " + "-" * 67)
    for metric in ['Total Energy (kWh)', 'Total Energy (therms)', 'Peak Demand (kW)', 'Annual Cost ($)', 'GHG (tCO2e)']:
        lines.append(f"  {metric:<35} {'___':<12} {'___':<12} {'___':<12} {'___':<8}")
    lines.append(f"\n  Precision: ___% at ___% confidence")

    return '\n'.join(lines)


def greenfield_defaults():
    """Pre-filled data for the Greenfield Municipal Center capstone."""
    return {
        'background': {
            'site_name': 'Greenfield Municipal Center',
            'site_address': 'Greenfield, Mid-Atlantic (CZ 4A)',
            'site_overview': '62,000 sq ft government facility, 4 wings (Office, Library, Data Center, Common)',
            'ecm_description': '4 ECMs: LED lighting + controls, chiller/DX replacement, roof insulation R-15 to R-30, VFDs on AHU fans',
            'estimated_energy_savings': '~10.5% electricity, gas increase 6.2% (interactive effects)',
            'estimated_cost_savings': 'TBD — depends on utility rate structure',
            'implementation_cost': 'ESPC financed',
            'implementation_date': 'Reporting year starts Jan of post-retrofit year',
            'contract_type': 'ESPC (15-year, savings shortfall risk on ESCO)',
        },
        'team': {
            'team': [
                {'name': 'M&V Lead', 'role': 'Lead analyst', 'rate': 120},
                {'name': 'Project Manager', 'role': 'ESCO coordination', 'rate': 100},
                {'name': 'Data Analyst', 'role': 'Data collection & QC', 'rate': 80},
            ],
            'budget': 25000,
        },
        'design': {
            'approach': 'Whole facility statistical regression (electric) + 3P heating (gas)',
            'desired_accuracy': '15% at 90% confidence',
            'measurement_boundary': 'Whole building — single electric and gas meter',
            'baseline_period': '12 months (Jan–Dec baseline year)',
            'reporting_period': '12 months (Jan–Dec reporting year)',
            'independent_variables': 'Monthly average outdoor air temperature (OAT)',
            'data_sources': 'Monthly utility bills, TMY weather data, EnergyPlus simulation output',
            'model_type': '5P change-point (electric), 3PH (gas)',
            'validation_criteria': 'ASHRAE G14: NMBE +/-5%, CV(RMSE) <=15%, R^2 >=0.75 (monthly)',
            'nra_protocol': 'Data center expansion in month 8 — requires NRA adjustment to isolate ECM savings',
        },
        'tasks': {
            'tasks': [
                {'task': 'Review building documentation & ESPC contract', 'hours': 8},
                {'task': 'Stakeholder interviews & risk mapping', 'hours': 8},
                {'task': 'Boundary selection & approach justification', 'hours': 12},
                {'task': 'Baseline data collection & QC', 'hours': 16},
                {'task': 'Baseline model fitting (5P electric, 3PH gas)', 'hours': 24},
                {'task': 'Model validation (ASHRAE G14)', 'hours': 8},
                {'task': 'Reporting period data collection & review', 'hours': 12},
                {'task': 'NRA identification & adjustment protocol', 'hours': 16},
                {'task': 'Savings calculation with uncertainty', 'hours': 12},
                {'task': 'Draft M&V report', 'hours': 24},
                {'task': 'Stakeholder presentation & plan defense', 'hours': 12},
            ],
        },
    }


def main():
    parser = argparse.ArgumentParser(description='M&V Plan Builder')
    parser.add_argument('--template', action='store_true', help='Print blank template')
    parser.add_argument('--greenfield', action='store_true', help='Pre-fill with Greenfield Municipal Center data')
    parser.add_argument('--output', type=str, help='Save plan to file')
    parser.add_argument('--json', type=str, help='Save plan data as JSON')
    args = parser.parse_args()

    if args.greenfield:
        defaults = greenfield_defaults()
        print("\n  Pre-filling with Greenfield Municipal Center data.")
        print("  Press Enter to accept defaults, or type to override.\n")
        bg = collect_project_background(defaults['background'])
        team_info = collect_team(defaults['team'])
        design = collect_design(defaults['design'])
        task_info = collect_tasks(defaults['tasks'])
    elif args.template:
        bg = {k: 'TBD' for k in ['site_name', 'site_address', 'site_overview', 'ecm_description',
              'estimated_energy_savings', 'estimated_cost_savings', 'implementation_cost',
              'implementation_date', 'contract_type']}
        bg['site_name'] = 'Template'
        team_info = {'team': [], 'budget': 0}
        design = {k: 'TBD' for k in ['approach', 'desired_accuracy', 'measurement_boundary',
                  'baseline_period', 'reporting_period', 'independent_variables',
                  'data_sources', 'model_type', 'validation_criteria', 'nra_protocol']}
        task_info = {'tasks': [
            {'task': 'Project management', 'hours': 0},
            {'task': 'Baseline data collection', 'hours': 0},
            {'task': 'Model development', 'hours': 0},
            {'task': 'Savings calculation', 'hours': 0},
            {'task': 'Reporting', 'hours': 0},
        ]}
    else:
        bg = collect_project_background()
        team_info = collect_team()
        design = collect_design()
        task_info = collect_tasks()

    report = generate_report(bg, team_info, design, task_info)
    print("\n" + report)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\n  Plan saved to {args.output}")

    if args.json:
        plan_data = {'background': bg, 'team': team_info, 'design': design, 'tasks': task_info}
        with open(args.json, 'w') as f:
            json.dump(plan_data, f, indent=2)
        print(f"  Plan data saved to {args.json}")


if __name__ == '__main__':
    main()
