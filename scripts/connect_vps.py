"""
Connect to N VPs (default: 54).

Searches Apollo for VP-level decision makers and imports them into the
configured Instantly campaign.

Usage:
    python scripts/connect_vps.py            # connects to 54 VPs
    python scripts/connect_vps.py --count 25 # connects to 25 VPs
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent import AutonomousLeadAgent


def main() -> int:
    parser = argparse.ArgumentParser(description="Connect to N VPs from Apollo.")
    parser.add_argument("--count", type=int, default=54, help="Number of VPs to connect to (default: 54)")
    args = parser.parse_args()

    agent = AutonomousLeadAgent()
    connected = agent.connect_vps(num_vps=args.count)
    return 0 if connected > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
