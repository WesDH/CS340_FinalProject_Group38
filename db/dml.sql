-- Project Step 4 Draft Version: Design HTML Interface + DML SQL (Group / On Ed Discussion)
-- GROUP 38: Joseph Houghton, Lauren Norman Schueneman, Wesley Havens
--
-- DML queries that define the front-end/database interactions
-- {{var}} denotes custom variable inserted by Flask web framework


-- ********************************************************************
-- Queries that act on Home Page  --
-- ********************************************************************

-- for user account creation
INSERT INTO User_Accounts (username, password, email) VALUES ({{username}}, {{password}}, {{email}})

-- for selecting a single user by username dropdown
SELECT username, password, email FROM User_Accounts WHERE username = {{username}}

-- for selecting all users
SELECT username, password, email FROM User_Accounts ORDER BY username ASC


-- *****************************************************************************
-- Queries that act on charSelection Page  --
-- *****************************************************************************

-- for loading all Characters in the “All Characters” list
SELECT character_name, race, class, creature_type, alignment FROM Characters ORDER BY character_name ASC;

-- for loading only this user’s Characters in the “My Characters” list
SELECT character_name, race, class, creature_type, alignment FROM Characters JOIN User_Accounts ON Characters.Users_user_id = User_Accounts.user_id WHERE User_Accounts.user_id = {{user_id}} ORDER BY character_name ASC;

-- this displays the user’s username in “User007’s Chars”
SELECT username FROM User_Accounts WHERE user_id = {{user_id}};

-- for Character creation
INSERT INTO Characters (character_name, race, class, creature_type, alignment, Users_user_id) VALUES ({{character_name}}, {{race}}, {{class}}, {{creature_type}}, {{alignment}});

-- for when the user updates a Char, previous values can be pre-loaded into the Edit form that the user submits, then only values that the user actually changed will be updated in the DB
UPDATE Characters SET character_name = {{character_name}}, race = {{race}}, class = {{class}}, creature_type = {{creature_type}}, alignment = {{alignment}} WHERE character_id = {{character_id}};

-- for when a user deletes a char
DELETE FROM Characters WHERE character_id = {{character_id}}


-- *****************************************************************************
-- Queries that act on Spells/Abilities Page  --
-- *****************************************************************************

-- display all Spells when no character is selected
SELECT Characters.character_name, Spells.spell_name, Spells.spell_damage FROM Characters INNER JOIN Characters_has_Spells ON Characters.character_id = Characters_has_Spells.Characters_character_id INNER JOIN Spells ON Characters_has_Spells.Spells_spell_id = Spells.spell_id;

-- displays Spells when char {{character_id}} is selected
SELECT Characters.character_name, Spells.spell_name, Spells.spell_damage FROM Characters INNER JOIN Characters_has_Spells ON Characters.character_id = Characters_has_Spells.Characters_character_id INNER JOIN Spells ON Characters_has_Spells.Spells_spell_id = Spells.spell_id WHERE Characters.character_id = {{character_id}};

-- displays all Abilities when no char is selected
SELECT Characters.character_name, Abilities.ability_name, Abilities.ability_damage, Dungeons.dungeon_name FROM Characters INNER JOIN Characters_has_Abilities ON Characters.character_id = Characters_has_Abilities.Characters_character_id INNER JOIN Abilities ON Characters_has_Abilities.Ability_ability_id = Abilities.ability_id INNER JOIN Dungeons ON Abilities.Dungeons_dungeon_id = Dungeons.dungeon_id;

-- displays Abilities when char {{character_id}} is selected
SELECT Characters.character_name, Abilities.ability_name, Abilities.ability_damage, Dungeons.dungeon_name FROM Characters INNER JOIN Characters_has_Abilities ON Characters.character_id = Characters_has_Abilities.Characters_character_id INNER JOIN Abilities ON Characters_has_Abilities.Ability_ability_id = Abilities.ability_id INNER JOIN Dungeons ON Abilities.Dungeons_dungeon_id = Dungeons.dungeon_id WHERE Characters.character_id = {{character_id}};

-- for creating a new Spell
INSERT INTO Spells (spell_name, spell_damage) VALUES (spell_name = {{spell_name}}, spell_damage = {{spell_damage}});

-- for creating a new Ability
INSERT INTO Abilities (ability_name, ability_damage, Dungeons_dungeon_id) VALUES (ability_name = {{ability_name}}, ability_damage = {{ability_damage}}, Dungeons_dungeon_id = {{Dungeons_dungeon_id}});


-- *****************************************************************************
-- Queries that act on dungeonSelection Page  --
-- *****************************************************************************

-- for loading all Dungeons in the “All Dungeons” list
SELECT dungeon_name FROM Dungeons ORDER BY dungeon_name ASC;

-- this displays the user’s username in “User007’s Dungeons”
SELECT username FROM User_Accounts WHERE user_id = {{user_id}};

-- for loading only this user’s Dungeons (via attachments to the abilities that this user’s chars have) in the “My Dungeons” list
SELECT dungeon_name, dungeon_type, dungeon_description, damage_multiplier FROM Dungeons INNER JOIN Abilities ON Dungeons.dungeon_id = Abilities.Dungeons_dungeon_id INNER JOIN Characters_has_Abilities ON Abilities.ability_id = Characters_has_Abilities.Abilities_ability_id INNER JOIN Characters ON Characters_has_Abilities.Characters_character_id = Characters.character_id INNER JOIN User_Accounts ON Characters.Users_user_id = User_Accounts.user_id WHERE User_Accounts.user_id = {{user_id}};

-- for Dungeon creation
INSERT INTO Dungeons (dungeon_name, dungeon_type, dungeon_description, damage_multiplier) VALUES (dungeon_name = {{dungeon_name}}, dungeon_type = {{dungeon_type}}, dungeon_description = {{dungeon_description}}, damage_multiplier = {{damage_multiplier}});

-- for when the user updates a Dungeon, previous values can be pre-loaded into the Edit form that the user submits, then only values that the user actually changed will be updated in the DB
UPDATE Dungeons SET dungeon_name = {{dungeon_name}}, dungeon_type = {{dungeon_type}}, dungeon_description = {{dungeon_description}}, damage_multiplier = {{damage_multiplier}} WHERE dungeon_id = {{dungeon_id}};

-- for deleting from the dungeon table
DELETE FROM Dungeons WHERE dungeon_id = {{dungeon_id}};


-- *****************************************************************************
-- Queries that act on dungeonPage  --
-- *****************************************************************************

-- for loading the Dungeon name into the “Dungeon Sprite” section
SELECT dungeon_name FROM Dungeons WHERE dungeon_id = {{dungeon_id}};

-- for loading the Dungeon name into the “Dungeon Description” section
SELECT dungeon_description FROM Dungeons WHERE dungeon_id = {{dungeon_id}};

-- for loading the dungeon details into the "Dungeon Details" section
SELECT dungeon_type, damage_multiplier FROM Dungeons WHERE dungeon_id = {{dungeon_id}};


-- *****************************************************************************
-- Queries that act on itemPage  --
-- *****************************************************************************

-- for loading the Item name into the “Item Sprite” section
SELECT item_name FROM Items WHERE item_id = {{item_id}};

-- for loading the Item description into the “Item Description” section
SELECT item_description FROM Items WHERE item_id = {{item_id}};

-- for loading the Item weapon info into the “Item Info” section
SELECT is_weapon FROM Items WHERE item_id = {{item_id}};


-- ********************************************************************
-- Queries that act on Items Page  --
-- ********************************************************************

-- case 1 -- User views Items Table/Page causing a GET request --
-- generate Items table:
SELECT Items.item_id, Items.item_name, Items.item_description, Items.is_weapon FROM Items;

-- case 2 -- User clicks "insert" button to INSERT a new Item:
INSERT INTO Items (item_name, item_description, is_weapon) VALUES ({{item_name_input}},{{item_desc_input}},{{is_weapon_dropdown}});


-- ********************************************************************
-- Queries that act on itemSelection Page  --
-- ********************************************************************

-- User views Inventory_Items Table/Page causing a GET request --
-- generate complete inventory table for all users:
SELECT Characters.character_name, Items.item_name, Items.item_description, Inventory_Items.quantity,
       Inventory_Items.inventory_id, Items.item_id, Characters.character_id
from Characters
INNER JOIN Inventory_Items ON Characters.character_id=Inventory_Items.Characters_character_id
INNER JOIN Items ON Inventory_Items.Items_item_id=Items.item_id
ORDER BY Characters.character_name ASC;

-- generate custom inventory table for current user:
SELECT
User_Accounts.username, Characters.character_name, Items.item_name, Items.item_description,Inventory_Items.quantity, Items.item_id
from User_Accounts
INNER JOIN Characters on User_Accounts.user_id=Characters.Users_user_id
INNER JOIN Inventory_Items ON Characters.character_id=Inventory_Items.Characters_character_id
INNER JOIN Items ON Inventory_Items.Items_item_id=Items.item_id
WHERE User_Accounts.username='{{username}}';

-- Enable dynamic drop down menus to select character and item
-- for <form> on bottom of page:
SELECT Characters.character_id, Characters.character_name FROM Characters;
SELECT SELECT Items.item_id, Items.item_name FROM Items;

-- User clicks "X" button to DELETE an Inventory_Item:
DELETE FROM Inventory_Items
WHERE Inventory_Items.inventory_id='{{inventory_id_from_cur_row}}';

-- User clicks "update" button to UPDATE a row
-- (Update for 3 tables: Items, Inventory_Items, Characters)
UPDATE Characters, Inventory_Items, Items
SET
    Characters.character_name='{{input_character_name_cur_row}}',
    Inventory_Items.quantity={{input_quantity_cur_row}},
    Items.item_name='{{input_item_name_cur_row}}',
    Items.item_description='{{input_description_cur_row}}'
WHERE Items.item_id=Inventory_Items.Items_item_id
AND Characters.character_id=Inventory_Items.Characters_character_id
AND Inventory_Items.inventory_id='{{inventory_id_of_row_clicked}}';
;

-- User clicks "INSERT" button to INSERT a new Inventory_Item for a Character:
INSERT INTO Inventory_Items (Characters_character_id, Items_item_id, quantity)
VALUES ({{char_id_from_dropdown}},{{item_id_from_dropdown}},{{qty_from_input_form}});


-- ********************************************************************
-- Queries that act on "Reload Database" button:     --
-- ********************************************************************
-- Execute all statements in schema (ddl.sql) again to reset DB to default.

