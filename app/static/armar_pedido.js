// armar_pedido.js — confirmación del botón Pagar con SweetAlert2
(() => {
    const boton = document.getElementById('btn-pagar');
    if (!boton || typeof Swal === 'undefined') return;

    boton.addEventListener('click', () => {
        Swal.fire({
            title: '¿Confirmás el pago?',
            text: 'Revisá tu pedido antes de continuar.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, confirmar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                const form = document.getElementById('form-confirmar');
                if (form) form.submit();
            }
        });
    });
})();