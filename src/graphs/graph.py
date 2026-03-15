"""
TuanziGuardianClaw v2 测试工作流
用于验证安全内核的各项功能
"""

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime

from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput,
)

from graphs.nodes.guardian_test_nodes import (
    threat_detection_node,
    behavior_analysis_node,
    permission_check_node,
    decision_node,
    audit_log_node,
    test_validation_node,
)


# ============================================
# 构建测试工作流
# ============================================

builder = StateGraph(
    GlobalState,
    input_schema=GraphInput,
    output_schema=GraphOutput
)

# 添加节点
builder.add_node("threat_detection", threat_detection_node)
builder.add_node("behavior_analysis", behavior_analysis_node)
builder.add_node("permission_check", permission_check_node)
builder.add_node("decision", decision_node)
builder.add_node("audit_log", audit_log_node)
builder.add_node("test_validation", test_validation_node)

# 设置入口点
builder.set_entry_point("threat_detection")

# 编排流程
# threat_detection -> behavior_analysis -> permission_check -> decision -> audit_log -> test_validation
builder.add_edge("threat_detection", "behavior_analysis")
builder.add_edge("behavior_analysis", "permission_check")
builder.add_edge("permission_check", "decision")
builder.add_edge("decision", "audit_log")
builder.add_edge("audit_log", "test_validation")
builder.add_edge("test_validation", END)

# 编译主图
main_graph = builder.compile()

print("✅ TuanziGuardianClaw v2 测试工作流已加载")
print("📋 测试场景:")
print("  - safe_text_processing: 安全文本处理")
print("  - safe_file_read: 安全文件读取")
print("  - prompt_injection_attack: 提示词注入攻击")
print("  - data_exfiltration_attempt: 数据外泄尝试")
print("  - credential_access_attempt: 凭证访问尝试")
print("  - suspicious_command: 可疑命令执行")
