function navshow() {

    const centernav = document.getElementById('centernav');
    if (centernav.style.display == 'none') {

        centernav.style.display = 'block'
    }
    else {
        centernav.style.display = 'block'
    }
}

// Get references to the buttons
const toggleButtons = document.querySelectorAll('.toggleButton');


// Add click event listeners to each button
toggleButtons.forEach(button => {
    button.addEventListener('click', function () {
        const currentValue = button.getAttribute('value');
        const onlights = document.querySelector('.onlights');
        const offlights = document.querySelector('.offlights');

        // Toggle the value for the clicked button
        button.setAttribute('value', currentValue === 'true' ? 'false' : 'true');

        // Update the view based on the value
        if (currentValue === 'true') {
            button.classList.remove('true-color');
            onlights.style.display='block'
            offlights.style.display='none'

        } else {
            button.classList.add('true-color');
            onlights.style.display='none'
            offlights.style.display='block'

        }
    });
});
