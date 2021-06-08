from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from .models import ChatData


@login_required
def course_chat_room(request, course_id):
    try:
        course = request.user.courses_joined.get(id=course_id)
        room_name = f'chat_{course_id}'
        msg = ChatData.objects.filter(room_name=room_name)
    except:
        return HttpResponseForbidden()
    return render(request, 'chat/room.html', {'course': course, 'msg': msg})


