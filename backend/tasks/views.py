from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import TaskSerializer
from .scoring import score_task


class AnalyzeTasksView(APIView):
    def post(self, request):
        data = request.data

        tasks = data.get("tasks", [])
        strategy = data.get("strategy", "smart-balance")

        if not isinstance(tasks, list):
            return Response({"error": "tasks must be a list"}, status=400)

        validated_tasks = []
        for t in tasks:
            s = TaskSerializer(data=t)
            if not s.is_valid():
                return Response({"error": "invalid task", "details": s.errors}, status=400)
            validated_tasks.append(s.validated_data)

        # Assign IDs automatically if missing
        for i, t in enumerate(validated_tasks):
            if "id" not in t:
                t["id"] = i + 1

        # Score tasks
        results = []
        for t in validated_tasks:
            result = score_task(t, validated_tasks, strategy=strategy)
            combined = {**t, **result}
            results.append(combined)

        # Sort by score
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        return Response({
            "strategy": strategy,
            "tasks": results
        }, status=200)
