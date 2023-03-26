const form = document.querySelector('form');
const loadingComponent = document.querySelector('#loading-component');

form.addEventListener('submit', () => {
    loadingComponent.classList.remove('invisible');
});