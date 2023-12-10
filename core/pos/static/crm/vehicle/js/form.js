document.addEventListener('DOMContentLoaded', function (e) {
    const fv = FormValidation.formValidation(document.getElementById('frmForm'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                type: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 9,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fv.form.querySelector('[type="type"]').value,
                                    pattern: 'type',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El nombre ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                placa: {
                    validators: {
                        stringLength: {
                            min: 4,
                        }
                    }
                },
                chasis: {
                    validators: {
                        stringLength: {
                            min: 18,
                        }
                    }
                },
                model: {
                    validators: {
                        stringLength: {
                            min: 10,
                        }
                    }
                },
                motor: {
                    validators: {
                        stringLength: {
                            min: 18,
                        }
                    }
                },
                km: {
                    validators: {
                        stringLength: {
                            min: 1,
                            max: 6,
                        }
                    }
                },
                cylinder: {
                    validators: {
                        stringLength: {
                            min: 4,
                        }
                    }
                },
                capacitycarga: {
                    validators: {
                        stringLength: {
                            min: 1,
                        }
                    }
                },
                capacitypeople: {
                    validators: {
                        stringLength: {
                            min: 1,
                        }
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fv.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            submit_formdata_with_ajax_form(fv);
        });
});
