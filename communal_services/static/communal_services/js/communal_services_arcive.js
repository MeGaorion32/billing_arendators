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
        
        const parentTypeField = form.querySelector('#id_parent_type').closest('.form-group');
        const tariff1Field = form.querySelector('#id_tariff_1').closest('.form-group');
        const tariff2Field = form.querySelector('#id_tariff_2').closest('.form-group');
        const tariff3Field = form.querySelector('#id_tariff_3').closest('.form-group');
        const defaultTariffField = form.querySelector('#id_default_tariff').closest('.form-group');
        const generalTariffField = form.querySelector('#id_general_tariff').closest('.form-group');

        // Сбросить все checkbox'ы к их исходным значениям (как при загрузке)
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

            // Всегда показываем все блоки с чекбоксами (они могут быть скрыты ранее)
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
                [divisionCheckboxBlock, parentCheckboxBlock].forEach(field => {
                    if (field) field.style.display = 'none';
                });
                [generalTariffField, defaultTariffField].forEach(field => {
                    if (field) field.style.display = 'block';
                });
            } 
            else if (parentChecked) {
                [divisionCheckboxBlock, generalCheckboxBlock].forEach(field => {
                    if (field) field.style.display = 'none';
                });
                parentTypeField.style.display = 'block';
                // Поля тарифов появятся после выбора родителя
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
    console.log("Test");
    
});