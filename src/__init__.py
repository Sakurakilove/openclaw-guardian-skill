"""
TuanziGuardianClaw v2 - OpenClaw Security Kernel

A comprehensive security solution for OpenClaw AI Agents.
Provides threat detection, permission management, and audit capabilities.

Example usage:
    from guardian import SecurityKernel
    
    guardian = SecurityKernel()
    result = guardian.evaluate_operation(
        skill_input="Summarize this document",
        skill_action="summarize",
        skill_target="document.txt"
    )
    
    if result.blocked:
        print(f"Operation blocked: {result.reason}")
    else:
        print("Operation approved")
"""

__version__ = "2.0.0"
__author__ = "Tuanzi Security Team"
__license__ = "MIT"

# Import main components
from .security_kernel import SecurityKernel
from .risk_scorer import RiskScorer
from .threat_detector import ThreatDetector
from .permission_manager import PermissionManager
from .audit_logger import AuditLogger

__all__ = [
    "SecurityKernel",
    "RiskScorer",
    "ThreatDetector",
    "PermissionManager",
    "AuditLogger",
]
