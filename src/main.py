#!/usr/bin/env python3
"""
Main entry point for the agentic application.
"""

from graph import build_graph


def main():
    """Main entry point function."""
    graph = build_graph()
    # Add your main execution logic here
    print("Graph built successfully!")


if __name__ == "__main__":
    main()
