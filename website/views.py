from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, TournamentForm
from .models import Record, Tournament

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
        return render(request, "create_tournament.html", {})

    else:
        messages.error(
            request, "You must be logged in access the tournament area")
        return redirect('home')


def create_tournament(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TournamentForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tournament Created')

                # Redirecionar para a lista de torneios
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


def customer_record(request, pk):

    if request.user.is_authenticated:
        # look up records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "You must be logged in to views that page")
        return redirect('home')
