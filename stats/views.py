from django.shortcuts import render, redirect
from stats.utils import *


def homepage(request):
    user = request.user

    if user.is_anonymous:
        return redirect("/login")

    data = get_user_display_data(user)
    if request.method == "POST":
        if "am_i_healthy" in request.POST:
            prompt = generate_prompt("am_i_healthy", data)
            response = generate_response(prompt)
            data['textResponse']['am_i_healthy'] = response
        if "how_was_my_day" in request.POST:
            prompt = generate_prompt("how_was_my_day", data)
            response = generate_response(prompt)
            data['textResponse']['how_was_my_day'] = response
        if "increase_water" in request.POST:
            entry = UserDailyStats.objects.get(user=user, date=timezone.now())
            entry.water += 250
            entry.save()
            return redirect("/")
    return render(request, "stats/stats.html", data)
