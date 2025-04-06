
document.addEventListener("DOMContentLoaded", function () {

    let isBusiness = document.getElementById("isBusiness");
    let business = document.getElementById("business-block");
    let personal = document.getElementById("individual-block");
    
    if (isBusiness && business && personal) {
        // Ensure correct initial display state
        business.style.display = "none";
        personal.style.display = "block";
        
        isBusiness.addEventListener("change", function () {
            if (isBusiness.checked) {
                business.style.display = "block";
                personal.style.display = "none";
            } else {
                business.style.display = "none";
                personal.style.display = "block";
            }
        });
    }
});