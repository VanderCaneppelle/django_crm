from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from random import shuffle
from .forms import SignUpForm, AddRecordForm, TournamentForm, MatchScoreForm
from .models import Record, Tournament, Doubles, Match
from django.utils import timezone
from django.db.models.functions import Coalesce

# Create your views here.


def home(request):
    records = Record.objects.all()

    # check if user is logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been Logged In!')
            return redirect('home')
        else:
            messages.success(
                request, 'There was an error Logging In, please try again.')
            return redirect('home')
    else:
        return render(request, 'index.html', {'records': records})


# def login_user(request):
#     pass


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticated and log in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):

    if request.user.is_authenticated:
        # look up records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "You must be logged in to views that page")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:

        record = Record.objects.get(id=pk)
        first_name = record.first_name
        last_name = record.last_name

        record.delete()
        messages.success(
            request, f"{first_name} {last_name} Deleted Successfully!")
        return redirect('home')

    else:
        messages.error(request, "You must be logged in to delete a record!")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record added successfully!")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "You must be logged in to add records!")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated!")
            return redirect('home')
        return render(request, "update_record.html", {'form': form})
    else:
        messages.error(request, "You must be logged in to update a record!")
        return redirect('home')


def search_results(request):
    if request.method == "POST":
        searched = request.POST['searched']

        if not searched:
            messages.error(request, "No ID entered!")
            return redirect('home')

        records = Record.objects.filter(id=searched)
        if not records:
            messages.error(request, "No ID found!")
            return redirect('home')
        return render(request, "search_results.html", {'searched': searched, 'records': records})

    else:
        return render(request, "search_results.html", {})


def create_tournament(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TournamentForm(request.POST)
            if form.is_valid():
                # Create a new tournament instance but don't save it yet
                tournament = form.save(commit=False)

                tournament.save()

                # Now, we need to process the players field to get the selected players
                selected_players = form.cleaned_data['players']

                # Add the selected players to the tournament
                tournament.players.set(selected_players)

                # Save the tournament with the selected players
                tournament.save()

                messages.success(request, 'Tournament Created')

                # Redirect to the list of tournaments or wherever you want
                return redirect('tournament_list')
        else:
            form = TournamentForm()

        return render(request, 'create_tournament.html', {'form': form})
    else:
        messages.error(
            request, "You must be logged in access the tournament area")
        return redirect('home')


def tournament_list(request):
    if request.user.is_authenticated:
        tournaments = Tournament.objects.all()

        if not tournaments:
            messages.error(request, 'No Tournaments created')
            return redirect('create_tournament')
        else:
            return render(request, 'tournament_list.html', {'tournaments': tournaments})
    else:
        messages.error(request, 'You must be logged in see Tournaments')
        return redirect('home')


def view_tournament(request, pk):
    if request.user.is_authenticated:
        tournament = Tournament.objects.get(id=pk)
        return render(request, 'view_tournament.html', {'tournament': tournament})

    else:
        messages.error(request, 'You must be logged in see Tournaments')
        return redirect('home')


def delete_tournament(request, pk):
    if request.user.is_authenticated:

        tournament = Tournament.objects.get(id=pk)
        name = tournament.name
        tournament.delete()

        messages.success(
            request, f"{name} was deleted Successfully!")
        return redirect('tournament_list')

    else:
        messages.error(
            request, "You must be logged in to delete a Tournament!")
        return redirect('home')


def update_tournament(request, pk):
    if request.user.is_authenticated:
        current_tournament = Tournament.objects.get(id=pk)
        form = TournamentForm(request.POST or None,
                              instance=current_tournament)
        if form.is_valid():
            form.save()
            messages.success(request, "Tournament has been updated!")
            return redirect('tournament_list')
        return render(request, "update_tournament.html", {'form': form})
    else:
        messages.error(
            request, "You must be logged in to update a Tournament!")
        return redirect('home')


def create_teams(request, pk):
    if request.user.is_authenticated:
        tournament = Tournament.objects.get(id=pk)

        if not tournament.doubles.exists():
            players_D = tournament.players.filter(side='D')
            players_E = tournament.players.filter(side='E')

            # players_D = Record.objects.filter(side='D')
            # players_E = Record.objects.filter(side='E')

            if players_D.count() < 2 or players_E.count() < 2:
                messages.error(request, " There is not enough players.")
            else:
                shuffle(list(players_D))
                shuffle(list(players_E))

                for i in range(len(players_D)):
                    team_D = players_D[i]
                    team_E = players_E[i]
                    doubles_team = Doubles.objects.create(
                        player1=team_D, player2=team_E)
                    tournament.doubles.add(doubles_team)
                    messages.success(request, "Teams Created!")

        messages.success(request, "Teams were already created!")
        return redirect('view_tournament', pk=pk)

    else:
        messages.error(request, "You must be logged in to create teams!")
        return redirect('home')


def get_teams_data(request, pk):
    if request.user.is_authenticated:
        tournament = Tournament.objects.get(id=pk)
        doubles = tournament.doubles.all()

        data = []

        for double in doubles:
            data.append({
                "player1": double.player1.first_name + " " + double.player1.last_name,
                "player2": double.player2.first_name + " " + double.player2.last_name
            })

        return JsonResponse(data, safe=False)


def gen_1_phase_matches(request, pk):
    # Obtenha o torneio com base no ID (pk)
    tournament = get_object_or_404(Tournament, id=pk)

    # Obtenha todas as duplas associadas a este torneio
    doubles = Doubles.objects.filter(tournament=tournament)

    if tournament.matches.count() == 0:
        # Crie as partidas
        matches = []
        for i, team_a in enumerate(doubles):
            for team_b in doubles[i+1:]:
                # Crie a partida apenas se team_a e team_b forem diferentes
                match = Match.objects.create(
                    team_a=team_a, team_b=team_b, tournament=tournament, date=timezone.now())
                matches.append(match)
        # Redirecione de volta para a página do torneio com as partidas criadas
        return render(request, "first_phase_matches.html", {'tournament': tournament, 'matches': matches, 'doubles': doubles})

    else:
        # Recupere as partidas existentes
        matches = Match.objects.filter(tournament=tournament)
        messages.error(request, "Matches were already created!")
        return render(request, "first_phase_matches.html", {'tournament': tournament, 'matches': matches, 'doubles': doubles})


def _calculate_stats(result_a, result_b, team_a_id, team_b_id):

    pass


def save_match_scores(request, pk):
    # Obtenha o torneio com base no ID (pk)
    tournament = get_object_or_404(Tournament, id=pk)

    # Obtenha todas as partidas do torneio
    matches = Match.objects.filter(tournament=tournament)
    doubles = Doubles.objects.filter(tournament=tournament)

    if request.method == 'POST':
        form = MatchScoreForm(request.POST)
        if form.is_valid():
            # Processar o formulário e salvar as pontuações no banco de dados
            match_id = request.POST.get('match_id')  # Acesse o campo oculto
            result_a = form.cleaned_data['result_a']
            result_b = form.cleaned_data['result_b']

            match = Match.objects.get(pk=match_id)
            match.result_a = result_a
            match.result_b = result_b
            match.save()

            # adicionar total matches nas stats e fazer  verificação dos is none pelo numero de matches
            #
            for double in doubles:
                if match.team_a_id == double.id:
                    double.scored_points = Coalesce(
                        double.scored_points, 0) + result_a
                    double.conc_points = Coalesce(
                        double.conc_points, 0) + result_b

                    if result_a > result_b:
                        double.wins = Coalesce(double.wins, 0) + 1
                    else:
                        double.defeats = Coalesce(double.defeats, 0) + 1

                if match.team_b_id == double.id:
                    double.scored_points = Coalesce(
                        double.scored_points, 0) + result_b
                    double.conc_points = Coalesce(
                        double.conc_points, 0) + result_a

                    if result_b > result_a:
                        double.wins = Coalesce(double.wins, 0) + 1
                    else:
                        double.defeats = Coalesce(double.defeats, 0) + 1

                double.save()

            initial_results = {}  # Use um dicionário para mapear match_id para resultados
            for match in matches:
                initial_results[f'result_a_{match.id}'] = match.result_a
                initial_results[f'result_b_{match.id}'] = match.result_b

            form = MatchScoreForm(initial=initial_results)

    else:
        form = MatchScoreForm()

    return render(request, 'first_phase_matches.html', {'tournament': tournament, 'matches': matches, 'form': form})


def get_tournament_ranking(request, pk):

    tournament = get_object_or_404(Tournament, id=pk)

    # Obtenha todas as partidas do torneio
    matches = Match.objects.filter(tournament=tournament)
    doubles = Doubles.objects.filter(
        tournament=tournament).order_by('wins', 'balance', 'scored_points').reverse

    return render(request, 'get_tournament_ranking.html', {'doubles': doubles, 'matches': matches, 'tournament': tournament})
