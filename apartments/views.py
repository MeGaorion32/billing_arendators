from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from .models import Apartment
from .forms import ApartmentForm
from users.models import User

@login_required
def apartments_list(request):
    if request.user.is_admin:
        apartments = Apartment.objects.all()
    elif request.user.is_client:
        apartments = Apartment.objects.filter(owner=request.user)
    else:
        return redirect('forbidden')
    
    paginator = Paginator(apartments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'apartments/apartments_list.html', {
        'page_obj': page_obj
    })

@login_required
def create_apartment(request):
    if request.method == 'POST':
        form = ApartmentForm(request.POST, request=request)
        if form.is_valid():
            obj = form.save()
            messages.success(request, _('Объект успешно создан'))
            if request.user.is_admin:
                return redirect('admin_dashboard')
            else:
                return redirect('client_dashboard')
    else:
        form = ApartmentForm(request=request)
    
    return render(request, 'apartments/apartment_form.html', {
        'form': form,
        'title': _('Создание объекта')
    })

@login_required
def update_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    # Проверка прав доступа
    if not request.user.is_admin and apartment.owner != request.user:
        return redirect('forbidden')
    
    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apartment, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, _('Объект успешно обновлен'))
            if request.user.is_admin:
                return redirect('admin_dashboard')
            else:
                return redirect('client_dashboard')
    else:
        form = ApartmentForm(instance=apartment, request=request)
    
    return render(request, 'apartments/apartment_form.html', {
        'form': form,
        'title': _('Редактирование объекта')
    })

@login_required
def delete_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    # Проверка прав доступа
    if not request.user.is_admin and apartment.owner != request.user:
        return redirect('forbidden')
    
    if request.method == 'POST':
        apartment.delete()
        messages.success(request, _('Объект успешно удален'))
        if request.user.is_admin:
            return redirect('admin_dashboard')
        else:
            return redirect('client_dashboard')
    
    return render(request, 'apartments/apartment_confirm_delete.html', {
        'apartment': apartment
    })