from flask import request, abort, jsonify


def get_int(num: int):
    """Validate if given value is or can be integer"""
    if type(num) != int:
        try:
            num = int(num)
        except TypeError:
            abort(400)

    return num


def exists(obj):
    if not obj:
        abort(404)

    return obj


def get_page_number():
    """Validate page number is less than 100"""
    page_number = get_int(request.args.get("page", 1, int))
    if page_number > 100:
        abort(400)

    return page_number


def format_questions(data, api):
    questions = data.get('questions')

    return jsonify({
        "success": True,
        "questions": exists(api.paginated_questions(questions, get_page_number())),
        "total_questions": len(questions),
        "current_category": data.get('category')
    })
