const btn = document.getElementById('btn');

// On clicking submit clear designated fields
btn.addEventListener('click', function Submit(event) {
    const block = document.querySelectorAll('#name, #email, #subject');
    block.forEach(fill => {
        fill.value = '';
    });
    // Add alert
    alert('To infinity....and beyond!');
});

