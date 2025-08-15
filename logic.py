from hvs import *
from PyQt6.QtWidgets import *
import csv, random
from typing import Tuple

class NameShortError(Exception):
    pass

class NameLongError(Exception):
    pass

class WeaponError(Exception):
    pass

class Logic(QMainWindow, Ui_HeroVS):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the main window and sets up connections.

        Initializes instance variables for wins and losses, and sets up
        QButtonGroups for the radio buttons to ensure weapon choices are cleared
        when the round finishes.
        """
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.fightbutt.clicked.connect(self.final_statement)

        self.hwins = 0
        self.hlosses = 0
        self.vwins = 0
        self.vlosses = 0

        self.hstatbutt = QButtonGroup(self)
        self.hstatbutt.addButton(self.hsword)
        self.hstatbutt.addButton(self.hbook)
        self.hstatbutt.addButton(self.hbow)

        self.vstatbutt = QButtonGroup(self)
        self.vstatbutt.addButton(self.vsword)
        self.vstatbutt.addButton(self.vbook)
        self.vstatbutt.addButton(self.vbow)

    def weapon_check(self) -> Tuple[str, str]:
        """
        Determines the chosen weapon for the hero and villain.
        Raises WeaponError if a weapon is not selected for either player.
        """
        hchoice: str
        vchoice: str
        if self.hsword.isChecked():
            hchoice="sword"
        elif self.hbow.isChecked():
            hchoice="bow"
        elif self.hbook.isChecked():
            hchoice="book o' spells"
        else:
            raise WeaponError

        if self.vsword.isChecked():
            vchoice="sword"
        elif self.vbow.isChecked():
            vchoice="bow"
        elif self.vbook.isChecked():
            vchoice="book o' spells"
        else:
            raise WeaponError

        return hchoice, vchoice

    def dam_calc(self, choice: str) -> int:
        """
        Calculates a random damage value based on the weapon chosen.
        """
        damage: int = 0

        if choice == "sword":
            damage = random.randint(2,10) * random.randint(2,3)
        elif choice == "bow":
            damage = random.randint(1,15) * random.randint(1,3)
        elif choice == "book o' spells":
            damage = random.randint(2,20) * random.randint(0,3)
        else:
            raise WeaponError

        return damage

    def name_check(self) -> Tuple[str, str]:
        """
        Checks the length of the hero's and villain's names.
        Raises NameShortError if either name is empty, or NameLongError
        if either name is too long.
        """
        hname: str = self.hname.text().strip()
        vname: str = self.vname.text().strip()

        if len(hname) < 1 or len(vname) < 1:
            raise NameShortError()
        elif len(hname) > 10 or len(vname) > 10:
            raise NameLongError()
        return hname, vname

    def winning_check(self, hdam: int, vdam: int) -> str:
        """
        Compares the hero's and villain's damage to determine the winner.
        In the event of a tie, the string "tie" will be returned so the game is aware.
        """
        if hdam > vdam:
            return self.hname.text().strip()
        elif vdam > hdam:
            return self.vname.text().strip()
        return "tie"

    def win_loss_count(self, winner: str) -> None:
        """
        Updates the win/loss counters and their corresponding labels on the GUI.
        """
        if winner == self.hname.text().strip():
            self.hwins += 1
            self.vlosses += 1
            self.hwin.setText(f"Wins: {self.hwins}")
            self.vloss.setText(f"Losses: {self.vlosses}")
        elif winner == self.vname.text().strip():
            self.vwins += 1
            self.hlosses += 1
            self.vwin.setText(f"Wins: {self.vwins}")
            self.hloss.setText(f"Losses: {self.hlosses}")

    def final_statement(self) -> None:
        """
        This is the main logic for the 'Fight!' button.

        Once the button is pressed, the game runs through all of the methods and collects the info.
        If an error is raised, the game will stop and let the players know what to correct before the program can finish.
        """
        try:
            hname, vname = self.name_check()
            hchoice, vchoice = self.weapon_check()
            hdam = self.dam_calc(hchoice)
            vdam = self.dam_calc(vchoice)
            winner = self.winning_check(hdam, vdam)

            if winner != "tie":
                self.outcome.setText(f"{hname} strikes {vname} for {hdam} damage. {vname} strikes {hname} for {vdam} damage. {winner} wins!")
                self.win_loss_count(winner)

                self.hstatbutt.setExclusive(False)
                self.vstatbutt.setExclusive(False)

                self.hsword.setChecked(False)
                self.hbook.setChecked(False)
                self.hbow.setChecked(False)
                self.vsword.setChecked(False)
                self.vbook.setChecked(False)
                self.vbow.setChecked(False)
            else:
                self.outcome.setText(f"What a twist! {hname} and {vname} both strike each other for {hdam} damage. It's a tie!")

                self.hsword.setChecked(False)
                self.hbook.setChecked(False)
                self.hbow.setChecked(False)
                self.vsword.setChecked(False)
                self.vbook.setChecked(False)
                self.vbow.setChecked(False)
            with open('data.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([hname, hchoice, hdam, vname, vchoice, vdam])
        except NameShortError:
            self.outcome.setText("Battles cannot be retold without names. Please type a name.")
        except NameLongError:
            self.outcome.setText("Legends cannot remember names that long. Please shorten your name.")
        except WeaponError:
            self.outcome.setText("You need a weapon to survive in this world. Please choose one.")