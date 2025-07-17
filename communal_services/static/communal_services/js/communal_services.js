document.addEventListener('DOMContentLoaded', function() {
    function initTypeForm() {
        const form = document.getElementById('communal-service-type-form');
        if (!form) return;

        const divisionCheckbox = form.querySelector('#id_division_by_tariff');
        const generalCheckbox = form.querySelector('#id_had_general_tariff');
        const parentCheckbox = form.querySelector('#id_had_parent');

        const divisionCheckboxBlock = form.querySelector('#division_by_tariff_block');
        const generalCheckboxBlock = form.querySelector('#had_general_tariff_block');
        const parentCheckboxBlock = form.querySelector('#had_parent_block');
        
        const parentTypeField = form.querySelector('#parent-type-field');
        const tariff1Field = form.querySelector('#tariff-1-field');
        const tariff2Field = form.querySelector('#tariff-2-field');
        const tariff3Field = form.querySelector('#tariff-3-field');
        const defaultTariffField = form.querySelector('#default-tariff-field');
        const generalTariffField = form.querySelector('#general-tariff-field');

        // Сбросить чекбоксы к дефолтному состоянию
        divisionCheckbox.checked = divisionCheckbox.defaultChecked;
        generalCheckbox.checked = generalCheckbox.defaultChecked;
        parentCheckbox.checked = parentCheckbox.defaultChecked;

        function updateFieldsVisibility() {
            const divisionChecked = divisionCheckbox.checked;
            const generalChecked = generalCheckbox.checked;
            const parentChecked = parentCheckbox.checked;

            // Скрываем все дополнительные поля
            [parentTypeField, tariff1Field, tariff2Field, tariff3Field, 
             defaultTariffField, generalTariffField].forEach(field => {
                if (field) field.style.display = 'none';
            });

            // Всегда показываем все блоки с чекбоксами
            [divisionCheckboxBlock, generalCheckboxBlock, parentCheckboxBlock].forEach(field => {
                if (field) field.style.display = 'block';
            });

            // Показываем нужные поля в зависимости от выбранного варианта
            if (divisionChecked) {
                // [tariff1Field, tariff2Field, tariff3Field, defaultTariffField].forEach(field => {
                //     if (field) field.style.display = 'block';
                // });
                [generalCheckboxBlock, parentCheckboxBlock].forEach(field => {
                    if (field) field.style.display = 'none';
                });
            } 
            else if (generalChecked) {
                [generalTariffField, defaultTariffField].forEach(field => {
                    if (field) field.style.display = 'block';
                });
                [divisionCheckboxBlock, parentCheckboxBlock].forEach(field => {
                    if (field) field.style.display = 'none';
                });
            } 
            else if (parentChecked) {
                parentTypeField.style.display = 'block';
                [divisionCheckboxBlock, generalCheckboxBlock].forEach(field => {
                    if (field) field.style.display = 'none';
                });
            }
        }

        function handleParentTypeChange() {
            const parentType = form.querySelector('#id_parent_type');
            if (!parentType) return;

            if (parentType.value && parentCheckbox.checked) {
                [tariff1Field, tariff2Field, tariff3Field, defaultTariffField].forEach(field => {
                    if (field) field.style.display = 'block';
                });
            } else {
                [tariff1Field, tariff2Field, tariff3Field].forEach(field => {
                    if (field) field.style.display = 'none';
                });
            }
        }

        // Инициализация
        updateFieldsVisibility();
        
        // Обработчики событий
        if (divisionCheckbox) {
            divisionCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    generalCheckbox.checked = false;
                    parentCheckbox.checked = false;
                }
                updateFieldsVisibility();
            });
        }

        if (generalCheckbox) {
            generalCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    divisionCheckbox.checked = false;
                    parentCheckbox.checked = false;
                }
                updateFieldsVisibility();
            });
        }

        if (parentCheckbox) {
            parentCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    divisionCheckbox.checked = false;
                    generalCheckbox.checked = false;
                }
                updateFieldsVisibility();
            });
        }

        const parentTypeSelect = form.querySelector('#id_parent_type');
        if (parentTypeSelect) {
            parentTypeSelect.addEventListener('change', handleParentTypeChange);
        }
    }

    initTypeForm();
    console.log("test");
    
});