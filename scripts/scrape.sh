#!/bin/bash
source "$(dirname "${BASH_SOURCE[0]}")/pythonpath_dir.sh"
PYTHONPATH="$CODE_DIR" python -m src.scraper.main "$@"
