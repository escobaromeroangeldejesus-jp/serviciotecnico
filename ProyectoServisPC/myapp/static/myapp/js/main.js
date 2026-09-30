        const estrellas = document.querySelectorAll('.estrella');

        const campoEstrellas = document.getElementById(
            'id_estrellas'
        );

        const textoEstrellas = document.getElementById(
            'texto-estrellas'
        );


        const textos = [
            '',
            'Muy mala',
            'Mala',
            'Regular',
            'Buena',
            'Excelente'
        ];


        estrellas.forEach(function(estrella) {

            estrella.addEventListener('click', function() {

                const valor = this.dataset.value;

                // Guardamos el valor en el campo de Django
                campoEstrellas.value = valor;

                // Iluminamos las estrellas seleccionadas

                estrellas.forEach(function(item) {

                    if (item.dataset.value <= valor) {

                        item.classList.remove('bi-star');

                        item.classList.add(
                            'bi-star-fill',
                            'seleccionada'
                        );

                    } else {

                        item.classList.remove(
                            'bi-star-fill',
                            'seleccionada'
                        );

                        item.classList.add('bi-star');

                    }

                });

                textoEstrellas.textContent =
                    textos[valor];

            });

        });