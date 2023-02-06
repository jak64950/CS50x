const box = document.getElementById('box');

// Change text color on mouseover
box.addEventListener('mouseover', function handleMouseOver() {
  box.style.color = 'orange';
});

// Change text color back on mouseout
box.addEventListener('mouseout', function handleMouseOut() {
  box.style.color = 'white';
});