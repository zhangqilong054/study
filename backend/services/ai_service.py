import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import AI_API_KEY, AI_API_BASE, AI_MODEL

try:
    from openai import OpenAI
    _client = None

    def _get_client():
        global _client
        if _client is None:
            if not AI_API_KEY:
                return None
            _client = OpenAI(api_key=AI_API_KEY, base_url=AI_API_BASE)
        return _client

    def chat_completion(messages, temperature=0.7, max_tokens=2000):
        """调用 AI 接口获取回复"""
        if not AI_API_KEY:
            return _mock_response(messages)
        try:
            client = _get_client()
            if client is None:
                return _mock_response(messages)
            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception:
            return "[AI服务暂时不可用，请稍后重试或联系管理员]"

except ImportError:
    def chat_completion(messages, temperature=0.7, max_tokens=2000):
        return _mock_response(messages)


def _mock_response(messages):
    """在未配置 API Key 时返回演示性回复"""
    last = messages[-1]["content"] if messages else ""
    if "知识点" in last or "课件" in last or "总结" in last:
        return (
            "**课件知识点提炼（演示）**\n\n"
            "1. **核心概念**：本章围绕主要理论展开，包括基本定义、原理与应用场景。\n"
            "2. **重要定理**：掌握定理推导过程及其适用条件。\n"
            "3. **典型例题**：通过例题理解知识点的实际应用方法。\n"
            "4. **易错点**：注意区分相似概念，避免混淆。\n\n"
            "> ⚠️ 当前为演示模式，请在 `.env` 文件中配置 `AI_API_KEY` 以启用真实AI功能。"
        )
    if "练习题" in last or "题目" in last:
        return (
            "**自动生成练习题（演示）**\n\n"
            "**单选题**\n"
            "1. 下列说法正确的是（ ）\n   A. 选项A  B. 选项B  C. 选项C  D. 选项D\n\n"
            "**简答题**\n"
            "2. 请简述该知识点的核心原理及应用场景。\n\n"
            "**综合题**\n"
            "3. 结合所学知识，分析并解决以下实际问题……\n\n"
            "> ⚠️ 当前为演示模式，请配置 `AI_API_KEY` 以启用真实AI功能。"
        )
    if "复习计划" in last or "计划" in last:
        return (
            "**个性化复习计划（演示）**\n\n"
            "📅 **第1周**：梳理基础概念，完成课本第1-3章复习，做课后习题。\n"
            "📅 **第2周**：重点攻克难点章节，整理错题，总结解题思路。\n"
            "📅 **第3周**：综合练习，模拟考试，查漏补缺。\n"
            "📅 **考前2天**：回顾知识图谱，重温重要公式与定理。\n\n"
            "> ⚠️ 当前为演示模式，请配置 `AI_API_KEY` 以启用真实AI功能。"
        )
    if "请假" in last:
        return (
            "**请假流程（演示）**\n\n"
            "1. 登录学校教务系统，进入【学生请假】模块。\n"
            "2. 填写请假原因、起止时间，上传相关证明材料（如病假需提供医院证明）。\n"
            "3. 提交申请后，等待辅导员审批（一般1-2个工作日）。\n"
            "4. 审批通过后，系统自动发送短信通知。\n"
            "5. 销假时需在系统内登记返校时间。\n\n"
            "📋 **所需材料**：学生证、请假申请表、相关证明材料\n"
            "📍 **办理地点**：辅导员办公室 / 教务系统线上办理\n\n"
            "> ⚠️ 当前为演示模式，请配置 `AI_API_KEY` 以启用真实AI功能。"
        )
    if "奖助学金" in last or "奖学金" in last or "助学金" in last:
        return (
            "**奖助学金申请流程（演示）**\n\n"
            "1. 关注学院通知，了解申请时间节点（一般每学年9-10月）。\n"
            "2. 在教务/学工系统中填写申请表，填写个人基本信息和成绩情况。\n"
            "3. 准备所需材料：成绩单、家庭经济情况证明（助学金）等。\n"
            "4. 提交至辅导员，班级民主评议后上报学院。\n"
            "5. 学院审核公示，无异议后上报学校。\n"
            "6. 学校审批后发放至学生银行卡。\n\n"
            "📋 **所需材料**：申请表、成绩单、家庭经济证明（助学金需要）\n\n"
            "> ⚠️ 当前为演示模式，请配置 `AI_API_KEY` 以启用真实AI功能。"
        )
    if "简历" in last:
        return (
            "**简历优化建议（演示）**\n\n"
            "✅ **基本结构**：个人信息 → 教育背景 → 实习/项目经历 → 技能 → 荣誉\n\n"
            "📝 **优化建议**：\n"
            "1. 使用动词开头描述经历，如【负责】【主导】【优化】等。\n"
            "2. 量化成果，如【提升效率30%】【参与10万行代码项目】。\n"
            "3. 突出与岗位匹配的技能和经历。\n"
            "4. 保持简洁，控制在1页以内（应届生）。\n"
            "5. 检查排版，确保字体统一、间距合理。\n\n"
            "> ⚠️ 当前为演示模式，请配置 `AI_API_KEY` 以启用真实AI功能。"
        )
    return (
        "**智校通 AI 助手（演示模式）**\n\n"
        "您好！我是智校通 AI 助手，可以帮助您：\n"
        "- 📚 提炼课程知识点、生成练习题和复习计划\n"
        "- 🏫 查询校园事务流程（请假、奖助学金、证件补办等）\n"
        "- 🎯 提供学业规划、简历优化和面试建议\n\n"
        f"您的问题：{last[:100]}{'...' if len(last) > 100 else ''}\n\n"
        "> ⚠️ 当前为演示模式，请在 `.env` 文件中配置 `AI_API_KEY` 以启用真实AI功能。"
    )
