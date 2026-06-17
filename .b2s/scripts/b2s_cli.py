"""CLI entry point for the staged `.b2s` framework."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from b2s_engine import dispatch, gates, init_workspace, inputs, next_step, reset, state, validation  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="b2s_cli.py",
        description="CLI for the staged .b2s framework.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    commands = {
        "init-workspace": init_workspace.run,
        "dispatch-next": dispatch.run,
        "next-step": next_step.run,
        "collect-inputs": inputs.run,
        "validate-artifact": validation.run,
        "update-state": state.run,
        "repair-state": state.repair_state,
        "reset-to-phase": reset.run,
        "retry-action": gates.retry_action,
        "rerun-last-action": gates.rerun_last_action,
        "approve-current-gate": gates.approve_current_gate,
        "reject-current-gate": gates.reject_current_gate,
    }

    for name, handler in commands.items():
        subparser = subparsers.add_parser(name, help=f"Run `{name}`.")
        subparser.add_argument(
            "--workspace-root",
            type=Path,
            required=False,
            help="Path to the initiative workspace.",
        )
        subparser.add_argument(
            "--output",
            type=Path,
            required=False,
            help="Machine-readable output path for the command.",
        )
        if name in {"collect-inputs", "validate-artifact", "update-state"}:
            subparser.add_argument(
                "--action-id",
                type=str,
                required=False,
                help="Override the action ID instead of using the active action in workflow state.",
            )
        if name == "init-workspace":
            subparser.add_argument(
                "--initiative-id",
                type=str,
                required=False,
                help="Initiative ID (e.g. I012-MY-APP). Used to derive workspace path when --workspace-root is omitted.",
            )
        if name == "retry-action":
            subparser.add_argument(
                "--action-id",
                type=str,
                required=True,
                help="The action ID to reopen for retry after a gate rejection.",
            )
        if name in {"approve-current-gate", "reject-current-gate"}:
            subparser.add_argument(
                "--reason",
                type=str,
                required=False,
                help="Optional decision note to persist in the gate output.",
            )
        if name == "reset-to-phase":
            subparser.add_argument(
                "--stage-id",
                type=str,
                required=False,
                help="Stage ID to reset the workflow back to.",
            )
        subparser.set_defaults(handler=handler)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.handler(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
