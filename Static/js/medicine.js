// static/js/medicine.js

document.addEventListener("DOMContentLoaded", function () {

    console.log("Medicine JS Loaded");


    /* -----------------------------
       Medicine Delete Confirmation
    ------------------------------ */

    const deleteButtons = document.querySelectorAll(".delete-medicine");

    deleteButtons.forEach(button => {

        button.addEventListener("click", function (event) {

            const medicineName = this.dataset.name;

            const confirmDelete = confirm(
                `Are you sure you want to delete ${medicineName}?`
            );

            if (!confirmDelete) {
                event.preventDefault();
            }

        });

    });



    /* -----------------------------
       Medicine Search Filter
    ------------------------------ */

    const searchInput = document.getElementById("medicineSearch");

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            const searchValue = this.value.toLowerCase();

            const rows = document.querySelectorAll(
                ".medicine-row"
            );


            rows.forEach(row => {

                const medicineName =
                    row.dataset.name.toLowerCase();


                if (medicineName.includes(searchValue)) {

                    row.style.display = "";

                } else {

                    row.style.display = "none";

                }

            });

        });

    }




    /* -----------------------------
       Stock Quantity Validation
    ------------------------------ */

    const quantityInput =
        document.getElementById("quantity");


    if(quantityInput){

        quantityInput.addEventListener(
            "input",
            function(){

                if(this.value < 0){

                    this.value = 0;

                    alert(
                        "Stock quantity cannot be negative"
                    );

                }

            }
        );

    }





    /* -----------------------------
       Expiry Date Validation
    ------------------------------ */

    const expiryInput =
        document.getElementById("expiry_date");


    if(expiryInput){

        expiryInput.addEventListener(
            "change",
            function(){

                const selectedDate =
                    new Date(this.value);

                const today =
                    new Date();


                today.setHours(
                    0,0,0,0
                );


                if(selectedDate < today){

                    alert(
                        "Expiry date cannot be in the past"
                    );

                    this.value="";

                }

            }
        );

    }





    /* -----------------------------
       Auto Calculate Selling Price
    ------------------------------ */


    const purchasePrice =
        document.getElementById(
            "purchase_price"
        );


    const profitPercentage =
        document.getElementById(
            "profit_percentage"
        );


    const sellingPrice =
        document.getElementById(
            "selling_price"
        );



    if(
        purchasePrice &&
        profitPercentage &&
        sellingPrice
    ){

        function calculatePrice(){

            let purchase =
                Number(
                    purchasePrice.value
                );


            let profit =
                Number(
                    profitPercentage.value
                );


            let finalPrice =
                purchase +
                (
                    purchase *
                    profit /
                    100
                );


            sellingPrice.value =
                finalPrice.toFixed(2);

        }



        purchasePrice.addEventListener(
            "input",
            calculatePrice
        );


        profitPercentage.addEventListener(
            "input",
            calculatePrice
        );

    }




    /* -----------------------------
       Medicine Form Validation
    ------------------------------ */


    const medicineForm =
        document.getElementById(
            "medicineForm"
        );


    if(medicineForm){

        medicineForm.addEventListener(
            "submit",
            function(event){


                const name =
                    document.getElementById(
                        "medicine_name"
                    );


                if(
                    name &&
                    name.value.trim()===""
                ){

                    event.preventDefault();


                    alert(
                        "Medicine name is required"
                    );


                    name.focus();

                }


            }
        );

    }


});