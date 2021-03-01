def get_shopname_shop_url(each_shop):
    tag = each_shop.select_one('h3.slcHead > a')
    shop_name = tag.text
    shop_url = tag.get('href')

    return shop_name, shop_url

def get_phone_number_link(each_shop_html):
    return each_shop_html.select_one('td.w618 > a').get('href')