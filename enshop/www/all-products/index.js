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
			let {field_filters, attribute_filters} = filters;

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
