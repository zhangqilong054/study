import os
import sys
from flask import Blueprint, request, jsonify

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.ai_service import chat_completion

growth_bp = Blueprint("growth", __name__, url_prefix="/api/growth")


@growth_bp.route("/career-plan", methods=["POST"])
def career_plan():
    """学业与职业规划建议"""
    data = request.json or {}
    major = data.get("major", "").strip()
    grade = data.get("grade", "").strip()
    interests = data.get("interests", "").strip()
    goals = data.get("goals", "").strip()

    if not major:
        return jsonify({"error": "请填写专业信息"}), 400

    context = f"专业：{major}"
    if grade:
        context += f"\n年级：{grade}"
    if interests:
        context += f"\n兴趣方向：{interests}"
    if goals:
        context += f"\n目标/期望：{goals}"

    messages = [
        {
            "role": "system",
            "content": (
                "你是一位经验丰富的大学生涯规划导师。请根据学生的专业、年级和兴趣，"
                "提供个性化的学业规划和职业发展建议。包括：\n"
                "1. 在校期间学业重点安排\n"
                "2. 核心技能培养路径\n"
                "3. 实习/项目/竞赛建议\n"
                "4. 毕业去向选择（就业/考研/出国）分析\n"
                "5. 近期可执行的行动计划\n"
                "使用 Markdown 格式，结合 emoji 增加可读性。"
            ),
        },
        {"role": "user", "content": f"请为我提供学业规划建议：\n{context}"},
    ]
    result = chat_completion(messages, temperature=0.6)
    return jsonify({"result": result})


@growth_bp.route("/resume", methods=["POST"])
def optimize_resume():
    """简历优化辅助"""
    data = request.json or {}
    resume_text = data.get("resume", "").strip()
    target_position = data.get("position", "").strip()
    target_industry = data.get("industry", "").strip()

    if not resume_text:
        return jsonify({"error": "请粘贴您的简历内容"}), 400

    context = f"目标岗位：{target_position}" if target_position else ""
    if target_industry:
        context += f"\n目标行业：{target_industry}"

    messages = [
        {
            "role": "system",
            "content": (
                "你是一位专业的简历优化顾问，熟悉各类岗位的招聘要求。"
                "请对学生的简历提供全面的优化建议，包括：\n"
                "1. 整体结构和排版建议\n"
                "2. 各模块内容优化（量化成果、动词使用等）\n"
                "3. 关键词优化建议\n"
                "4. 需要补充或删减的内容\n"
                "5. 针对目标岗位的个性化建议\n"
                "请直接给出优化后的建议版本（关键部分）。"
            ),
        },
        {
            "role": "user",
            "content": (
                f"{'岗位信息：' + context + chr(10) + chr(10) if context else ''}"
                f"我的简历内容如下，请帮我优化：\n\n{resume_text[:2000]}"
            ),
        },
    ]
    result = chat_completion(messages, temperature=0.5)
    return jsonify({"result": result})


@growth_bp.route("/interview", methods=["POST"])
def interview_practice():
    """面试表达训练"""
    data = request.json or {}
    position = data.get("position", "").strip()
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()
    mode = data.get("mode", "feedback")  # feedback / generate

    if mode == "generate":
        if not position:
            return jsonify({"error": "请填写目标岗位"}), 400
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一位专业的面试官，熟悉各类岗位的面试题目。"
                    "请根据目标岗位生成常见面试题，包括行为面试题、情景题和专业题。"
                ),
            },
            {
                "role": "user",
                "content": f"请为【{position}】岗位生成10道常见面试题，并注明题型。",
            },
        ]
    else:
        if not question or not answer:
            return jsonify({"error": "请填写面试题目和您的回答"}), 400
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一位经验丰富的面试教练。请对学生的面试回答进行点评，"
                    "从内容完整性、表达逻辑、亮点挖掘等方面给出具体改进建议，"
                    "并提供一个优化后的示范回答。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"面试题目：{question}\n\n"
                    f"{'目标岗位：' + position + chr(10) + chr(10) if position else ''}"
                    f"我的回答：{answer}\n\n"
                    "请点评并给出优化建议和示范回答。"
                ),
            },
        ]
    result = chat_completion(messages, temperature=0.6)
    return jsonify({"result": result})


@growth_bp.route("/campus-nav", methods=["POST"])
def campus_nav():
    """校园生活信息导航"""
    data = request.json or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "请输入您的问题"}), 400

    messages = [
        {
            "role": "system",
            "content": (
                "你是一位热心的学长/学姐，熟悉大学校园生活的方方面面。"
                "请用轻松友好的语气，为学弟学妹提供校园生活相关的建议和信息导航，"
                "包括学习资源、社团活动、生活服务、心理健康等方面。"
            ),
        },
        {"role": "user", "content": query},
    ]
    result = chat_completion(messages, temperature=0.7)
    return jsonify({"result": result})


@growth_bp.route("/exam-reminder", methods=["POST"])
def exam_reminder():
    """考试/重要日期提醒生成"""
    data = request.json or {}
    exams = data.get("exams", [])
    semester_start = data.get("semester_start", "").strip()

    if not exams:
        return jsonify({"error": "请提供考试信息"}), 400

    exam_list = "\n".join(
        f"- {e.get('name', '未命名')}：{e.get('date', '待定')}（{e.get('notes', '')}）"
        for e in exams
    )

    messages = [
        {
            "role": "system",
            "content": (
                "你是一位贴心的学习助手。请根据学生的考试日历，"
                "生成考前复习提醒计划，包括考前1个月、2周、1周、3天的复习建议。"
            ),
        },
        {
            "role": "user",
            "content": (
                f"{'本学期开始日期：' + semester_start + chr(10) if semester_start else ''}"
                f"我的考试安排如下：\n{exam_list}\n\n"
                "请生成复习提醒计划。"
            ),
        },
    ]
    result = chat_completion(messages, temperature=0.5)
    return jsonify({"result": result})
