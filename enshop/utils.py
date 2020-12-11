import frappe


def update_website_context(context):
    context.most_popular_cards = _get_most_popular_cards('most_popular_cards')
    context.featured_item_group = _get_featured_item_group_cards('featured_item_group')

   

def _get_most_popular_cards(parentfield):
    return frappe.get_all(
        "Enshop Settings Card Most Popular",
        fields=["label", "hyperlink","imageurl"],
        filters={"parentfield": parentfield}
    )
def _get_featured_item_group_cards(parentfield):
    return frappe.get_all(
        "Enshop Group Card",
        fields=["label","imageurl"],
        filters={"parentfield": parentfield}
    )


