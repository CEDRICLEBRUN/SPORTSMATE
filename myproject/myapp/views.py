from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .forms import SignUpForm, UserUpdateForm, EventForm, MessageForm
from .models import Event, Conversation

def home(request):
    return render(request, 'index.html')

def main(request):
    return render(request, 'main.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Charger le profil automatiquement
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def account(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Compte mis à jour !')
            return redirect('account')  # Redirige vers la page du compte après la mise à jour
    else:
        user_form = UserUpdateForm(instance=request.user)

    context = {
        'user_form': user_form,
    }
    return render(request, 'registration/account.html', context)

@login_required
def event_list(request):
    title = request.GET.get('t', '')
    city = request.GET.get('c', '')
    if title:
        events = Event.objects.filter((Q(name__icontains=title) | Q(sport__icontains=title)), date__gte=timezone.now()).order_by('date')
    elif city:
        events = Event.objects.filter(Q(city__icontains=city), date__gte=timezone.now()).order_by('date')
    else:
        events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'events/event_list.html', {'events': events, 'title': title})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = event.participants.all()

    if event.available_places > 0 and request.user != event.owner and request.user not in participants:
        join_event = True
    else:
        join_event = False

    return render(request, 'events/event_detail.html', {'event': event, 'participants': participants, 'join_event': join_event })

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.available_places = request.POST.get('participants_number')
            try:
                event.save()
                return redirect('my_events')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def my_events(request):
    user = request.user
    filter_type = request.GET.get('filter', 'upcoming')

    if filter_type == 'past':
        events = Event.objects.filter(owner=request.user, date__lt=timezone.now()).order_by('date') | user.events_joined.filter(date__lt=timezone.now()).order_by('date')
    else: 
        events = Event.objects.filter(owner=request.user, date__gte=timezone.now()).order_by('date') | user.events_joined.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'events/my_events.html', {'events': events, 'filter_type': filter_type})

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user == event.owner:
        messages.error(request, "Vous ne pouvez pas rejoindre votre événement.")
        return redirect('event_list')
    if request.user not in event.participants.all():
        if event.still_available:
            event.new_participant(request.user)
            event.save()
            # Ajouter un message de succès ici si nécessaire
        else:
            messages.error(request, "Plus de place disponible.")
    return redirect('event_list')

@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participant1=request.user) | Conversation.objects.filter(participant2=request.user)
    conversation_data = []
    for conversation in conversations:
        if conversation.participant1 == request.user:
            other_participant = conversation.participant2
        else:
            other_participant = conversation.participant1
        conversation_data.append({
            'conversation': conversation,
            'messages': conversation.messages.all(),
            'other_participant': other_participant,
        })
    return render(request, 'messaging/conversation_list.html', {'conversation_data': conversation_data})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user != conversation.participant1 and request.user != conversation.participant2:
        return redirect('conversation_list')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('conversation_detail', conversation_id=conversation_id)
    else:
        form = MessageForm()
    
    messages = conversation.messages.all().order_by('timestamp')
    other_participant = conversation.participant1 if request.user != conversation.participant1 else conversation.participant2
    return render(request, 'messaging/conversation_detail.html', {'conversation': conversation, 'form': form, 'messages': messages, 'other_participant': other_participant})

@login_required
def start_conversation(request, user_id=None):
    if request.method == 'POST':
        other_user_id = request.POST.get('other_user_id')
        other_user = get_object_or_404(User, id=other_user_id)
        if other_user == request.user:
            return redirect('conversation_list')
        
        conversation = Conversation.objects.filter(participant1=request.user, participant2=other_user) | \
                       Conversation.objects.filter(participant1=other_user, participant2=request.user)
        
        if conversation.exists():
            conversation = conversation.first()
        else:
            conversation = Conversation.objects.create(participant1=request.user, participant2=other_user)
        
        return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'messaging/start_conversation.html', {'users': users})