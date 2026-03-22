# iit hyderbad prism

## Overview
This repository contains the source code and assets for **iit hyderbad prism**.



## Architecture Overview

### Project Type
- **Primary stack:** Python application
- **Primary language:** Python
- **Primary entrypoint/build root:** main module or app script

### High-Level Architecture
- This repository is organized in modular directories grouped by concern (application code, configuration, scripts, documentation, and assets).
- Runtime/build artifacts such as virtual environments, node modules, and compiled outputs are intentionally excluded from architecture mapping.
- The project follows a layered flow: entry point -> domain/application modules -> integrations/data/config.

### Component Breakdown
- **Application layer:** Core executables, services, UI, or command handlers.
- **Domain/business layer:** Feature logic and processing modules.
- **Integration layer:** External APIs, databases, files, or platform-specific connectors.
- **Support layer:** Config, scripts, docs, tests, and static assets.

### Data/Execution Flow
1. Start from the configured entrypoint or package scripts.
2. Route execution into feature-specific modules.
3. Process domain logic and interact with integrations/storage.
4. Return results to UI/API/CLI outputs.

### Directory Map (Top-Level + Key Subfolders)
```
create_presentation.py
.DS_Store
prism
prism/.DS_Store
prism/requirements.txt
prism/_h_batch_production_data.xlsx
prism/.streamlit
prism/extract_stats.py
prism/utils
prism/models
prism/__pycache__
prism/README.md
prism/.gitignore
prism/.venv
prism/app.py
prism/_h_batch_process_data.xlsx
prism/_debug_5whys.py
prism/.git
prism/modules
prism/data
prism/test_pipeline.py
PRISM_PPT_DATA_A_TO_Z.md
README.md
.venv
create_data.py
```

### Notes
- Architecture section auto-generated on 2026-03-22 and can be refined further with exact runtime/deployment details.
