
$(() => {

	class ProductListing {
		constructor() {
			this.bind_filters();
		}
		bind_filters() {
			if (window.location.pathname === "/all-products") {

				const queryString = window.location.search
				const urlParams = new URLSearchParams(queryString);
				const category_name = urlParams.get("categories")
				const item_group_name = urlParams.get("item_group")

				if (category_name && item_group_name) {

					const args = {
						category_name: category_name,
						group_name: item_group_name
					}
					console.log(category_name)
					frappe.call('enshop.api.item_filters.get_products_html_for_website_by_category_name_and_group', args)
						.then(r => {
							if (r.message) {
								var html = r.message
								$($('.page_content').children()[2]).html(html);
							} else {
								$($('.page_content').children()[2]).html("<div></div>");
							}
						})

				} else if (item_group_name) {
					//to be continue
				}
				else if (category_name) {

					const args = {
						category_name: category_name
					}
					frappe.call('enshop.api.item_filters.get_products_html_for_website_by_category_name', args)
						.then(r => {
							if (r.message) {
								var html = r.message
								$($('.page_content').children()[2]).html(html);
							} else {
								$($('.page_content').children()[2]).html("<div></div>");
							}
						})
				}
			}
			else if (window.location.pathname === "/categories") {
				const queryString = window.location.search

				$('.select-category').on('click', function () {
					const new_params = queryString + "&categories=" + this.text.trim()
					window.location = 'all-products' + new_params
				});
			}

			if (window.location.pathname === "/categories") {
				const queryString = window.location.search
				const urlParams = new URLSearchParams(queryString);
				const item_group_name = urlParams.get("item_group")

				const args = {
					group_name: item_group_name
				}

				frappe.call('enshop.api.item_filters.get_categories_from_group', args)
					.then(r => {
						if (r.message) {
							var html = r.message
							$('.card').html(html);
							const queryString = window.location.search

							$('.select-category').on('click', function () {
								const new_params = queryString + "&categories=" + this.text.trim()
								window.location = 'all-products' + new_params
							});
						} else {
							$('.card').html("<div>No Categories Found</div>");
						}
					})


			}
		}
	}
	new ProductListing();
})

const getQueryParams = ( name, url ) => {
  
	name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
  };