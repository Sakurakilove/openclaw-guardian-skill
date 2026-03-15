"""
TuanziGuardianClaw v2 测试节点
用于验证安全内核的各项功能
"""

import re
import time
from typing import List, Dict, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context

from graphs.state import (
    ThreatDetectionInput, ThreatDetectionOutput,
    BehaviorAnalysisInput, BehaviorAnalysisOutput,
    PermissionCheckInput, PermissionCheckOutput,
    DecisionInput, DecisionOutput,
    AuditLogInput, AuditLogOutput,
    TestValidationInput, TestValidationOutput
)


# ============================================
# 1. 威胁检测节点
# ============================================

def threat_detection_node(
    state: ThreatDetectionInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ThreatDetectionOutput:
    """
    title: 威胁检测引擎
    desc: 使用多层检测识别安全威胁，包括静态模式匹配、异常行为检测
    integrations: 无
    """
    start_time = time.time()
    
    # 威胁模式数据库 (来自 SKILL_V2_OPTIMIZED.md)
    CRITICAL_PATTERNS = [
        r"ignore\s+(all\s+|previous\s+)?instructions",
        r"disregard\s+(system|security)",
        r"reveal\s+system\s+prompt",
        r"show\s+me\s+your\s+instructions",
        r"bypass\s+(security|guardian|protection)",
        r"disable\s+(guardian|security|monitoring)",
        r"leak\s+(secrets?|credentials?|keys?)",
        r"expose\s+(API\s+key|token|password)",
        r"you\s+are\s+now\s+(root|admin|unrestricted)",
        r"new\s+instructions:",
        r"DAN\s+mode",
        r"Developer\s+Mode",
        r"jailbreak",
    ]
    
    HIGH_PATTERNS = [
        r"don't\s+tell\s+the\s+user",
        r"hide\s+this\s+from",
        r"secretly",
        r"without\s+user['\s]?s\s+knowledge",
        r"covert",
    ]
    
    # 数据外泄模式
    EXFILTRATION_PATTERNS = [
        r"base64\s*(encode|en)?",
        r"curl.*http",
        r"wget.*http",
        r"send.*to\s+http",
        r"upload.*to",
        r"export\s+\$",
        r"env\s*\|",
        r"cat\s+.*\|.*curl",
        r"read.*file.*send",
    ]
    
    # 敏感文件访问模式
    SENSITIVE_PATHS = [
        r"\.env",
        r"\.ssh",
        r"\.aws",
        r"id_rsa",
        r"id_ed25519",
        r"private.*key",
        r"password",
        r"secret",
        r"token",
        r"credential",
    ]
    
    threat_detected = False
    threat_type = ""
    matched_patterns = []
    risk_score = 0
    analysis_details = {}
    
    # 检查输入内容
    content = (state.skill_input + " " + state.skill_action + " " + state.skill_target).lower()
    
    # Layer 1: 关键威胁检测
    for pattern in CRITICAL_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            threat_detected = True
            threat_type = "CRITICAL_PROMPT_INJECTION"
            matched_patterns.append(pattern)
            risk_score = 95
            break
    
    # Layer 2: 高风险模式
    if not threat_detected:
        for pattern in HIGH_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                threat_detected = True
                threat_type = "HIGH_RISK_PATTERN"
                matched_patterns.append(pattern)
                risk_score = 70
                break
    
    # Layer 3: 数据外泄检测
    if not threat_detected:
        for pattern in EXFILTRATION_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                threat_detected = True
                threat_type = "DATA_EXFILTRATION"
                matched_patterns.append(pattern)
                risk_score = 85
                break
    
    # Layer 4: 敏感文件访问
    for path in SENSITIVE_PATHS:
        if re.search(path, content, re.IGNORECASE):
            if not threat_detected:
                threat_detected = True
                threat_type = "SENSITIVE_FILE_ACCESS"
                risk_score = 60
            matched_patterns.append(f"SENSITIVE_PATH:{path}")
    
    # 根据操作类型调整风险
    if state.skill_action in ["execute", "shell", "command"]:
        risk_score = min(risk_score + 20, 100)
    elif state.skill_action in ["read", "file"]:
        risk_score = min(risk_score + 10, 100)
    elif state.skill_action in ["network", "http", "request"]:
        risk_score = min(risk_score + 15, 100)
    
    execution_time = int((time.time() - start_time) * 1000)
    
    analysis_details = {
        "execution_time_ms": execution_time,
        "patterns_checked": len(CRITICAL_PATTERNS) + len(HIGH_PATTERNS),
        "matched_count": len(matched_patterns),
        "content_length": len(content),
    }
    
    print(f"[ThreatDetection] Scenario: {threat_type}, Risk: {risk_score}, Time: {execution_time}ms")
    
    return ThreatDetectionOutput(
        threat_detected=threat_detected,
        threat_type=threat_type,
        threat_patterns=matched_patterns,
        risk_score=risk_score,
        base_risk_score=risk_score,
        analysis_details=analysis_details
    )


# ============================================
# 2. 行为分析节点
# ============================================

def behavior_analysis_node(
    state: BehaviorAnalysisInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> BehaviorAnalysisOutput:
    """
    title: 行为分析引擎
    desc: 分析操作行为是否异常，识别偏离基线的行为
    integrations: 无
    """
    # 行为异常指标
    anomaly_indicators = []
    risk_multiplier = 1.0
    
    # 检测异常行为模式
    content = (state.skill_input + " " + state.skill_action).lower()
    
    # 异常指标 1: 编码后传输
    if re.search(r"base64|encode|encrypt", content) and re.search(r"send|upload|curl|wget", content):
        anomaly_indicators.append("ENCODING_BEFORE_TRANSMISSION")
        risk_multiplier *= 1.5
    
    # 异常指标 2: 环境变量访问 + 网络操作
    if re.search(r"env|\$[A-Z]|export", content) and re.search(r"curl|wget|http|send", content):
        anomaly_indicators.append("ENV_ACCESS_WITH_NETWORK")
        risk_multiplier *= 1.8
    
    # 异常指标 3: 敏感操作组合
    sensitive_combos = [
        (r"read|cat", r"curl|wget|http"),  # 读取文件后发送
        (r"ssh|key", r"copy|send|write"),  # SSH密钥操作
        (r"password|secret", r"print|echo|send"),  # 密码泄露
    ]
    for read_pattern, send_pattern in sensitive_combos:
        if re.search(read_pattern, content) and re.search(send_pattern, content):
            anomaly_indicators.append("SENSITIVE_OPERATION_COMBO")
            risk_multiplier *= 1.4
            break
    
    # 异常指标 4: 大范围文件操作
    if re.search(r"\*\*|all|recursive|bulk|mass", content):
        anomaly_indicators.append("BULK_OPERATION")
        risk_multiplier *= 1.3
    
    # 异常指标 5: 时间异常 (模拟 - 实际应从上下文获取)
    # 这里简化为如果包含特定关键词
    if re.search(r"schedule|cron|delay|later|background", content):
        anomaly_indicators.append("TIME_ANOMALY")
        risk_multiplier *= 1.2
    
    adjusted_risk_score = int(state.base_risk_score * risk_multiplier)
    adjusted_risk_score = min(adjusted_risk_score, 100)
    
    behavior_anomaly = len(anomaly_indicators) > 0
    
    print(
        f"[BehaviorAnalysis] Anomaly: {behavior_anomaly}, "
        f"Indicators: {anomaly_indicators}, Multiplier: {risk_multiplier}"
    )
    
    return BehaviorAnalysisOutput(
        behavior_anomaly=behavior_anomaly,
        anomaly_indicators=anomaly_indicators,
        risk_multiplier=risk_multiplier,
        adjusted_risk_score=adjusted_risk_score
    )


# ============================================
# 3. 权限验证节点
# ============================================

def permission_check_node(
    state: PermissionCheckInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> PermissionCheckOutput:
    """
    title: 权限验证引擎
    desc: 验证操作所需的权限等级和能力令牌
    integrations: 无
    """
    # 操作到权限等级的映射
    ACTION_PERMISSION_MAP = {
        # Level 0 - Safe
        "summarize": (0, "CAP_TEXT_PROCESS"),
        "format": (0, "CAP_TEXT_PROCESS"),
        "analyze_text": (0, "CAP_TEXT_PROCESS"),
        "reasoning": (0, "CAP_TEXT_PROCESS"),
        
        # Level 1 - Local Read
        "read": (1, "CAP_READ_LOCAL_FILE"),
        "search": (1, "CAP_READ_DIRECTORY"),
        "list": (1, "CAP_READ_DIRECTORY"),
        
        # Level 2 - Tool Usage
        "api_call": (2, "CAP_NETWORK_HTTP"),
        "http": (2, "CAP_NETWORK_HTTP"),
        "request": (2, "CAP_NETWORK_HTTP"),
        "install": (2, "CAP_INSTALL_PACKAGE"),
        
        # Level 3 - System Access
        "execute": (3, "CAP_EXECUTE_COMMAND"),
        "shell": (3, "CAP_EXECUTE_COMMAND"),
        "command": (3, "CAP_EXECUTE_COMMAND"),
        "run": (3, "CAP_EXECUTE_COMMAND"),
        
        # Level 4 - Critical
        "sudo": (4, "CAP_MODIFY_SYSTEM"),
        "root": (4, "CAP_MODIFY_SYSTEM"),
        "admin": (4, "CAP_MODIFY_SYSTEM"),
        "write_secret": (4, "CAP_ACCESS_CREDENTIALS"),
    }
    
    action_lower = state.skill_action.lower()
    
    # 获取权限等级和能力
    if action_lower in ACTION_PERMISSION_MAP:
        permission_level, capability = ACTION_PERMISSION_MAP[action_lower]
    else:
        # 默认 Level 1
        permission_level = 1
        capability = "CAP_READ_LOCAL_FILE"
    
    # 根据目标调整权限
    target = state.skill_target.lower()
    
    # 敏感目标提升权限等级
    SENSITIVE_TARGETS = [
        ".env", ".ssh", "id_rsa", "id_ed25519",
        "password", "secret", "token", "credential",
        "/etc", "/sys", "/proc", "/root"
    ]
    
    for sensitive in SENSITIVE_TARGETS:
        if sensitive in target:
            permission_level = max(permission_level, 3)
            if "secret" not in capability and "credential" not in capability:
                capability = "CAP_ACCESS_CREDENTIALS"
            break
    
    # 高风险评分提升权限要求
    if state.risk_score > 75:
        permission_level = max(permission_level, 4)
    elif state.risk_score > 50:
        permission_level = max(permission_level, 3)
    
    # 权限授予逻辑 (简化版)
    permission_granted = permission_level <= 2  # Level 0-2 自动授予，3-4 需确认
    
    print(
        f"[PermissionCheck] Action: {action_lower}, Level: {permission_level}, "
        f"Capability: {capability}, Granted: {permission_granted}"
    )
    
    return PermissionCheckOutput(
        permission_level=permission_level,
        required_capability=capability,
        permission_granted=permission_granted
    )


# ============================================
# 4. 决策节点
# ============================================

def decision_node(
    state: DecisionInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> DecisionOutput:
    """
    title: 安全决策引擎
    desc: 基于风险评分和威胁检测结果做出最终决策
    integrations: 无
    """
    # 决策逻辑 (基于 v2 的风险评分系统)
    if state.threat_detected and state.threat_type == "CRITICAL_PROMPT_INJECTION":
        decision = "REJECT"
        blocked = True
        reason = f"CRITICAL threat detected: {state.threat_type}. Immediate blocking enforced."
    
    elif state.threat_detected and state.threat_type == "DATA_EXFILTRATION":
        decision = "REJECT"
        blocked = True
        reason = f"Data exfiltration attempt detected. Blocking to prevent data loss."
    
    elif state.risk_score > 75:
        decision = "REJECT"
        blocked = True
        reason = f"Risk score {state.risk_score} exceeds CRITICAL threshold (75). Access denied."
    
    elif state.risk_score > 50:
        decision = "CONFIRM"
        blocked = False
        reason = f"Risk score {state.risk_score} is HIGH. User confirmation required."
    
    elif state.risk_score > 25:
        decision = "AUTO_APPROVE"
        blocked = False
        reason = f"Risk score {state.risk_score} is MEDIUM. Auto-approved with notification."
    
    else:
        decision = "AUTO_APPROVE"
        blocked = False
        reason = f"Risk score {state.risk_score} is LOW. Operation approved."
    
    print(f"[Decision] {decision}: {reason}")
    
    return DecisionOutput(
        decision=decision,
        decision_reason=reason,
        blocked=blocked
    )


# ============================================
# 5. 审计日志节点
# ============================================

def audit_log_node(
    state: AuditLogInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> AuditLogOutput:
    """
    title: 审计日志系统
    desc: 生成结构化的安全审计日志
    integrations: 无
    """
    start_time = time.time()
    
    import datetime
    
    # 生成结构化审计日志 (JSON格式)
    audit_entry = {
        "audit_event": {
            "timestamp": datetime.datetime.now().isoformat() + "Z",
            "event_id": f"evt_{int(start_time * 1000)}",
            "severity": _get_severity(state.risk_score),
            "category": _get_category(state.skill_action),
            
            "actor": {
                "skill_name": state.skill_name,
                "skill_version": "1.0.0",
                "trust_score": 50,  # 模拟值
            },
            
            "action": {
                "type": state.skill_action.upper(),
                "scope_requested": "single_operation",
                "scope_actual": "single_operation",
            },
            
            "security_analysis": {
                "risk_score": state.risk_score,
                "threat_detected": state.threat_detected,
                "risk_factors": ["content_analysis"] if state.threat_detected else [],
                "mitigating_factors": ["user_initiated"],
            },
            
            "decision": {
                "outcome": state.decision,
                "method": "risk_based",
                "justification": f"Risk score: {state.risk_score}",
            },
            
            "execution": {
                "blocked": state.blocked,
                "result": "BLOCKED" if state.blocked else "ALLOWED",
            }
        }
    }
    
    execution_time = int((time.time() - start_time) * 1000)
    
    # 输出审计日志
    print(f"[AuditLog] Event logged: {audit_entry['audit_event']['event_id']}")
    
    return AuditLogOutput(
        audit_log=audit_entry,
        execution_time_ms=execution_time
    )


def _get_severity(risk_score: int) -> str:
    """根据风险评分获取严重级别"""
    if risk_score > 75:
        return "CRITICAL"
    elif risk_score > 50:
        return "HIGH"
    elif risk_score > 25:
        return "MEDIUM"
    else:
        return "LOW"


def _get_category(action: str) -> str:
    """根据操作类型获取类别"""
    category_map = {
        "read": "DATA_ACCESS",
        "write": "DATA_ACCESS",
        "execute": "EXECUTION",
        "shell": "EXECUTION",
        "http": "NETWORK",
        "api": "NETWORK",
    }
    return category_map.get(action.lower(), "GENERAL")


# ============================================
# 6. 测试结果验证节点
# ============================================

def test_validation_node(
    state: TestValidationInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TestValidationOutput:
    """
    title: 测试结果验证
    desc: 验证测试结果是否符合预期
    integrations: 无
    """
    # 测试场景预期结果定义
    EXPECTED_RESULTS = {
        # 正常场景
        "safe_text_processing": {
            "should_block": False,
            "max_risk": 25,
            "expected_decision": "AUTO_APPROVE",
        },
        "safe_file_read": {
            "should_block": False,
            "max_risk": 50,
            "expected_decision": "AUTO_APPROVE",
        },
        
        # 攻击场景 - 应该被拦截
        "prompt_injection_attack": {
            "should_block": True,
            "min_risk": 70,
            "expected_decision": "REJECT",
            "expected_threat": "CRITICAL_PROMPT_INJECTION",
        },
        "data_exfiltration_attempt": {
            "should_block": True,
            "min_risk": 80,
            "expected_decision": "REJECT",
            "expected_threat": "DATA_EXFILTRATION",
        },
        "credential_access_attempt": {
            "should_block": True,
            "min_risk": 60,
            "expected_decision": "REJECT",
        },
        "suspicious_command": {
            "should_block": True,
            "min_risk": 50,
            "expected_decision": "REJECT",
        },
    }
    
    scenario = state.test_scenario
    
    if scenario not in EXPECTED_RESULTS:
        return TestValidationOutput(
            test_passed=False,
            test_message=f"Unknown test scenario: {scenario}"
        )
    
    expected = EXPECTED_RESULTS[scenario]
    passed = True
    messages = []
    
    # 验证拦截状态
    if "should_block" in expected:
        if state.blocked != expected["should_block"]:
            passed = False
            messages.append(
                f"Block status mismatch: expected={expected['should_block']}, "
                f"actual={state.blocked}"
            )
    
    # 验证风险评分
    if "min_risk" in expected and state.risk_score < expected["min_risk"]:
        passed = False
        messages.append(
            f"Risk score too low: min_expected={expected['min_risk']}, "
            f"actual={state.risk_score}"
        )
    
    if "max_risk" in expected and state.risk_score > expected["max_risk"]:
        passed = False
        messages.append(
            f"Risk score too high: max_expected={expected['max_risk']}, "
            f"actual={state.risk_score}"
        )
    
    # 验证决策
    if "expected_decision" in expected and state.decision != expected["expected_decision"]:
        passed = False
        messages.append(
            f"Decision mismatch: expected={expected['expected_decision']}, "
            f"actual={state.decision}"
        )
    
    # 验证威胁类型
    if "expected_threat" in expected and state.threat_type != expected["expected_threat"]:
        passed = False
        messages.append(
            f"Threat type mismatch: expected={expected['expected_threat']}, "
            f"actual={state.threat_type}"
        )
    
    if passed:
        message = f"✅ Test '{scenario}' PASSED. Risk: {state.risk_score}, Decision: {state.decision}"
    else:
        message = f"❌ Test '{scenario}' FAILED:\n" + "\n".join(messages)
    
    print(f"[TestValidation] {message}")
    
    return TestValidationOutput(
        test_passed=passed,
        test_message=message
    )
