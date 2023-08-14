"""
    All SQL queries that act on the DB are defined here. This matches our DML
    but is Python valid syntax and variables.
"""

# -- *****************************************************************************
# -- Queries that act on Users page  --
# -- *****************************************************************************

# -- for loading the Dungeon details onto the Dungeon Page
insert_user = "INSERT INTO User_Accounts (username, password, email) VALUES (%s,%s,%s);"

get_all_users = "SELECT * FROM User_Accounts;"


# -- *****************************************************************************
# -- Queries that act on Spells/Abilities page --
# -- *****************************************************************************

# -- 2 queries for loading the Abilities table onto the Spells/Abilities page
get_all_abilities = "SELECT * FROM Abilities ORDER BY ability_name;"

get_ability_dungeon = "SELECT dungeon_name FROM Dungeons WHERE dungeon_id = %s;"

# -- for loading the Spells table onto the Spells/Abilities page
get_all_spells = "SELECT * FROM Spells ORDER BY spell_name;"

# -- get Spells of current User's Characters
get_user_spells = "SELECT spell_id, spell_name, spell_damage, character_name FROM Spells JOIN Characters_has_Spells ON Spells.spell_id = Characters_has_Spells.Spells_spell_id JOIN Characters ON Characters_has_Spells.Characters_character_id = Characters.character_id JOIN User_Accounts ON Characters.Users_user_id = User_Accounts.user_id WHERE User_Accounts.user_id = %s ORDER BY spell_name;"

# -- get Abilities of current User's Characters
#get_user_abilities = "SELECT ability_id, ability_name, ability_damage, Dungeons_dungeon_id, character_name FROM Abilities JOIN Characters_has_Abilities ON Abilities.ability_id = Characters_has_abilities.Abilities_ability_id JOIN Characters ON Characters_has_abilities.Characters_character_id = Characters.character_id JOIN User_Accounts ON Characters.Users_user_id = User_Accounts.user_id WHERE User_Accounts.user_id = %s ORDER BY ability_name;"
get_user_abilities = "SELECT ability_id, ability_name, ability_damage, Dungeons_dungeon_id, character_name FROM Abilities INNER JOIN Characters_has_Abilities ON Abilities.Ability_id = Characters_has_Abilities.Abilities_ability_id INNER JOIN Characters ON Characters_has_Abilities.Characters_character_id = Characters.character_id INNER JOIN User_Accounts ON Characters.Users_user_id = User_Accounts.user_id WHERE User_Accounts.user_id = %s ORDER BY ability_name ASC;"

# -- add a new Ability without a Character
add_ability = "INSERT INTO Abilities (ability_name, ability_damage, Dungeons_dungeon_id) VALUES (%s, %s, %s);" 

# -- link an Ability to a Character
add_ability_to_char = "INSERT INTO Characters_has_Abilities (Characters_character_id, Abilities_ability_id) VALUES (%s, %s);"

# -- add a new Spell without a Character
add_spell = "INSERT INTO Spells (spell_name, spell_damage) VALUES (%s, %s);"

# -- link a Spell to a Character
add_spell_to_char = "INSERT INTO Characters_has_Spells (Characters_character_id, Spells_spell_id) VALUES (%s, %s);"

# for updating an Ability for all characters
update_ability = "UPDATE Abilities SET ability_name = %s, ability_damage = %s, Dungeons_dungeon_id = %s WHERE ability_id = %s;"

# for deleting an Ability for all characters
delete_ability = "DELETE FROM Abilities WHERE ability_id = %s;"
 
# for deleting a link from the Characters_has_Abilities table
delete_user_ability = "DELETE FROM Characters_has_Abilities WHERE Abilities_ability_id = %s AND Characters_character_id = %s;"

# for updating an Spell for all characters
update_spell = "UPDATE Spells SET spell_name = %s, spell_damage = %s WHERE spell_id = %s;"

# for deleting an Spell for all characters
delete_spell = "DELETE FROM Spells WHERE spell_id = %s;"
 
# for deleting a link from the Characters_has_Spells table
delete_user_spell = "DELETE FROM Characters_has_Spells WHERE Spells_spell_id = %s AND Characters_character_id = %s;"


# -- *****************************************************************************
# -- Queries that act on Dungeons page --
# -- *****************************************************************************

# -- for loading the Dungeon details onto the Dungeon Page
get_dungeon = "SELECT dungeon_name, dungeon_type, dungeon_description, damage_multiplier FROM Dungeons WHERE dungeon_id = %s;"

# -- *****************************************************************************
# -- Queries that act on Characters page (charPage) --
# -- *****************************************************************************

# -- for loading the Character details onto the Character Page
get_char = "SELECT character_name, race,  class, creature_type, alignment FROM Characters WHERE character_id = %s;"

# -- get Spells of current selected single Character View
get_char_spells =  "SELECT spell_id, spell_name, spell_damage, username FROM Spells JOIN Characters_has_Spells ON Spells.spell_id = Characters_has_Spells.Spells_spell_id JOIN Characters ON Characters_has_Spells.Characters_character_id = Characters.character_id JOIN User_Accounts ON Characters.Users_user_id = User_Accounts.user_id WHERE Characters.character_id = %s ORDER BY spell_name;"

# -- get Abilities of current selected single Character View
get_char_abilities = "SELECT ability_id, ability_name, ability_damage, Dungeons_dungeon_id, username FROM Abilities JOIN Characters_has_Abilities ON Abilities.ability_id = Characters_has_Abilities.Abilities_ability_id JOIN Characters ON Characters_has_Abilities.Characters_character_id = Characters.character_id JOIN User_Accounts ON Characters.Users_user_id = User_Accounts.user_id WHERE Characters.character_id = %s ORDER BY ability_name;"


# -- *****************************************************************************
# -- Queries that act on Items pages --
# -- *****************************************************************************

# -- for loading the Dungeon details onto the Dungeon Page
get_item = "SELECT item_name, item_description, is_weapon FROM Items WHERE item_id = %s;"

# -- for getting item details
get_all_item_info = "SELECT Items.item_id, Items.item_name, Items.item_description, Items.is_weapon FROM Items"

# -- for creating a new item
insert_new_item = "INSERT INTO Items (item_name, item_description, is_weapon) VALUES (%s,%s,%s);"


# -- *****************************************************************************
# -- Queries that act on dungeonSelection Page  --
# -- *****************************************************************************


# for loading only this user’s Dungeons (via attachments to the abilities that this user’s chars have) in the “My Dungeons” list
get_user_dungeons = "SELECT dungeon_id, character_name, ability_name, dungeon_name, dungeon_type, dungeon_description, damage_multiplier FROM Dungeons INNER JOIN Abilities ON Dungeons.dungeon_id = Abilities.Dungeons_dungeon_id INNER JOIN Characters_has_Abilities ON Abilities.ability_id = Characters_has_Abilities.Abilities_ability_id INNER JOIN Characters ON Characters_has_Abilities.Characters_character_id = Characters.character_id INNER JOIN User_Accounts ON Characters.Users_user_id = User_Accounts.user_id WHERE User_Accounts.user_id = %s;"
 
# for Dungeon creation
add_dungeon = "INSERT INTO Dungeons (dungeon_name, dungeon_type, dungeon_description, damage_multiplier) VALUES (%s, %s, %s, %s);"
 
 # for when the user updates a Dungeon
update_dungeon = "UPDATE Dungeons SET dungeon_name = %s, dungeon_type = %s, dungeon_description = %s, damage_multiplier = %s WHERE dungeon_id = %s;"
 
 # for deleting from the dungeon table
delete_dungeon = "DELETE FROM Dungeons WHERE dungeon_id = %s;"




# -- *****************************************************************************
# -- Queries that act on charSelection Page  --
# -- *****************************************************************************

# -- for loading all Characters in the “All Characters” list
get_all_chars = "SELECT character_id, character_name, race, class, creature_type, alignment FROM Characters ORDER BY character_name ASC;"

# -- this displays the user’s username in “User007’s Chars”
# get_user = "SELECT username FROM User_Accounts WHERE user_id = %s;"

# -- for Character creation
add_char = "INSERT INTO Characters (character_name, race, class, creature_type, alignment, Users_user_id) VALUES (%s, %s, %s, %s, %s, %s);"
 
# -- for when the user updates a Char
update_char = "UPDATE Characters SET character_name = %s, race = %s, class = %s, creature_type = %s, alignment = %s WHERE character_id = %s;"

# -- for when a user deletes a char
delete_char = "DELETE FROM Characters WHERE character_id = %s;"



# -- *****************************************************************************
# --  Queries that act on Inventory page --
# -- *****************************************************************************

# -- select all inventory items
chars_items_qty = "SELECT Characters.character_name, Items.item_name, Items.item_description, Inventory_Items.quantity, Inventory_Items.inventory_id, Items.item_id, Characters.character_id from Characters " \
                 "INNER JOIN Inventory_Items ON Characters.character_id=Inventory_Items.Characters_character_id " \
                 "LEFT JOIN Items ON Inventory_Items.Items_item_id=Items.item_id " \
                 "ORDER BY Characters.character_name ASC;"

# -- Select inventory items based on User_Accounts.username:
individual_char_items = "SELECT User_Accounts.username, Characters.character_name, Items.item_name, Items.item_description,Inventory_Items.quantity, Items.item_id from User_Accounts INNER JOIN Characters on User_Accounts.user_id=Characters.Users_user_id INNER JOIN Inventory_Items ON Characters.character_id=Inventory_Items.Characters_character_id INNER JOIN Items ON Inventory_Items.Items_item_id=Items.item_id WHERE User_Accounts.username=%s;"

# -- for when a user deletes an inventory item
delete_item_from_inv = "DELETE FROM Inventory_Items WHERE inventory_id=%s;"

# -- Update query for 3 tables (Items, Inventory_Items, Characters)
update_inventory_items = "UPDATE Characters, Inventory_Items, Items SET Characters.character_name=%s, Inventory_Items.quantity=%s, Items.item_name=%s, Items.item_description=%s WHERE Items.item_id=Inventory_Items.Items_item_id AND Characters.character_id=Inventory_Items.Characters_character_id AND Inventory_Items.inventory_id=%s;"

# -- Set a Inventory_Items.Items_item_id FK to NULL:
update_inv_items_null = "UPDATE Characters, Inventory_Items SET Characters.character_name=%s, Inventory_Items.quantity=%s, Inventory_Items.Items_item_id=NULL WHERE Characters.character_id=Inventory_Items.Characters_character_id AND Inventory_Items.inventory_id=%s;"

# -- INSERT into Inventory_Items table
insert_inv_items = "INSERT INTO Inventory_Items (Characters_character_id, Items_item_id, quantity) VALUES (%s,%s,%s);"

# For drop down menu functionality:
get_char_list = "SELECT Characters.character_id, Characters.character_name FROM Characters;"



# -- *****************************************************************************
# -- Queries that act on multiple pages: --
# -- *****************************************************************************

# For drop down menu functionality:
get_item_list = "SELECT Items.item_id, Items.item_name FROM Items"

# this gets the user's id from the sessions username
get_user_id = "SELECT user_id FROM User_Accounts WHERE username = %s;"

# this gets the char's id from the char's name
get_char_id = "SELECT character_id FROM Characters WHERE character_name = %s;"

# for loading all Dungeons in the “All Dungeons” list & for inserting a dungeon into an Ability
get_all_dungeons = "SELECT dungeon_id, dungeon_name, dungeon_type, dungeon_description, damage_multiplier FROM Dungeons ORDER BY dungeon_name ASC;"

# -- for loading only this user’s Characters in the “My Characters” list or on the Spells/Abilities page
get_user_chars = "SELECT character_id, character_name, race, class, creature_type, alignment FROM Characters JOIN User_Accounts ON Characters.Users_user_id = User_Accounts.user_id WHERE User_Accounts.user_id = %s ORDER BY character_name ASC;"
