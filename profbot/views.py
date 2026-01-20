from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Assignment, Submission
from .ai_service import grade_submission_with_gemini # Importing your brain!

@csrf_exempt
def upload_and_grade(request):
    if request.method == 'POST':
        try:
            # 1. Get Data from the Request
            assignment_id = request.POST.get('assignment_id')
            student_file = request.FILES.get('file')
            student_name = request.POST.get('student_name', 'Unknown Student')

            # Check if assignment exists
            try:
                assignment = Assignment.objects.get(id=assignment_id)
            except Assignment.DoesNotExist:
                return JsonResponse({'error': 'Assignment not found'}, status=404)

            # 2. Save to Database (So we have a record)
            submission = Submission.objects.create(
                assignment=assignment,
                student_name=student_name,
                answer_file=student_file
            )

            # 3. CALL THE AI (The Magic Step)
            # We get the file path from the object we just saved
            file_path = submission.answer_file.path
            
            print("Sending to Gemini...")
            ai_result = grade_submission_with_gemini(file_path, assignment.rubric)

            # 4. Save AI Result back to Database
            submission.marks_obtained = ai_result.get('marks')
            submission.ai_feedback = ai_result.get('feedback')
            submission.save()

            # 5. Return JSON to Frontend
            return JsonResponse({
                'status': 'success',
                'submission_id': submission.id,
                'marks': submission.marks_obtained,
                'feedback': submission.ai_feedback
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method allowed'}, status=400)