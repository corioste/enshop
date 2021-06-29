$(document).ready(function () {

	// Lift card and show stats on Mouseover
	$('.product-card').hover(function () {
		console.log("HOVER")
		$(this).addClass('animate');
		$('div.carouselNext, div.carouselPrev').addClass('visible');
	}, function () {
		$(this).removeClass('animate');
		$('div.carouselNext, div.carouselPrev').removeClass('visible');
	});


});

frappe.ready(() => {
	$('.btn-prev, .btn-next').click((e) => {
		const $btn = $(e.target);
		$btn.prop('disabled', true);
		const start = $btn.data('start');
		let query_params = frappe.utils.get_query_params();
		query_params.start = start;
		let path = window.location.pathname + '?' + frappe.utils.get_url_from_dict(query_params);
		window.location.href = path;
	});
});

$(() => {
	class ProductListing {
		constructor() {
			this.bind_search();
			this.restore_filters_state();
		}

		bind_search() {
			$('input[type=search]').on('keydown', (e) => {
				if (e.keyCode === 13) {
					// Enter
					const value = e.target.value;
					if (value) {
						window.location.search = 'search=' + e.target.value;
					} else {
						window.location.search = '';
					}
				}
			});
		}

		restore_filters_state() {
			const filters = frappe.utils.get_query_params();
			let { field_filters, attribute_filters } = filters;

			if (field_filters) {
				field_filters = JSON.parse(field_filters);
				for (let fieldname in field_filters) {
					const values = field_filters[fieldname];
					const selector = values.map(value => {
						return `input[data-filter-name="${fieldname}"][data-filter-value="${value}"]`;
					}).join(',');
					$(selector).prop('checked', true);
				}
				this.field_filters = field_filters;
			}
			if (attribute_filters) {
				attribute_filters = JSON.parse(attribute_filters);
				for (let attribute in attribute_filters) {
					const values = attribute_filters[attribute];
					const selector = values.map(value => {
						return `input[data-attribute-name="${attribute}"][data-attribute-value="${value}"]`;
					}).join(',');
					$(selector).prop('checked', true);
				}
				this.attribute_filters = attribute_filters;
			}
		}
	}

	new ProductListing();

	function get_query_string(object) {
		const url = new URLSearchParams();
		for (let key in object) {
			const value = object[key];
			if (value) {
				url.append(key, value);
			}
		}
		return url.toString();
	}

	function if_key_exists(obj) {
		let exists = false;
		for (let key in obj) {
			if (obj.hasOwnProperty(key) && obj[key]) {
				exists = true;
				break;
			}
		}
		return exists ? obj : undefined;
	}
});


$('.add_to_cart').on('click', function () {
	var item_code = $(this).attr('data-item-code')
	erpnext.shopping_cart.update_cart({
		item_code,
		qty: 1,
		callback(r) {
			console.log(r)
		}
	});
});
