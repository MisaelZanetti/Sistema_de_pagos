(function () {
  const root = document.querySelector('.tecnopc-home');
  if (!root) return;
  const toast = root.querySelector('#tp-toast');
  let toastTimer;

  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('is-visible');
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => toast.classList.remove('is-visible'), 2400);
  }

  root.querySelectorAll('.tp-add-button').forEach((button) => {
    button.addEventListener('click', () => {
      showToast(button.dataset.product + ' se añadió a la bolsa de demostración');
    });
  });

  const configButton = root.querySelector('#tp-config-button');
  if (configButton) {
    configButton.addEventListener('click', () => {
      showToast('El configurador estará disponible próximamente');
    });
  }
})();
