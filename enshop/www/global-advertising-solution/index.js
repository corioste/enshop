$(document).ready(function () {
	$(".wish-icon i").click(function () {
		$(this).toggleClass("fa-heart fa-heart-o");
	});
});

$('.add-to-cart').on('click', function () {
	var item_code = $(this).attr('data-item-code')
	erpnext.shopping_cart.update_cart({
		item_code,
		qty: 1,
		callback(r) {
			console.log(r)
		}
	});
});
