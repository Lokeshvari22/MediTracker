/*
    MediTrack Pro
    Frontend Validation Script

    Handles:
    - Login/Register validation
    - Medicine form validation
    - Sales validation
    - CSV import validation
*/


document.addEventListener("DOMContentLoaded", function () {


    /*
        Generic Bootstrap Form Validation
    */

    const forms = document.querySelectorAll(".needs-validation");


    Array.from(forms).forEach(function (form) {

        form.addEventListener(
            "submit",
            function (event) {

                if (!form.checkValidity()) {

                    event.preventDefault();
                    event.stopPropagation();

                }


                form.classList.add("was-validated");


            },
            false
        );

    });



});





/*
    Password Validation
*/

function validatePassword(password) {


    const errors = [];


    if (password.length < 8) {

        errors.push(
            "Password must contain at least 8 characters"
        );

    }


    if (!/[A-Z]/.test(password)) {

        errors.push(
            "Password must contain one uppercase letter"
        );

    }


    if (!/[a-z]/.test(password)) {

        errors.push(
            "Password must contain one lowercase letter"
        );

    }


    if (!/[0-9]/.test(password)) {

        errors.push(
            "Password must contain one number"
        );

    }


    if (!/[!@#$%^&*]/.test(password)) {

        errors.push(
            "Password must contain one special character"
        );

    }


    return errors;

}





/*
    Register Password Check
*/

function checkPasswordStrength(input) {


    const password = input.value;


    const message =
        document.getElementById(
            "passwordMessage"
        );


    if (!message) return;



    const errors =
        validatePassword(password);



    if(errors.length === 0){

        message.innerHTML =
            `
            <span class="text-success">
            Strong Password ✓
            </span>
            `;

    }

    else{


        message.innerHTML =
            `
            <span class="text-danger">
            ${errors[0]}
            </span>
            `;

    }


}






/*
    Confirm Password Validation
*/


function checkConfirmPassword(
    password,
    confirmPassword
){


    if(password !== confirmPassword){

        return false;

    }


    return true;


}








/*
    Medicine Form Validation
*/


function validateMedicineForm(){


    const medicineName =
        document.getElementById(
            "medicine_name"
        );


    const quantity =
        document.getElementById(
            "quantity"
        );


    const price =
        document.getElementById(
            "price"
        );



    if(!medicineName.value.trim()){


        alert(
            "Medicine name is required"
        );

        return false;

    }



    if(quantity.value <=0){


        alert(
            "Quantity must be greater than zero"
        );

        return false;

    }



    if(price.value <=0){


        alert(
            "Price must be greater than zero"
        );

        return false;

    }



    return true;


}








/*
    Sales Validation
*/


function validateSaleForm(){


    const quantity =
        document.getElementById(
            "sale_quantity"
        );


    const available =
        document.getElementById(
            "available_stock"
        );



    if(quantity.value <=0){


        alert(
            "Enter valid quantity"
        );


        return false;

    }



    if(
        Number(quantity.value)
        >
        Number(available.value)
    ){


        alert(
            "Not enough stock available"
        );


        return false;

    }



    return true;


}








/*
    CSV Import Validation
*/


function validateImportFile(input){



    const file =
        input.files[0];



    if(!file){

        return false;

    }



    const extension =
        file.name
        .split(".")
        .pop()
        .toLowerCase();



    if(extension !== "csv"){


        alert(
            "Only CSV files are allowed"
        );


        input.value="";


        return false;


    }



    return true;


}








/*
    Delete Confirmation
*/


function confirmDelete(message){


    return confirm(
        message ||
        "Are you sure you want to delete?"
    );


}








/*
    Auto Hide Alert Messages
*/


setTimeout(
    function(){

        const alerts =
            document.querySelectorAll(
                ".alert"
            );


        alerts.forEach(
            function(alert){

                alert.style.display =
                    "none";

            }
        );


    },
    5000
);