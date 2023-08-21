from django.shortcuts import render
from .models import UserChatRoom, UserChatMessages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
import json
from base.utils import get_page_obj, page_serializer


@login_required
def chats(request):
    users = User.objects.all()
    return render(request, 'chat/chats.html', {'users': users})


def mark_as_read(request):
    # if request.method == 'POST':
    #     data = json.loads(request.body)
    #     # room_id = data.get('room_id', None)
    #     messagesIds = data.get('messagesIds', None)
    #     user = data.get('user', None)
    #     user = User.objects.get(username=user)
    #     for messId in messagesIds:
    #         mess_obj = UserChatMessages.objects.get(id=messId)
    #         mess_obj.seen_by.add(user)
    return JsonResponse({'ok': "ok"})


def get_messages(request, room):
    print('heheh'*150)
    is_json = request.GET.get('is_json', False)
    messages_qs = UserChatMessages.objects.filter(
        room=room).order_by('-id')
    message_pages_obj = get_page_obj(request, messages_qs)
    if is_json:
        page = page_serializer(message_pages_obj, 'messages')
        return JsonResponse({'messages': page})
    page = page_serializer(message_pages_obj, 'messages')
    return page


@login_required
def chat(request, created_with, created_by):
    created_with = User.objects.get(username=created_with)
    created_by = User.objects.get(username=created_by)
    all_users = User.objects.all()
    room_name = created_with.username + '/' + created_by.username
    reverse_room_name = created_by.username + '/' + created_with.username
    user_room = UserChatRoom.objects.filter(Q(
        name=room_name
    )).first()
    if not user_room:
        user_room = UserChatRoom.objects.filter(Q(
            name=reverse_room_name
        )).first()
    if not user_room:
        user_room = UserChatRoom.objects.create(
            name=room_name,
            slug=room_name.lower(),
            created_by=created_by,
            # created_with=created_with,
            reverse_name=reverse_room_name
        )
        user_room.users.add(created_with)
        user_room.users.add(created_by)
    message_pages = get_messages(request, user_room)

    users_in_room = user_room.users.all()
    context = {'room': user_room, 'messages': message_pages,
               'users_in_room': users_in_room, 'users': all_users}
    return render(request, 'chat/chat.html', context)




















