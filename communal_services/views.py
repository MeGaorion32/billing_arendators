from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import CommunalService, CommunalServiceType
from .forms import CommunalServiceForm, CommunalServiceTypeForm

# Коммунальные услуги
@login_required
def service_list(request):
    services = CommunalService.objects.all()
    return render(request, 'communal_services/service_list.html', {
        'services': services
    })

@login_required
def service_create(request):
    if request.method == 'POST':
        form = CommunalServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Коммунальная услуга успешно создана'))
            return redirect('communal_services:service_list')
    else:
        form = CommunalServiceForm()
    
    return render(request, 'communal_services/service_form.html', {
        'form': form,
        'title': _('Создание коммунальной услуги')
    })

@login_required
def service_edit(request, pk):
    service = get_object_or_404(CommunalService, pk=pk)
    
    if request.method == 'POST':
        form = CommunalServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, _('Коммунальная услуга успешно обновлена'))
            return redirect('communal_services:service_list')
    else:
        form = CommunalServiceForm(instance=service)
    
    return render(request, 'communal_services/service_edit.html', {
        'form': form,
        'title': _('Редактирование коммунальной услуги'),
        'service': service
    })

@login_required
def service_delete(request, pk):
    service = get_object_or_404(CommunalService, pk=pk)
    
    if request.method == 'POST':
        service.delete()
        messages.success(request, _('Коммунальная услуга успешно удалена'))
        return redirect('communal_services:service_list')
    
    return render(request, 'communal_services/service_confirm_delete.html', {
        'service': service
    })

# Типы коммунальных услуг
@login_required
def service_type_create(request, service_pk):
    service = get_object_or_404(CommunalService, pk=service_pk)
    
    if request.method == 'POST':
        form = CommunalServiceTypeForm(request.POST, communal_service=service)
        if form.is_valid():
            try:
                type_instance = form.save(commit=False)
                type_instance.communal_service = service
                
                if type_instance.had_parent and type_instance.parent_type:
                    parent = type_instance.parent_type
                    # Сохраняем тарифы из формы, даже если они есть у родителя
                    type_instance.tariff_1 = form.cleaned_data.get('tariff_1', parent.tariff_1)
                    type_instance.tariff_2 = form.cleaned_data.get('tariff_2', parent.tariff_2)
                    type_instance.tariff_3 = form.cleaned_data.get('tariff_3', parent.tariff_3)
                    type_instance.default_tariff = form.cleaned_data.get('default_tariff', parent.default_tariff)
                
                type_instance.save()
                messages.success(request, _('Тип услуги успешно создан'))
                return redirect('communal_services:service_edit', pk=service.pk)
            except Exception as e:
                messages.error(request, _('Ошибка при сохранении типа услуги: ') + str(e))
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            messages.error(request, _('Ошибки в форме: ') + ', '.join(error_messages))
    else:
        form = CommunalServiceTypeForm(communal_service=service)
    
    return render(request, 'communal_services/service_type_form.html', {
        'form': form,
        'service': service,
        'title': _('Создание типа услуги')
    })

@login_required
def service_type_edit(request, service_pk, pk):
    service = get_object_or_404(CommunalService, pk=service_pk)
    service_type = get_object_or_404(CommunalServiceType, pk=pk)
    
    if request.method == 'POST':
        form = CommunalServiceTypeForm(
            request.POST, 
            instance=service_type,
            communal_service=service
        )
        if form.is_valid():
            type_instance = form.save(commit=False)
            
            # Для всех типов сохраняем default_tariff
            type_instance.default_tariff = form.cleaned_data.get('default_tariff', '')
            
            # Сохраняем тарифы в зависимости от типа
            if type_instance.division_by_tariff:
                type_instance.tariff_1 = form.cleaned_data.get('tariff_1', '')
                type_instance.tariff_2 = form.cleaned_data.get('tariff_2', '')
                type_instance.tariff_3 = form.cleaned_data.get('tariff_3', '')
            elif type_instance.had_general_tariff:
                type_instance.general_tariff = form.cleaned_data.get('general_tariff', '')
            elif type_instance.had_parent and type_instance.parent_type:
                parent = type_instance.parent_type
                type_instance.tariff_1 = form.cleaned_data.get('tariff_1', parent.tariff_1)
                type_instance.tariff_2 = form.cleaned_data.get('tariff_2', parent.tariff_2)
                type_instance.tariff_3 = form.cleaned_data.get('tariff_3', parent.tariff_3)
            
            type_instance.save()
            messages.success(request, _('Тип услуги успешно обновлен'))
            return redirect('communal_services:service_edit', pk=service.pk)
    else:
        form = CommunalServiceTypeForm(
            instance=service_type,
            communal_service=service
        )
    
    return render(request, 'communal_services/service_type_form.html', {
        'form': form,
        'service': service,
        'service_type': service_type,
        'title': _('Редактирование типа услуги')
    })


@login_required
def service_type_delete(request, service_pk, pk):
    service = get_object_or_404(CommunalService, pk=service_pk)
    service_type = get_object_or_404(CommunalServiceType, pk=pk)
    
    if request.method == 'POST':
        service_type.delete()
        messages.success(request, _('Тип услуги успешно удален'))
        return redirect('communal_services:service_edit', pk=service.pk)
    
    return render(request, 'communal_services/service_type_confirm_delete.html', {
        'service': service,
        'service_type': service_type
    })