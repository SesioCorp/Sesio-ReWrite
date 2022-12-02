from answer.models import Answer

def get_answer_by_preventive_maintenance(question, preventivemaintenance):
    if Answer.objects.filter(
        question=question, preventivemaintenance=preventivemaintenance, is_active=True
    ).exists():
        answer = Answer.objects.filter(
            question=question, preventivemaintenance=preventivemaintenance
        ).last()
        answer_dict = {"parent_answer": "", "image": ""}

        if question.answer_type in ["select", "radio"]:
            parent_question_answer = (
                question.parent_question.filter(category=question.category).first().parent_answer
                if question.parent_question.filter(category=question.category).exists() else ""
            )
            if answer.answer_type_text_number in parent_question_answer:
                try:
                    child_answer = Answer.objects.get(
                        question=question.parent_question.filter(category=question.category).first(),
                        preventivemaintenance=preventivemaintenance, is_active=True
                    )
                    image_url = child_answer.answer_type_image.url
                except Exception:
                    image_url = None
            else:
                image_url = None

            answer_dict["answer"] = answer.answer_type_text_number
            return_answer_dict

        elif question.answer_type in ["select_image"]:
            parent_question_answer = (
                question.parent_question.filter(category=question.category).first().parent_answer
                if question.parent_question.filter(category=question.category).exists() else ""
                
            )
            if answer.answer_type_text_number == parent_question_answer:
                try:
                    child_answer = Answer.objects.get(
                        question=question,
                        preventivemaintenance=preventivemaintenance,
                        is_active=True
                    )
                    image_url = child_answer.answer_type_image.url
                except Exception:
                    image_url=None
            else:
                image_url=None
            
            answer_dict["parent_answer"] = "pass" if image_url is None else "fail"
            answer_dict["image"] = image_url
            return answer_dict
        answer_dict["parent_answer"] = "pass"
        return answer_dict
    else:
        return None