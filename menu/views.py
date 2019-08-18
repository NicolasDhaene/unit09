from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from datetime import datetime, timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *
from django.db.models import Q


def menu_list(request):
    all_menus = Menu.objects.all().prefetch_related('items')
    query = Q(expiration_date__gte=timezone.now()) | Q(expiration_date__isnull=True)
    menus = all_menus.filter(query).order_by('-expiration_date')
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try: 
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            menu.created_date = timezone.now()
            menu.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_new.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            menu = form.save()
            menu.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu/change_menu.html', {'form': form})
