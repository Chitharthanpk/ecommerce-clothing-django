
const sizeButtons = document.querySelectorAll('input[type="radio"]');
const addToCartButton = document.querySelector('.add-to-cart-button');

sizeButtons.forEach((button) => {
    button.addEventListener('change', () => {
        const selectedSize = document.querySelector('input[type="radio"]:checked');

        // Enable or disable the "Add to cart" button based on the selected size's availability
        if (selectedSize) {
            addToCartButton.disabled = false;
        } else {
            addToCartButton.disabled = true;
        }
    });
});



var ProductImg = document.getElementById("ProductImg");
var SmallImg = document.getElementsByClassName("SmallImg");
SmallImg[0].onclick = function () {
ProductImg.src = SmallImg[0].src;
}
SmallImg[1].onclick = function () {
ProductImg.src = SmallImg[1].src;
}
SmallImg[2].onclick = function () {
ProductImg.src = SmallImg[2].src;
}
SmallImg[3].onclick = function () {
ProductImg.src = SmallImg[3].src;
}



$("#add-to-cart-btn").on("click", function () {
let quantity = $("#product-quantity").val();
let product_name = $(".product-name").val();
let product_id = $(".product-id").val();
let product_price = $(".current-product-price").text();

let this_val = $(this);

console.log("Quantity", quantity);
console.log("Product_Name", product_name);
console.log("Product_Id", product_id);
console.log("Product_Price", product_price);
console.log("current_element :", this_val);
});
