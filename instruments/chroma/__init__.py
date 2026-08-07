"""
Chroma Instruments Command Library

This package contains SCPI command definitions for various Chroma instruments.
Each model has its own command file for easy reference and maintenance.
"""

from .chroma_62000d_commands import Chroma62000DCommands
from .chroma_load_commands import ChromaElectronicLoadCommands
from .chroma_61500_commands import Chroma61500Commands

# Model registry mapping model names to command classes
CHROMA_COMMAND_REGISTRY = {
    # DC Bidirectional Power Supplies
    "62000D": Chroma62000DCommands,
    "62060D": Chroma62000DCommands,  # Same command set
    "62050D": Chroma62000DCommands,  # Same command set
    # Electronic Loads
    "6280":   ChromaElectronicLoadCommands,
    "63200":  ChromaElectronicLoadCommands,
    # AC Power Sources (61500 series)
    "61500":  Chroma61500Commands,
    "61501":  Chroma61500Commands,
    "61505":  Chroma61500Commands,
    "61507":  Chroma61500Commands,
    "61509":  Chroma61500Commands,
    "61512":  Chroma61500Commands,
}

def get_command_set(model):
    """
    Get the command set for a specific Chroma model

    Args:
        model: Model number (e.g., "62000D", "61509")

    Returns:
        Command class or None if not found
    """
    return CHROMA_COMMAND_REGISTRY.get(model)

__all__ = [
    'Chroma62000DCommands',
    'ChromaElectronicLoadCommands',
    'Chroma61500Commands',
    'CHROMA_COMMAND_REGISTRY',
    'get_command_set'
]
