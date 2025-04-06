document.addEventListener("DOMContentLoaded", function () {
    let TrademarkName = null;
    let TradeMarkLogo = null;
    let Categories_Tags = null;
    let Price = null;

    fetchSection1();
    fetchSection2();
    fetchPrice();
    fetchSection3();

});

// Section 1
function fetchSection1() {
    fetch('/get-section-1')
        .then(response => response.json())
        .then(data => {
            const trademarkName = data.text;
            const trademarkImage = data['file-data']; // Accessing property with hyphen
            const trademarkImageName = data['file-name']; // Accessing property with hyphen
            createSection1(trademarkName, trademarkImage, trademarkImageName);
        })
        .catch(error => {
            console.error('Error fetching section 1:', error);
        });
}

function createSection1(name, image, imageName) {
    let trademarkNameElement = document.getElementById("order-summary-name");
    trademarkNameElement.className = "card";
    trademarkNameElement.style.backgroundColor =  "#f5f3f4";
   
    // create name element:
    if (name != null) {
        let Namesection = document.createElement("h2");
        Namesection.className = "card-body";
        Namesection.textContent = `Trademark Name`;
        document.getElementById("order-summary-name").before(Namesection);

        let nameElement = document.createElement("h5");
        nameElement.className = "card-body";
        nameElement.textContent = name;
        trademarkNameElement.appendChild(nameElement);
        console.log("created name element");
        // create image element:
    }
    if (image != null) {
        let imgSection = document.getElementById("order-summary-img");
        // Set up the card container
        imgSection.className = "card";

        header = document.createElement("h2");
        header.className = "card-body";
        header.textContent = "Trademark Logo";
        document.getElementById("order-summary-img").before(header);
        //imgSection.appendChild(header);
        
        // Create the image element
        let img = document.createElement("img");
        img.src = `data:image/png;base64,${image}`;///NEED TO UPDATE CODE AND DB TO STORE IMAGE FILE TYPE IN DB
        img.width = 150;
        img.height = 150;
        img.alt = imageName;
        
        // Create the card body (optional, if you want to add text or other content)
        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
        
        // Add the image to the card
        cardBody.appendChild(img);
        
        // Add the card body to the card (optional)
        imgSection.appendChild(cardBody);
        console.log("created image element");
    }
}



// Section 2
function fetchSection2() {
    fetch('/get-section-2')
        .then(response => response.json())
        .then(data => {
            const classDict = {}; // class, tags

            data.forEach(({ class_selected, tags }) => {
                if (!classDict[class_selected]) {
                    classDict[class_selected] = [tags];
                }
                else {
                    classDict[class_selected].push(tags);
                }
            });

            createSection2(classDict);

        })
        .catch(error => {
            console.error('Error fetching section 2:', error);
        });
}
function createSection2(classDict) {
    let heading = document.createElement("h2");
    heading.textContent = "Selected Trademark Categories and Tags";
    document.getElementById("order-summary-trademarks").appendChild(heading);

    let accordionContainer = document.getElementById("order-summary-trademarks");
    accordionContainer.className = "accordion";

    // Iterate over each class_selected in classDict
    for (let classSelected in classDict) {
        if (classDict.hasOwnProperty(classSelected)) {
            let tags = classDict[classSelected]; // Get the array of tags for this class_selected

            // Create the accordion item
            let accordionItem = document.createElement("div");
            accordionItem.className = "accordion-item";

            // Create the accordion header
            let accordionHeader = document.createElement("h2");
            accordionHeader.className = "accordion-header";
            accordionHeader.id = `heading-${classSelected}`;

            // Create the accordion button
            let accordionButton = document.createElement("button");
            accordionButton.className = "accordion-button";
            accordionButton.type = "button";
            accordionButton.setAttribute("data-bs-toggle", "collapse");
            accordionButton.setAttribute("data-bs-target", `#accordion-body-${classSelected}`);
            accordionButton.setAttribute("aria-expanded", "true");
            accordionButton.setAttribute("aria-controls", `accordion-body-${classSelected}`);
            accordionButton.textContent = classSelected;

            // Append the button to the header
            accordionHeader.appendChild(accordionButton);

            // Create the accordion collapse section
            let accordionCollapse = document.createElement("div");
            accordionCollapse.id = `accordion-body-${classSelected}`;
            accordionCollapse.className = "accordion-collapse collapse show";
            accordionCollapse.setAttribute("aria-labelledby", `heading-${classSelected}`);

            // Create the accordion body
            let accordionBody = document.createElement("div");
            accordionBody.className = "accordion-body";

            // Add tags to the accordion body as badges
            tags.forEach(tag => {
                let badge = document.createElement("span");
                badge.className = "badge rounded-pill badge-colour m-1";
                badge.textContent = tag;
                accordionBody.appendChild(badge);
            });

            // Append the body to the collapse section
            accordionCollapse.appendChild(accordionBody);

            // Append the header and collapse section to the accordion item
            accordionItem.appendChild(accordionHeader);
            accordionItem.appendChild(accordionCollapse);

            // Append the accordion item to the container
            accordionContainer.appendChild(accordionItem);
        }
    }
}


// PRICE SECTION
function fetchPrice() {
    fetch('/get-price')
        .then(response => response.json())
        .then(data => {
            const price = data.price;
            createPrice(price);
        })
        .catch(error => {
            console.error('Error fetching section 1:', error);
        });
}



function createPrice(price) {
    let costContainer = document.getElementById("order-summary-cost");
    costContainer.className = "card bg-dark text-white";

    // Create and append cost display
    let costItem = document.createElement("h4");
    costItem.className = "card-body";
    costItem.textContent = `Total Cost: £${price}`;
    costItem.style.fontWeight = "bold";
    costContainer.appendChild(costItem);
   
}


// Section 3
function fetchSection3() {
    fetch('/get-section-3')
        .then(response => response.json())
        .then(data => {
            const isBusiness = data.isBusiness;
            const businessName = data.businessname;
            const fullName = data.fullname;
            const address = data.address;
            const country = data.country;
            const email = data.email;
            const phone = data.phone;
            createSection3(isBusiness, businessName, fullName, address, country, email, phone);
        })
        .catch(error => {
            console.error('Error fetching section 1:', error);
        });
}


function createSection3(isBusiness, businessName, fullName, address, country, email, phone) {
   

    let heading = document.createElement("h2");
    heading.textContent = "Personal Information";
    document.getElementById("order-summary-info").before(heading);

    let container = document.getElementById("order-summary-info");
    container.className = "card ";

    if (isBusiness == true) {
        let businessNameElement = document.createElement("h5");
        businessNameElement.className = "card-body";
        businessNameElement.textContent = `Business Name: ${businessName}`;
        businessNameElement.style.borderBottom = "1px solid #e9ecef";
        container.appendChild(businessNameElement);
    } else {
        let fullNameElement = document.createElement("h5");
        fullNameElement.className = "card-body";
        fullNameElement.textContent = `Full Name: ${fullName}`;
        fullNameElement.style.borderBottom = "1px solid #e9ecef";
        container.appendChild(fullNameElement);
    }

    let addressElement = document.createElement("h5");
    addressElement.className = "card-body";
    addressElement.textContent = `Address: ${address}`;
    addressElement.style.borderBottom = "1px solid #e9ecef";
    container.appendChild(addressElement);
    console.log("created address element");

    let countryElement = document.createElement("h5");
    countryElement.className = "card-body";
    countryElement.textContent = `Country: ${country}`;
    countryElement.style.borderBottom = "1px solid #e9ecef";
    container.appendChild(countryElement);

    let emailElement = document.createElement("h5");
    emailElement.className = "card-body";
    emailElement.textContent = `Email: ${email}`;
    emailElement.style.borderBottom = "1px solid #e9ecef";
    container.appendChild(emailElement);

    let phoneElement = document.createElement("h5");
    phoneElement.className = "card-body";
    phoneElement.textContent = `Phone: ${phone}`;
    container.appendChild(phoneElement);
}