// Global vars
let selectedTags = {}; // tag: category
let selectedCategory = null; // Stores the last selected category


document.addEventListener("DOMContentLoaded", function () {
    let searchBar = document.getElementById("search-bar");
    // Fetch tags on keyup
    searchBar.addEventListener("keyup", function () {
        fetchTags();
    });

});


function fetchTags() {
    let query = document.getElementById("search-bar").value;
    if (query.length === 0) {
        document.getElementById("suggestions").innerHTML = "";
        return;
    }

    fetch(`/search-tags?q=${query}`)
        .then(response => response.json())
        .then(data => {
            let suggestionBox = document.getElementById("suggestions");
            suggestionBox.innerHTML = ""; // Clear previous results
            
            data.forEach(({ tag, category }) => {
                let div = document.createElement("div");
                div.className = "suggestion-item";
                div.innerHTML = tag;
                div.onclick = () => selectTag(tag, category);
                suggestionBox.appendChild(div);
            });
        });
}

function selectTag(tag, category) {
    document.getElementById("search-bar").value = tag;
    document.getElementById("suggestions").innerHTML = ""; // Hide suggestions after selection
    selectedCategory = category;
}

function addTag(tag, category) {
    let selectedTag = document.getElementById("search-bar").value.trim();
    if (!selectedTag || !selectedCategory) return; // Prevent empty tags and missing category

    document.getElementById('search-bar').value = ''; // Clear input
    document.getElementById('suggestions').innerHTML = ''; // Clear suggestions

    category = selectedCategory;
    selectedCategory = null; // Reset selected category
    if (!selectedTags[category]) {
        selectedTags[category] = [];
        createAccordion(category);
    }

    if (!selectedTags[category].includes(selectedTag)) {
        selectedTags[category].push(selectedTag);

        let badge = document.createElement("span");
        badge.className = "badge rounded-pill badge-colour m-1";
        badge.textContent = selectedTag;

        document.querySelector(`#accordion-body-${category} .accordion-body`).appendChild(badge);
    }
    updateCost();
}

function createAccordion(category) {
    let accordionContainer = document.getElementById("Accordions");
    let accordionItem = document.createElement("div");
    accordionItem.className = "accordion-item";
    
    accordionItem.innerHTML = `
        <h2 class="accordion-header" id="heading-${category}">
            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#accordion-body-${category}" aria-expanded="true" aria-controls="accordion-body-${category}">
                ${category}
            </button>
        </h2>
        <div id="accordion-body-${category}" class="accordion-collapse collapse show" aria-labelledby="heading-${category}">
            <div class="accordion-body"></div>
        </div>
    `;
    
    accordionContainer.appendChild(accordionItem);
}

function updateCost() {
    let costContainer = document.getElementById("cost-card");
    costContainer.className = "card bg-dark text-white";
    
    // Clear previous cost display to avoid duplication
    costContainer.innerHTML = "";

    // Calculate total cost based on unique categories and base cost
    let base = 200;
    let totalcost = Object.keys(selectedTags).length * 50 + base;

    // Create and append cost display
    let costItem = document.createElement("h5");
    costItem.className = "card-body";
    costItem.textContent = `Total Cost: £${totalcost}`;
    costContainer.appendChild(costItem);

   
}

function submitForm() {
    let form = document.getElementById("form-2");
    let tagsInput = document.getElementById("tags"); // Get hidden input
    tagsInput.value = JSON.stringify(selectedTags);
    console.log("Submitting tags:", tagsInput.value); // Debugging

    console.log(tagsInput.value);
    form.submit();
}   



///3rd
