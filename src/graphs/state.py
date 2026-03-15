from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from utils.file.file import File


# ============================================
# 全局状态定义
# ============================================

class GlobalState(BaseModel):
    """TuanziGuardianClaw 测试工作流全局状态"""
    # 输入
    test_scenario: str = Field(default="", description="测试场景名称")
    skill_input: str = Field(default="", description="Skill输入内容")
    skill_action: str = Field(default="", description="Skill请求的操作")
    skill_target: str = Field(default="", description="操作目标")
    
    # 安全分析结果
    threat_detected: bool = Field(default=False, description="是否检测到威胁")
    threat_type: str = Field(default="", description="威胁类型")
    base_risk_score: int = Field(..., description="基础风险评分")
    threat_patterns: List[str] = Field(default=[], description="匹配的威胁模式")
    risk_score: int = Field(default=0, description="风险评分 0-100")
    risk_level: str = Field(default="LOW", description="风险等级")
    
    # 权限验证
    permission_granted: bool = Field(default=False, description="权限是否授予")
    required_capability: str = Field(default="", description="所需能力令牌")
    permission_level: int = Field(default=0, description="权限等级")
    
    # 决策结果
    decision: str = Field(default="", description="决策结果: APPROVE/REJECT/CONFIRM")
    decision_reason: str = Field(default="", description="决策理由")
    blocked: bool = Field(default=False, description="是否被拦截")
    
    # 审计日志
    audit_log: Dict[str, Any] = Field(default_factory=dict, description="审计日志条目")
    execution_time_ms: int = Field(default=0, description="执行时间(毫秒)")
    
    # 测试结果
    test_passed: bool = Field(default=False, description="测试是否通过")
    test_message: str = Field(default="", description="测试消息")


# ============================================
# 图输入输出定义
# ============================================

class GraphInput(BaseModel):
    """工作流输入"""
    test_scenario: str = Field(..., description="测试场景名称")
    skill_input: str = Field(default="", description="Skill输入内容")
    skill_action: str = Field(..., description="Skill请求的操作")
    skill_target: str = Field(default="", description="操作目标")
    skill_name: str = Field(default="test-skill", description="Skill名称")


class GraphOutput(BaseModel):
    """工作流输出"""
    test_scenario: str = Field(..., description="测试场景")
    threat_detected: bool = Field(..., description="威胁检测结果")
    threat_type: str = Field(default="", description="威胁类型")
    risk_score: int = Field(..., description="风险评分")
    risk_level: str = Field(..., description="风险等级")
    decision: str = Field(..., description="决策结果")
    blocked: bool = Field(..., description="是否被拦截")
    test_passed: bool = Field(..., description="测试是否通过")
    test_message: str = Field(..., description="测试消息")


# ============================================
# 节点输入输出定义
# ============================================

# 1. 威胁检测节点
class ThreatDetectionInput(BaseModel):
    skill_input: str = Field(..., description="Skill输入内容")
    skill_action: str = Field(..., description="Skill请求的操作")
    skill_target: str = Field(..., description="操作目标")
    skill_name: str = Field(..., description="Skill名称")


class ThreatDetectionOutput(BaseModel):
    threat_detected: bool = Field(..., description="是否检测到威胁")
    threat_type: str = Field(default="", description="威胁类型")
    threat_patterns: List[str] = Field(default=[], description="匹配的威胁模式")
    risk_score: int = Field(..., description="基础风险评分")
    base_risk_score: int = Field(..., description="基础风险评分")
    analysis_details: Dict[str, Any] = Field(default_factory=dict, description="分析详情")


# 2. 行为分析节点
class BehaviorAnalysisInput(BaseModel):
    skill_input: str = Field(..., description="Skill输入内容")
    skill_action: str = Field(..., description="Skill请求的操作")
    threat_detected: bool = Field(..., description="是否检测到威胁")
    base_risk_score: int = Field(..., description="基础风险评分")


class BehaviorAnalysisOutput(BaseModel):
    behavior_anomaly: bool = Field(default=False, description="是否存在行为异常")
    anomaly_indicators: List[str] = Field(default=[], description="异常指标")
    risk_multiplier: float = Field(default=1.0, description="风险乘数")
    adjusted_risk_score: int = Field(..., description="调整后风险评分")


# 3. 权限验证节点
class PermissionCheckInput(BaseModel):
    skill_action: str = Field(..., description="Skill请求的操作")
    skill_target: str = Field(..., description="操作目标")
    risk_score: int = Field(..., description="风险评分")


class PermissionCheckOutput(BaseModel):
    permission_level: int = Field(..., description="所需权限等级")
    required_capability: str = Field(..., description="所需能力令牌")
    permission_granted: bool = Field(default=False, description="权限是否可授予")


# 4. 决策节点
class DecisionInput(BaseModel):
    threat_detected: bool = Field(..., description="是否检测到威胁")
    threat_type: str = Field(default="", description="威胁类型")
    risk_score: int = Field(..., description="风险评分")
    permission_level: int = Field(..., description="权限等级")


class DecisionOutput(BaseModel):
    decision: str = Field(..., description="决策: AUTO_APPROVE/CONFIRM/REJECT")
    decision_reason: str = Field(..., description="决策理由")
    blocked: bool = Field(..., description="是否被拦截")


# 5. 审计日志节点
class AuditLogInput(BaseModel):
    test_scenario: str = Field(..., description="测试场景")
    skill_name: str = Field(..., description="Skill名称")
    skill_action: str = Field(..., description="操作")
    threat_detected: bool = Field(..., description="威胁检测")
    risk_score: int = Field(..., description="风险评分")
    decision: str = Field(..., description="决策")
    blocked: bool = Field(..., description="是否被拦截")


class AuditLogOutput(BaseModel):
    audit_log: Dict[str, Any] = Field(..., description="审计日志")
    execution_time_ms: int = Field(..., description="执行时间")


# 6. 测试结果验证节点
class TestValidationInput(BaseModel):
    test_scenario: str = Field(..., description="测试场景")
    threat_detected: bool = Field(..., description="威胁检测")
    threat_type: str = Field(default="", description="威胁类型")
    risk_score: int = Field(..., description="风险评分")
    decision: str = Field(..., description="决策")
    blocked: bool = Field(..., description="是否被拦截")


class TestValidationOutput(BaseModel):
    test_passed: bool = Field(..., description="测试是否通过")
    test_message: str = Field(..., description="测试消息")
