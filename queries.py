
"""
    SQL queries can go here
"""

"""
Inventory Items Junction Table associated queries:
"""
chars_items_qty = "SELECT Characters.character_name, Items.item_name, Items.item_description, Inventory_Items.quantity from Characters " \
                 "INNER JOIN Inventory_Items ON Characters.character_id=Inventory_Items.Characters_character_id " \
                 "INNER JOIN Items ON Inventory_Items.Items_item_id=Items.item_id " \
                 "ORDER BY Characters.character_name ASC;"

individual_char_items = "SELECT Characters.character_name, Items.item_name, Items.item_description, Inventory_Items.quantity from Items " \
                 "INNER JOIN Inventory_Items ON Items.item_id=Inventory_Items.Items_item_id " \
                 "INNER JOIN Characters ON Inventory_Items.Characters_character_id=Characters.character_id " \
                 "INNER JOIN User_Accounts ON Characters.Users_user_id=User_Accounts.user_id " \
                 "WHERE User_Accounts.user_id='3'"

# For drop down menu functionality:
get_char_names = "SELECT Characters.character_name FROM Characters;"

"""
Items Table associated queries:
"""
get_all_item_info =  "SELECT Items.item_id, Items.item_name, Items.item_description, Items.is_weapon FROM Items"
insert_new_item = "INSERT INTO Items (item_name, item_description, is_weapon) VALUES (%s,%s,%s);"


"""
Queries used by User_Accounts (login) page:
"""
get_all_users = "SELECT * FROM User_Accounts;"

"""
Queries used by multiple pages:
"""
# For drop down menu functionality:
get_item_list = "SELECT Items.item_name FROM Items"