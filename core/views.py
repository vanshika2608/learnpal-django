from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from .recommender import get_recommendations

from .forms import LearningGoalForm, ResourceForm
from .models import LearningGoal, Resource


# ----- Dashboard -----
def dashboard(request):
    goals = LearningGoal.objects.all()

    # Stats
    total = goals.count()
    completed = goals.filter(status=LearningGoal.DONE).count()
    in_progress = goals.filter(status=LearningGoal.IN_PROGRESS).count()
    not_started = goals.filter(status=LearningGoal.NOT_STARTED).count()
    avg_progress = goals.aggregate(p=Avg("progress"))["p"] or 0

    # Upcoming due (next 7 days)
    today = timezone.now().date()
    upcoming = goals.filter(
        due_date__isnull=False,
        due_date__gte=today,
        due_date__lte=today + timedelta(days=7)
    ).order_by("due_date")[:5]

    # ----- Recommendations -----
    recommended = []
    if goals.exists():
        # Combine all goal titles + descriptions for better recommendations
        user_input = " ".join(
            [goal.title + " " + (goal.description or "") + " " + (goal.tags or "") for goal in goals]
        ).strip()

        if user_input:
            try:
                recommended = get_recommendations(user_input)
            except Exception as e:
                messages.warning(request, f"⚠️ Recommendation system error: {str(e)}")
        else:
            messages.info(request, "Add a goal description for better recommendations.")
    else:
        messages.info(request, "Add some goals to get personalized recommendations!")

    context = {
        "stats": {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "not_started": not_started,
            "avg_progress": round(avg_progress, 1),
        },
        "upcoming": upcoming,
        "goals": goals,
        "recommended": recommended,
    }

    return render(request, "core/dashboard.html", context)


# ----- Goals (list + create) -----
def goals_home(request):
    if request.method == "POST":
        form = LearningGoalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Goal added successfully!")
            return redirect("goals_home")
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = LearningGoalForm()

    goals = LearningGoal.objects.all()
    return render(request, "core/home.html", {"form": form, "goals": goals})


def edit_goal(request, goal_id):
    goal = get_object_or_404(LearningGoal, id=goal_id)
    if request.method == "POST":
        form = LearningGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Goal updated successfully!")
            return redirect("goals_home")
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = LearningGoalForm(instance=goal)
    return render(request, "core/edit.html", {"form": form, "goal": goal})


def delete_goal(request, goal_id):
    goal = get_object_or_404(LearningGoal, id=goal_id)
    goal.delete()
    messages.success(request, "🗑️ Goal deleted successfully!")
    return redirect("goals_home")


# ----- Resources -----
def resources_list(request):
    resources = Resource.objects.select_related("goal").all()
    form = ResourceForm()
    return render(request, "core/resources.html", {"resources": resources, "form": form})


def add_resource(request):
    if request.method == "POST":
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "📚 Resource added successfully!")
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
        return redirect("resources")
    return redirect("resources")
