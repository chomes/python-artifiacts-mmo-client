from python_artifacts_mmo_client.game_master_client import GMClient
from python_artifacts_mmo_client.character_client import (
    CharacterClient,
    NoCharactersExistError,
    CreateCharacterError,
    InvalidCharacterError
)
import sys
from python_artifacts_mmo_client.models.character import Character
from python_artifacts_mmo_client.models.monster import Monster
from python_artifacts_mmo_client.models.drop import Drop
from python_artifacts_mmo_client.models.fight import Fight
from python_artifacts_mmo_client.models.map import Map
from python_artifacts_mmo_client.models.resource import Resource


class TerminalClient:
    """This class is the customer facing class for the client, 
    It will do the operations for the user to play the game, all business logic will be
    in the actual clients themselves rather then on the TC.
    """
    def __init__(self, game_master_client: GMClient, character_client: CharacterClient) -> None:
        self.gm_client: GMClient = game_master_client
        self.cc: CharacterClient = character_client

    def show_main_menu(self) -> None:
        server_status: dict[str, str | int] = self.gm_client.get_server_status()
        print(
            f"""
        
    #     ########  ######## ###  ######      ###    #######   ######   ######    ##     ## ###   ###  #######   
  ## ##   ##     ##    ##     ##  ##         ## ##   ##    ##    ##    ##    ##   ###   ### ###   ### ##     ## 
 ##   ##  ##     ##    ##     ##  ##        ##   ##  ##          ##    ##         #### #### #### #### ##     ## 
##     ## ########     ##     ##  ######   ##     ## ##          ##     ######    ## ### ## ## ### ## ##     ## 
######### ##   ##      ##     ##  ##       ######### ##          ##          ##   ##     ## ##     ## ##     ## 
##     ## ##    ##     ##     ##  ##       ##     ## ##    ##    ##    ##    ##   ##     ## ##     ## ##     ## 
##     ## ##     ##    ##    #### ##       ##     ##  ######     ##     ######    ##     ## ##     ##  #######
            server status: {server_status['status']}
            game version: {server_status['version']}
              
        """
        )
    
    def get_characters(self) -> None:
        """Get the list of characters and prints them out for the user
        """
        try:
            characters: list[Character] = self.cc.get_characters()
            print("Here are your characters to choose from")
            for character in characters:
                print(f"Character : {character.name}  Level: {character.level}")
        except NoCharactersExistError:
            print("You don't have a character, lets make one!")
    
    def create_new_character(self) -> Character:
        """Creates a new character for the user

        Returns:
            Character: The users newly created character
        """
        try:
            confirmation: str | None = None
            while confirmation not in ("y", "yes"):
                name: str = input("What's the name of your character? ")
                confirmation: str = input(f"You have chosen {name} as your character, is that correct? y/n").lower()
                if confirmation not in ("y", "yes"):
                    print("Ok, lets try again!")
                    continue

            skin: str | None = None
            skin_options: tuple[str] = ("men1", "men2", "men3", "women1", "women2", "women3")
            
            while skin not in skin_options:
                skin: str = input("What character skin do you want to choose?  There is ('men1', 'men2', 'men3', 'women1', 'women2', 'women3') ")
                if skin not in skin_options:
                    print(f"{skin} is not a valid character skin choice, try again!")
                    continue
            
            print(f"Ok we have the character name {name} with the skin {skin}, lets create your character!")
            character: Character = self.cc.create_character(name, skin)
            print("Character has been created!")
            return character
        except CreateCharacterError:
            print("Uh-oh we couldn't create the character, start the game with logging to find out why")
            sys.exit(1)
    
    def get_existing_character(self) -> Character:
        """Get a character to play the game

        Returns:
            Character: Character<Inosuke>
        """
        try:
            character_name: str = input("What is the character you want to get? ")
            print(f"Retrieving character: {character_name}")
            character: Character = self.cc.get_character(character_name)
            return character
        except InvalidCharacterError:
            print("Uh-oh that character doesn't seem to exist, please try again")
            sys.exit(1)
    

    

    

            

