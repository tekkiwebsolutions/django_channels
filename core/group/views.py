from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import json
from chat.models import UserChatMessages, UserChatRoom
from base.utils import get_page_obj, page_serializer
from django.http import JsonResponse


def groups(request):
    all_users = User.objects.exclude(username=request.user.username)
    prev_groups = request.user.chat_rooms.all().exclude(is_group=False)
    print('prev', prev_groups)
    context = {'users': all_users, 'errors': None, 'prev_groups': prev_groups}
    if request.method == 'POST':
        group_name = request.POST.get('group-name', None)
        added_users = request.POST.get('added-users-list', None)
        added_users = json.loads(added_users)
        group_room_obj = UserChatRoom.objects.filter(name=group_name).first()
        if group_room_obj:
            errors = ['group with same name already exists']
            context['errors'] = errors
            return render(request, 'group/groups.html', context)

        group_room_obj = UserChatRoom.objects.create(
            name=group_name, slug=group_name.lower(),
            reverse_name=group_name, created_by=request.user,
            is_group=True
        )
        group_room_obj.users.add(request.user)
        for username in added_users:
            user = User.objects.get(username=username)
            group_room_obj.users.add(user)

        return redirect('group_chat', group_name=group_room_obj.name)
    return render(request, 'group/groups.html', context)


def get_messages(request, room):
    print('5%'*200)
    is_json = request.GET.get('is_json', False)
    messages_qs = UserChatMessages.objects.filter(
        room=room).order_by('-id')
    message_pages_obj = get_page_obj(request, messages_qs)
    if is_json:
        page = page_serializer(message_pages_obj, 'messages')
        return JsonResponse({'messages': page})
    page = page_serializer(message_pages_obj, 'messages')
    return page


def group(request, group_name):
    all_users = User.objects.all()
    print('groooo'*150, group_name)
    group_room_obj = UserChatRoom.objects.get(name=group_name)
    message_pages = get_messages(request, group_room_obj)
    context = {'group': group_room_obj}
    context = {'room': group_room_obj, 'messages': message_pages,
               'users_in_room': group_room_obj.users.all().values('username'), 
               'users': all_users}
    return render(request, 'group/group.html', context)
