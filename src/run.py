import sys
import os

# Ensure root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator.workflow import main

if __name__ == "__main__":
    main()







