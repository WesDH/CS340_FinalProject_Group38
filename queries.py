
"""
    SQL queries can go here
"""



# -- *****************************************************************************
# -- Queries that act on dungeonSelection Page  --
# -- *****************************************************************************

# for loading all Dungeons in the “All Dungeons” list
get_all_dungeons = "SELECT dungeon_name, dungeon_type, dungeon_description, damage_multiplier FROM Dungeons ORDER BY dungeon_name ASC;"

# this displays the user’s username in “User007’s Dungeons”
get_user = "SELECT username FROM User_Accounts WHERE user_id = %s;"

# for loading only this user’s Dungeons (via attachments to the abilities that this user’s chars have) in the “My Dungeons” list
get_user_dungeons = "SELECT character_name, ability_name, dungeon_name, dungeon_type, dungeon_description, damage_multiplier FROM Dungeons INNER JOIN Abilities ON Dungeons.dungeon_id = Abilities.Dungeons_dungeon_id INNER JOIN Characters_has_Abilities ON Abilities.ability_id = Characters_has_Abilities.Abilities_ability_id INNER JOIN Characters ON Characters_has_Abilities.Characters_character_id = Characters.character_id INNER JOIN User_Accounts ON Characters.Users_user_id = User_Accounts.user_id WHERE User_Accounts.user_id = %s;"
 
# # for Dungeon creation
# INSERT INTO Dungeons (dungeon_name, dungeon_type, dungeon_description, damage_multiplier) VALUES (dungeon_name = {{dungeon_name}}, dungeon_type = {{dungeon_type}}, dungeon_description = {{dungeon_description}}, damage_multiplier = {{damage_multiplier}});
# 
# # for when the user updates a Dungeon, previous values can be pre-loaded into the Edit form that the user submits, then only values that the user actually changed will be updated in the DB
# UPDATE Dungeons SET dungeon_name = {{dungeon_name}}, dungeon_type = {{dungeon_type}}, dungeon_description = {{dungeon_description}}, damage_multiplier = {{damage_multiplier}} WHERE dungeon_id = {{dungeon_id}};
# 
# # for deleting from the dungeon table
# DELETE FROM Dungeons WHERE dungeon_id = {{dungeon_id}};




# -- *****************************************************************************
# -- Queries that act on charSelection Page  --
# -- *****************************************************************************

# -- for loading all Characters in the “All Characters” list
get_all_chars = "SELECT character_id, character_name, race, class, creature_type, alignment FROM Characters ORDER BY character_name ASC;"

# -- for loading only this user’s Characters in the “My Characters” list
get_user_chars = "SELECT character_name, race, class, creature_type, alignment FROM Characters JOIN User_Accounts ON Characters.Users_user_id = User_Accounts.user_id WHERE User_Accounts.user_id = %s ORDER BY character_name ASC;"

# -- this displays the user’s username in “User007’s Chars”
get_user = "SELECT username FROM User_Accounts WHERE user_id = %s;"

# -- for Character creation
add_char = "INSERT INTO Characters (character_name, race, class, creature_type, alignment, Users_user_id) VALUES (%s, %s, %s, %s, %s, %s);"
 
# -- 2 queries for when the user updates a Char

update_char = "UPDATE Characters SET character_name = %s, race = %s, class = %s, creature_type = %s, alignment = %s WHERE character_id = %s;"

# -- for when a user deletes a char
delete_char = "DELETE FROM Characters WHERE character_id = %s;"




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
