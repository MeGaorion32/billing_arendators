from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from .models import User
from apartments.models import Apartment

def admin_check(user):
    return user.is_admin

def client_check(user):
    return user.is_client

def renter_check(user):
    return user.is_renter

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_admin:
                    return redirect('admin_dashboard')
                elif user.is_client:
                    return redirect('client_dashboard')
                elif user.is_renter:
                    return redirect('renter_dashboard')
            else:
                form.add_error(None, _('Неверный email или пароль'))
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(admin_check, login_url='/forbidden/')
def admin_dashboard(request):
    users = User.objects.all()
    apartments = Apartment.objects.all()
    
    user_paginator = Paginator(users, 5)
    user_page_number = request.GET.get('user_page')
    user_page_obj = user_paginator.get_page(user_page_number)
    
    apartment_paginator = Paginator(apartments, 5)
    apartment_page_number = request.GET.get('object_page')
    apartment_page_obj = apartment_paginator.get_page(apartment_page_number)
    
    return render(request, 'users/admin_dashboard.html', {
        'user_page_obj': user_page_obj,
        'apartment_page_obj': apartment_page_obj
    })

@login_required
@user_passes_test(client_check, login_url='/forbidden/')
def client_dashboard(request):
    # Показываем только арендаторов, привязанных к объектам клиента
    renters = User.objects.filter(
        role=User.Role.RENTER,
        rented_apartments__owner=request.user
    ).distinct()
    
    # Исправленный запрос для объектов клиента
    apartments = Apartment.objects.filter(owner=request.user)
    
    # Пагинация для арендаторов
    user_paginator = Paginator(renters, 5)
    user_page_number = request.GET.get('user_page', 1)
    user_page_obj = user_paginator.get_page(user_page_number)
    
    # Пагинация для объектов
    apartment_paginator = Paginator(apartments, 5)
    apartment_page_number = request.GET.get('apartment_page', 1)
    apartment_page_obj = apartment_paginator.get_page(apartment_page_number)
    
    return render(request, 'users/client_dashboard.html', {
        'user_page_obj': user_page_obj,
        'apartments_page_obj': apartment_page_obj
    })

@login_required
@user_passes_test(renter_check, login_url='/forbidden/')
def renter_dashboard(request):
    return render(request, 'users/renter_dashboard.html')

@login_required
def create_user(request):
    if not (request.user.is_admin or request.user.is_client):
        return redirect('forbidden')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request=request)
        if form.is_valid():
            user = form.save(commit=False)
            
            if request.user.is_client:
                user.role = User.Role.RENTER
            
            user.save()
            
            # Если это клиент, привязываем выбранные объекты к арендатору
            if request.user.is_client and 'apartments' in form.cleaned_data:
                apartments = form.cleaned_data['apartments']
                for apartment in apartments:
                    apartment.renter = user
                    apartment.save()
            
            messages.success(request, _('Пользователь {} успешно создан').format(user.email))
            if request.user.is_admin:
                return redirect('admin_dashboard')
            else:
                return redirect('client_dashboard')
    else:
        form = UserRegisterForm(request=request)
    
    return render(request, 'users/create_user.html', {'form': form})

# @login_required
# def update_user(request, pk):
#     user = get_object_or_404(User, pk=pk)
    
#     # Проверка прав доступа
#     if not (request.user.is_admin or (request.user.is_client and user.is_renter)):
#         return redirect('forbidden')
    
#     if request.method == 'POST':
#         form = UserUpdateForm(request.POST, instance=user, request=request)
#         if form.is_valid():
#             # Сохраняем пользователя
#             updated_user = form.save()
            
#             # Если это админ и он изменил роль с арендатора на другую
#             if request.user.is_admin and user.is_renter and updated_user.role != User.Role.RENTER:
#                 # Отвязываем все объекты
#                 Apartment.objects.filter(renter=user).update(renter=None)
#             # Если это админ или клиент и редактируется арендатор
#             elif (request.user.is_admin or request.user.is_client) and updated_user.is_renter and 'apartments' in form.cleaned_data:
#                 # Сначала отвязываем все объекты от этого арендатора
#                 Apartment.objects.filter(renter=user).update(renter=None)
                
#                 # Привязываем выбранные объекты
#                 apartments = form.cleaned_data['apartments']
#                 for apartment in apartments:
#                     apartment.renter = user
#                     apartment.save()
            
#             messages.success(request, _('Пользователь успешно обновлен'))
#             if request.user.is_admin:
#                 return redirect('admin_dashboard')
#             else:
#                 return redirect('client_dashboard')
#     else:
#         form = UserUpdateForm(instance=user, request=request)
    
#     return render(request, 'users/update_user.html', {
#         'form': form,
#         'user': user
#     })

# В функции update_view заменим:
@login_required
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    changed_user = request.user
    print('user', user)
    print('changed_user', changed_user)
    is_admin = request.user.is_admin
    
    # Проверка прав доступа
    # if not (is_admin or (request.user.is_client and user.is_renter)):
    if not (is_admin or request.user.is_client):

        return redirect('forbidden')

    if request.method == 'POST':
        form = UserUpdateForm(
            request.POST, 
            instance=user, 
            request=request,
            is_admin=is_admin
        )
        print('form', form)
        if form.is_valid():
            # Если пользователь не админ — сохраняем роль как у оригинального пользователя
            if not is_admin:
                form.instance.role = user.role
            updated_user = form.save()
            
            # Обработка объектов для арендаторов
            if updated_user.is_renter and 'apartments' in form.cleaned_data:
                # Отвязываем все объекты
                Apartment.objects.filter(renter=updated_user).update(renter=None)
                # Привязываем выбранные
                for apartment in form.cleaned_data['apartments']:
                    apartment.renter = updated_user
                    apartment.save()
            
            messages.success(request, _('Изменения сохранены'))
            return redirect('admin_dashboard' if is_admin else 'client_dashboard')
    else:
        form = UserUpdateForm(
            instance=user, 
            request=request,
            is_admin=is_admin
        )
    
    return render(request, 'users/update_user.html', {
        'form': form,
        'user': user,
        'is_admin': is_admin,
        'is_client': request.user.is_client
    })

@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Проверка прав доступа
    if not (request.user.is_admin or (request.user.is_client and user.is_renter)):
        return redirect('forbidden')
    
    if request.method == 'POST':
        # Отвязываем все объекты от этого пользователя перед удалением
        Apartment.objects.filter(renter=user).update(renter=None)
        user.delete()
        messages.success(request, _('Пользователь успешно удален'))
        if request.user.is_admin:
            return redirect('admin_dashboard')
        else:
            return redirect('client_dashboard')
    
    return render(request, 'users/user_confirm_delete.html', {
        'user': user
    })

def forbidden_view(request):
    return HttpResponseForbidden(_("У вас нет прав доступа к этой странице"))