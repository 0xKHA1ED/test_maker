document.addEventListener("keyup", function(event) {
    if (event.key === "h") {  // Remove class when key is released
        console.log('h is clicked')
        document.querySelectorAll(".actions").forEach(el => el.classList.toggle("show"));
    }
});