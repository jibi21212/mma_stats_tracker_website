from django.shortcuts import render, get_object_or_404
from .models import Event, Fight, Fighters, CareerStats, StrikeStats, FightPerformance, StrikeBreakdown, RoundStats

def home(request):
    query = request.GET.get('q')  # Get the search query from the search bar
    
    # If a search query is present, filter the fighters by name
    if query:
        fighters = Fighters.objects.filter(name__icontains=query)
    else:
        # If no search query, show all fighters (with pagination for performance)
        fighters = Fighters.objects.all()[:50]  # Limit to 50 for performance, you can paginate later
    
    # Retrieve corresponding stats for each fighter
    fighter_data = []
    for fighter in fighters:
        try:
            stats = CareerStats.objects.get(fighter=fighter)
        except CareerStats.DoesNotExist:
            stats = None
            
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

def fighter_profile(request, fighters_id):
    # Get the fighter by ID - using fighters_id which is your primary key
    fighter = get_object_or_404(Fighters, fighters_id=fighters_id)
    
    # Get fighter statistics
    try:
        fighter_stats = CareerStats.objects.get(fighter=fighter)
    except CareerStats.DoesNotExist:
        fighter_stats = None
    
    # Get all fight performances for this fighter
    fight_performances = FightPerformance.objects.filter(fighter=fighter)
    
    # Get the actual fights
    fights = []
    for performance in fight_performances:
        fight_data = {
            'fight': performance.fight,
            'result': performance.result,
            'opponent': None
        }
        
        # Try to find the opponent in this fight
        opponent_performance = FightPerformance.objects.filter(
            fight=performance.fight
        ).exclude(fighter=fighter).first()
        
        if opponent_performance:
            fight_data['opponent'] = opponent_performance.fighter
            
        fights.append(fight_data)
    
    # Pass the fighter, statistics, and fight history to the template
    context = {
        'fighter': fighter,
        'fighter_stats': fighter_stats,
        'fights': fights,
    }
    
    return render(request, 'fighter_profile.html', context)