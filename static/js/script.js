const menuToggle =
    document.getElementById("menuToggle");

const navMenu =
    document.getElementById("navMenu");


menuToggle.addEventListener(
    "click",
    function () {

        navMenu.classList.toggle("show");

    }
);


// Close mobile menu
// when clicking a navigation link

const navLinks =
    document.querySelectorAll(
        ".nav-menu a"
    );


navLinks.forEach(
    function (link) {

        link.addEventListener(
            "click",
            function () {

                navMenu.classList.remove(
                    "show"
                );

            }
        );

    }
);


// Demo search form

const searchForm =
    document.querySelector(
        ".ride-search-form"
    );


searchForm.addEventListener(
    "submit",
    function (event) {

        event.preventDefault();

        alert(
            "Ride search feature will be connected to the backend soon!"
        );

    }
);

// SWAP LOCATIONS

const swapButton =
    document.querySelector(".swap-button");

const inputs =
    document.querySelectorAll(
        ".input-wrapper input[type='text']"
    );


if (swapButton && inputs.length >= 2) {

    swapButton.addEventListener(
        "click",
        function () {

            const temp =
                inputs[0].value;

            inputs[0].value =
                inputs[1].value;

            inputs[1].value =
                temp;

        }
    );

}

// OFFER RIDE FORM

const offerForm =
    document.getElementById("offer-form");


if (offerForm) {

    offerForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            alert(
                "Your ride has been submitted successfully! Backend connection will be added soon."
            );

            offerForm.reset();

        }
    );

}