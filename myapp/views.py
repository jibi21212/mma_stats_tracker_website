from django.shortcuts import render
from .models import Fighter, FighterStats

def home(request):
    query = request.GET.get('q')  # Get the search query from the search bar
    fighters = []

    if query:
        # If a search query is present, filter the fighters by name
        fighters = Fighter.objects.filter(name__icontains=query)  # Case-insensitive search

    # Retrieve corresponding stats for each fighter
    fighter_data = []
    for fighter in fighters:
        try:
            stats = FighterStats.objects.get(fighter=fighter)  # Get stats related to the fighter
        except FighterStats.DoesNotExist:
            stats = None  # If no stats available, set to None

        fighter_data.append({
            'fighter': fighter,
            'stats': stats,
        })

    # Pass the query and fighters with their stats to the template
    return render(request, "home.html", {"query": query, "fighter_data": fighter_data})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

from django.shortcuts import render, get_object_or_404
from .models import Fighter, FighterStats, Bout

def fighter_profile(request, fighter_id):
    # Get the fighter by ID
    fighter = get_object_or_404(Fighter, id=fighter_id)

    # Get fighter statistics
    fighter_stats = FighterStats.objects.filter(fighter=fighter).first()

    # Get all bouts where this fighter was involved
    bouts_as_fighter_1 = Bout.objects.filter(fighter_1=fighter)
    bouts_as_fighter_2 = Bout.objects.filter(fighter_2=fighter)

    # Combine all bouts involving this fighter
    bout_history = bouts_as_fighter_1.union(bouts_as_fighter_2)

    # Pass the fighter, statistics, and bout history to the template
    context = {
        'fighter': fighter,
        'fighter_stats': fighter_stats,
        'bout_history': bout_history,
    }

    return render(request, 'fighter_profile.html', context)
