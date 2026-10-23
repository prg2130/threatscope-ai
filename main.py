#!/usr/bin/env python3
"""
ThreatScope AI - Main entry point
Provides CLI interface for running different components
"""

import sys
import argparse
from agent import ThreatScopeAgent
from database import get_statistics
from datetime import datetime

def cmd_run_full(args):
    """Run full analysis pipeline."""
    print("\n🔍 ThreatScope AI - Full Pipeline")
    print("="*60)

    agent = ThreatScopeAgent()
    agent.run_full_pipeline(
        reddit=not args.no_reddit,
        rss=not args.no_rss,
        sample_size=args.sample_size
    )

    print("\n" + "="*60)
    print("Pipeline complete!")
    print(f"Dashboard: streamlit run dashboard.py")
    print(f"Report: cat threat_report.md")

def cmd_collect(args):
    """Collect data only."""
    print("\n📊 ThreatScope AI - Data Collection")
    print("="*60)

    agent = ThreatScopeAgent()
    agent.initialize()
    agent.collect_data(
        reddit=not args.no_reddit,
        rss=not args.no_rss
    )

    print("\n✓ Data collection complete")
    print(f"Posts collected: {agent.posts_collected}")

def cmd_analyze(args):
    """Analyze collected data."""
    print("\n🔎 ThreatScope AI - Threat Analysis")
    print("="*60)

    agent = ThreatScopeAgent()
    agent.analyze_threats(sample_size=args.sample_size)

    print("\n✓ Analysis complete")
    print(f"Posts classified: {agent.posts_classified}")
    print(f"High-severity threats: {len(agent.high_severity_threats)}")

def cmd_report(args):
    """Generate report only."""
    print("\n📋 ThreatScope AI - Report Generation")
    print("="*60)

    agent = ThreatScopeAgent()
    agent.generate_intelligence_brief(output_file=args.output)

    print(f"\n✓ Report generated: {args.output}")

def cmd_dashboard(args):
    """Launch dashboard."""
    print("\n📈 ThreatScope AI - Dashboard")
    print("="*60)
    print("Starting Streamlit dashboard...")
    print("Open: http://localhost:8501")
    print("Press Ctrl+C to stop\n")

    import subprocess
    subprocess.run(["streamlit", "run", "dashboard.py"])

def cmd_stats(args):
    """Show statistics."""
    print("\n📊 ThreatScope AI - Statistics")
    print("="*60)

    stats = get_statistics()

    print(f"\nTotal posts: {stats['total_posts']}")
    print(f"Threat clusters: {len(stats.get('by_category', {}))}")

    if stats.get('by_category'):
        print("\nBy threat category:")
        for category, count in sorted(stats['by_category'].items()):
            print(f"  - {category.replace('_', ' ').title()}: {count}")

    if stats.get('by_severity'):
        print("\nBy severity:")
        for severity, count in sorted(stats['by_severity'].items()):
            print(f"  - {severity.upper()}: {count}")

    if stats.get('by_confidence'):
        print("\nBy confidence:")
        for confidence, count in sorted(stats['by_confidence'].items()):
            print(f"  - {confidence.upper()}: {count}")

    print()

def cmd_validate(args):
    """Run validation."""
    print("\n✅ ThreatScope AI - Validation")
    print("="*60)

    agent = ThreatScopeAgent()
    agent.validate_findings(require_manual_review=True)

def main():
    parser = argparse.ArgumentParser(
        description="ThreatScope AI - Autonomous Threat Intelligence Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full pipeline
  python main.py run

  # Collect data only
  python main.py collect

  # Analyze existing data
  python main.py analyze --sample 50

  # Launch dashboard
  python main.py dashboard

  # Generate report
  python main.py report

  # Show statistics
  python main.py stats
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run full pipeline')
    run_parser.add_argument('--no-reddit', action='store_true', help='Skip Reddit collection')
    run_parser.add_argument('--no-rss', action='store_true', help='Skip RSS collection')
    run_parser.add_argument('--sample-size', type=int, default=None, help='Sample N posts')
    run_parser.set_defaults(func=cmd_run_full)

    # Collect command
    collect_parser = subparsers.add_parser('collect', help='Collect data only')
    collect_parser.add_argument('--no-reddit', action='store_true', help='Skip Reddit')
    collect_parser.add_argument('--no-rss', action='store_true', help='Skip RSS')
    collect_parser.set_defaults(func=cmd_collect)

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze collected data')
    analyze_parser.add_argument('--sample-size', type=int, default=None, help='Sample N posts')
    analyze_parser.set_defaults(func=cmd_analyze)

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate report')
    report_parser.add_argument('--output', '-o', default='threat_report.md', help='Output file')
    report_parser.set_defaults(func=cmd_report)

    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Launch Streamlit dashboard')
    dashboard_parser.set_defaults(func=cmd_dashboard)

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.set_defaults(func=cmd_stats)

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Review findings')
    validate_parser.set_defaults(func=cmd_validate)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
