from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from .models import Apartment
from .forms import ApartmentForm
from users.models import User
from communal_services.models import CommunalServiceType

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
            try:
                apartment = form.save(commit=False)
                apartment.save()
                
                # Получаем очищенные данные из формы
                type_ids = form.cleaned_data['selected_types']
                if type_ids:
                    apartment.update_communal_service_types(type_ids)
                
                messages.success(request, _('Объект успешно создан'))
                # return redirect('apartments:apartments_list')
                if request.user.is_admin:
                    return redirect('admin_dashboard')
                else:
                    return redirect('client_dashboard')
            except Exception as e:
                messages.error(request, _('Ошибка при сохранении: ') + str(e))
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            messages.error(request, _('Ошибки в форме: ') + ', '.join(error_messages))
    else:
        form = ApartmentForm(request=request)
    
    from communal_services.models import CommunalService
    communal_services = CommunalService.objects.prefetch_related('types').all()
    
    return render(request, 'apartments/apartment_form.html', {
        'form': form,
        'title': _('Создание объекта'),
        'communal_services': communal_services,
        'selected_types': []
    })

# apartments/views.py
@login_required
def update_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if not request.user.is_admin and apartment.owner != request.user:
        return redirect('forbidden')
    
    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apartment, request=request)
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.save()
            
            # Получаем очищенные данные из формы
            type_ids = form.cleaned_data['selected_types']
            apartment.update_communal_service_types(type_ids)
            
            messages.success(request, _('Объект успешно обновлен'))
            # return redirect('apartments:apartments_list')
            if request.user.is_admin:
                return redirect('admin_dashboard')
            else:
                return redirect('client_dashboard')
    else:
        form = ApartmentForm(instance=apartment, request=request)
    
    from communal_services.models import CommunalService
    communal_services = CommunalService.objects.prefetch_related('types').all()
    
    return render(request, 'apartments/apartment_form.html', {
        'form': form,
        'title': _('Редактирование объекта'),
        'communal_services': communal_services,
        'selected_types': apartment.communal_service_types.all()
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