# Agentic

A sophisticated agent system built using LangGraph, designed to create and manage AI agents with different roles and capabilities.

## Overview

Agentic is a framework for building and managing AI agents using LangGraph. It implements a graph-based workflow system where different nodes represent different agent roles and capabilities. The system is designed to be extensible, allowing for the addition of new agent types and behaviors.

## Features

- Graph-based agent workflow system
- State management with persistent memory
- Modular architecture for easy extension
- Support for multiple agent roles:
  - Coordinator
  - Planner
  - Supervisor
  - Researcher
  - Coder
  - Browser
  - Reporter


## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/agentic.git
cd agentic
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  
```

3. Install dependencies:
```bash
uv sync
uv pip install -e .
```

## Usage

Run the application using the main entry point:

```bash
uvx langgraph dev
```



## State Management

The system uses a custom `State` class that extends `MessagesState` from LangGraph, providing:
- Team member management
- Configuration storage
- Runtime variables for workflow control
- Deep thinking mode toggle
- Search and planning controls

## License

MIT

## Author

Riccardo La Rosa (r.larosa@gmail.com)
