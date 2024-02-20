from django.shortcuts import render, redirect
from TSG.models import Tsg, Notification, Announcement, Flat
from django.contrib.auth.decorators import login_required
from TSG.forms import NotificationForm, AnnouncementForm, CreationForm
from django.db.models import Q
from django.views.generic import CreateView
from django.urls import reverse_lazy


@login_required
def tsg(request):
    print(Notification.objects.filter(
        (Q(users_viewed=request.user) | Q(users_viewed__isnull=True)) & Q(recipients__id=1)
    ).order_by('-creation_date').values('creation_date', 'theme', 'users_viewed'))

    return_set = set(Tsg.objects.filter(chairman=request.user))
    for flat in request.user.flat_set.all().select_related('entrance__house__TSG'):
        return_set.add(flat.entrance.house.TSG)
    if len(return_set) == 1:
        return redirect("tsg", return_set.pop().id)
    return render(request, 'tsg/tsg_list.html', context={'tsg_list': return_set})


# Create your views here.

@login_required
def tsg_detail(request, pk):
    tsg_item = Tsg.objects.select_related('chairman').get(pk=pk)
    tsg_name = tsg_item.name
    chairman_flag = tsg_item.chairman == request.user
    flat_list = request.user.flat_set.all().filter(entrance__house__TSG__id=pk)
    if not (flat_list or chairman_flag):
        return redirect('tsg_list')
    return render(
        request,
        'tsg/tsg_details.html',
        context={'tsg_name': tsg_name, 'chairman_flag': chairman_flag, 'flat_list': flat_list}
    )


@login_required
def manage(request, tsg_pk):
    if Tsg.objects.get(pk=tsg_pk).chairman != request.user:
        return redirect('tsg', tsg_pk)
    return render(
        request,
        'tsg/tsg_manage.html',
        context={'tsg_pk': tsg_pk}
    )


@login_required
def create_notification(request, tsg_pk):
    if Tsg.objects.get(pk=tsg_pk).chairman != request.user:
        return redirect('tsg', tsg_pk)
    tsg_obj = Tsg.objects.filter(pk=tsg_pk).prefetch_related('house_set__entrance_set__flat_set').get()
    if request.method == 'POST':
        form = NotificationForm(tsg_obj, request.POST)
        if form.is_valid():
            form.save()
            return redirect('tsg_manage', tsg_pk)

    else:
        form = NotificationForm(tsg_obj)
    return render(request, 'tsg/create_form.html', {'form': form})


@login_required
def create_announcement(request, tsg_pk):
    tsg_obj = Tsg.objects.get(pk=tsg_pk)
    if tsg_obj.chairman != request.user:
        return redirect('tsg', tsg_pk)
    if request.method == 'POST':
        form = AnnouncementForm(tsg_obj, request.POST)
        if form.is_valid():
            form.save()
            return redirect('tsg_manage', tsg_pk)

    else:
        form = AnnouncementForm(tsg_obj)
    return render(request, 'tsg/create_form.html', {'form': form})


@login_required
def announcement_list(request, tsg_pk):
    tsg_item = Tsg.objects.select_related('chairman').get(pk=tsg_pk)
    chairman_flag = tsg_item.chairman == request.user
    flat_list = request.user.flat_set.all().filter(entrance__house__TSG__id=tsg_pk)
    if not (flat_list or chairman_flag):
        return redirect('tsg_list')
    announcements = Announcement.objects.filter(
        (Q(users_viewed=request.user) | Q(users_viewed__isnull=True)) & Q(tsg_id=tsg_pk)
    ).order_by('-creation_date')
    creation_link = tsg_item.get_announcement_creation_link()
    creation_text = Announcement.get_creation_text()
    list_header = Announcement.get_list_header()
    return render(
        request,
        'tsg/date_theme_is_viewed_list.html',
        {'list_header': list_header, 'list': announcements, 'is_chairman': chairman_flag,
         'creation_text': creation_text, 'creation_link': creation_link}
    )


@login_required
def notification_tsg_list(request, tsg_pk):
    tsg_item = Tsg.objects.select_related('chairman').get(pk=tsg_pk)
    chairman_flag = tsg_item.chairman == request.user
    if not chairman_flag:
        return redirect('tsg_list')
    notifications = Notification.objects.filter(
        (Q(users_viewed=request.user) | Q(users_viewed__isnull=True)) & Q(tsg_id=tsg_pk)
    ).order_by('-creation_date')
    creation_link = tsg_item.get_notification_creation_link()
    creation_text = Notification.get_creation_text()
    list_header = Notification.get_list_header()
    return render(
        request,
        'tsg/notification_tsg_list.html',
        {'list_header': list_header, 'list': notifications, 'is_chairman': chairman_flag,
         'creation_text': creation_text, 'creation_link': creation_link, }
    )


@login_required
def notification_flat_list(request, flat_pk):
    flat = request.user.flat_set.all().filter(id=flat_pk)
    if not flat:
        return redirect('tsg')
    notifications = Notification.objects.filter(
        (Q(users_viewed=request.user) | Q(users_viewed__isnull=True)) & Q(recipients__id=flat_pk)
    ).order_by('-creation_date')
    list_header = Notification.get_list_header()
    return render(
        request,
        'tsg/notification_flat_list.html',
        {'list_header': list_header, 'list': notifications, 'flat_pk': flat_pk, }
    )


@login_required
def announcement_detail(request, tsg_pk, announcement_pk):
    tsg_item = Tsg.objects.select_related('chairman').get(pk=tsg_pk)
    chairman_flag = tsg_item.chairman == request.user
    flat_list = request.user.flat_set.all().filter(entrance__house__TSG__id=tsg_pk)
    if not (flat_list or chairman_flag):
        return redirect('tsg_list')
    announcement = Announcement.objects.filter(pk=announcement_pk, tsg_id=tsg_pk)
    if not announcement:
        return redirect('announcement_list', tsg_pk)
    announcement = announcement.get()
    announcement.users_viewed.add(request.user)
    announcement.save()
    return render(request, 'tsg/announcement.html', {'announcement': announcement, 'is_chairman': chairman_flag})


@login_required
def announcement_delete(request, tsg_pk, announcement_pk):
    tsg_item = Tsg.objects.select_related('chairman').get(pk=tsg_pk)
    chairman_flag = tsg_item.chairman == request.user
    if not chairman_flag:
        return redirect('announcement_list', tsg_pk)
    announcement = Announcement.objects.filter(pk=announcement_pk, tsg_id=tsg_pk).get()
    if not announcement:
        return redirect('announcement_list', tsg_pk)
    announcement.delete()
    return redirect('announcement_list', tsg_pk)


@login_required
def notification_detail(request, notification_pk, tsg_pk=None, flat_pk=None):
    chairman_flag = None
    flat_list = None
    notification = None
    if tsg_pk:
        tsg_item = Tsg.objects.select_related('chairman').get(pk=tsg_pk)
        chairman_flag = tsg_item.chairman == request.user
        notification = Notification.objects.filter(pk=notification_pk, tsg_id=tsg_pk)
    if flat_pk:
        flat_list = request.user.flat_set.all().filter(id=flat_pk)
        notification = Notification.objects.filter(pk=notification_pk, recipients__id=flat_pk).select_related('section')
    if not ((flat_list or chairman_flag) and notification):
        return redirect('tsg_list')
    notification_values = notification.values('section__name', 'theme', 'text', 'creation_date', 'id').get()
    notification = notification.get()
    notification.users_viewed.add(request.user)
    notification.save()
    return render(
        request,
        'tsg/notification.html',
        {'notification': notification_values, 'is_chairman': chairman_flag}
    )


@login_required
def notification_delete(request, tsg_pk, notification_pk):
    tsg_item = Tsg.objects.select_related('chairman').get(pk=tsg_pk)
    chairman_flag = tsg_item.chairman == request.user
    if not chairman_flag:
        return redirect('notification_tsg_list', tsg_pk)
    notification = Notification.objects.filter(pk=notification_pk, tsg_id=tsg_pk).get()
    if not notification:
        return redirect('notification_tsg_list', tsg_pk)
    notification.delete()
    return redirect('notification_tsg_list', tsg_pk)


@login_required
def flat_list(request, tsg_pk):
    tsg_item = Tsg.objects.select_related('chairman').get(pk=tsg_pk)
    chairman_flag = tsg_item.chairman == request.user
    if not chairman_flag:
        return redirect('tsg', tsg_pk)
    flat_list_var = Flat.objects.filter(entrance__house__TSG_id=tsg_pk).select_related('entrance__house')\
        .select_related("main_user")
    return render(
        request,
        'tsg/flat_list.html',
        {'flat_list': flat_list_var, 'tsg_name': tsg_item.name}
    )


class Register(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
