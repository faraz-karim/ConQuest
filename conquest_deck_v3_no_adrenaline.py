import os
import random

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class GameDecks:
    def __init__(self):
        self.item_deck = []
        self.item_discard = []
        self.event_deck = []
        self.event_discard = []
        self.std_monster_deck = []
        self.std_monster_discard = []
        self.boss_monster_deck = []
        self.boss_monster_discard = []
        self.shop_inventory = []
        
        self.initialize_decks()
        self.restock_shop()

    def initialize_decks(self):
        # BALANCED ITEM DECK 
        items_config = [
            ("Greatsword", 4, "Combat: 35 Damage (Costs 3 AP). Discard after."),
            ("Crossbow", 5, "Combat: 25 Damage (Costs 2 AP). Ranged. Discard after."),
            ("Enchanted Longbow", 2, "Combat: 30 Damage (Costs 2 AP). Long Range."),
            ("Assassin's Dagger", 3, "Combat: 15 Damage (Costs 1 AP). Bypasses armor."),
            ("Steel Shield", 5, "Defend: Block 50% of incoming damage this round (Costs 1 AP)."),
            ("Magic Armor", 2, "Passive: -2 dmg from all hits. Breaks at 15+ dmg."),
            ("Invisibility Dust", 3, "Utility: Cancel the round immediately, move back 1 space."),
            ("Essence of Life", 7, "Heal: +20 HP (Costs 2 AP)."),
            ("Phoenix Tears", 3, "Heal: +40 HP (Costs 2 AP)."),
            ("Antidote Potion", 4, "Utility: Cure Poison/Slow +5 HP (Costs 1 AP)."),
            ("Explosive Rune", 3, "Trap: 20 Damage to next player on this tile."),
            ("Slow Spell", 3, "Slow: Target moves 1d6 next turn."),
            ("Magic Boots", 3, "Move: Add +3 to your movement roll."),
            ("Teleport Spell", 3, "Move: Jump to player up to 6 tiles ahead.")
        ]
        for name, qty, effect in items_config:
            for _ in range(qty):
                self.item_deck.append({"name": name, "effect": effect})
        
        # BOSSES - Values tuned for Simultaneous Resolution
        self.boss_monster_deck = [
            {"name": "The Stone Golem", "hp": 70, "mechanic": "Takes 0 Damage from basic Punches.", "penalty": "20 dmg & Move back 5 tiles.", 
             "action_text": "Smashes the ground!", "action_dmg": 15},
            {"name": "Poison Dragon", "hp": 55, "mechanic": "Any Punch/Melee attack you do deals 5 dmg to YOU.", "penalty": "15 dmg, Poisoned, Move back 5 tiles.", 
             "action_text": "Breathes Toxic Fumes!", "action_dmg": 15},
            {"name": "Dark Wizard", "hp": 50, "mechanic": "You CANNOT use the 'Defend' action.", "penalty": "10 dmg & Discard 2 Items.", 
             "action_text": "Casts Decay Bolt!", "action_dmg": 20},
            {"name": "Black Knight", "hp": 65, "mechanic": "Completely Immune to damage on Even rounds (2, 4).", "penalty": "25 dmg & Move back 5 tiles.", 
             "action_text": lambda r: "Heavy Slash!" if r%2!=0 else "Raises Shield Wall! (Immune)", "action_dmg": lambda r: 25 if r%2!=0 else 0},
            {"name": "Illusion Wizard", "hp": 45, "mechanic": "Roll 1d6 when attacking: 1-2 misses completely (0 dmg).", "penalty": "15 dmg & Move back 5 tiles.", 
             "action_text": "Casts Magic Blast!", "action_dmg": 15}
        ]
        
        std_monsters_config = [
            ("Goblin Thief", "Target: 3", "Take 10 Dmg.", "Draw 1 Card."),
            ("Giant Spider", "Target: 4", "Take 5 Dmg + Poisoned.", "Draw 1 Card."),
            ("Dire Wolf", "Target: 4", "Take 15 Dmg.", "Draw 1 Card."),
            ("Orc", "Target: 5", "Take 10 Dmg + Discard 1 Card.", "Draw 1 Card."),
            ("Acid Slime", "Target: 3", "Take 10 Dmg.", "Restore 15 HP."),
            ("Skeleton Warrior", "Target: 5", "Take 20 Dmg.", "Draw 2 Cards, keep 1.")
        ]
        for name, target, penalty, reward in std_monsters_config:
            for _ in range(4):
                self.std_monster_deck.append({"name": name, "target": target, "penalty": penalty, "reward": reward})

        self.event_deck = [{"name": "Fate Event", "effect": "Draw 1 Card."}] * 15 
        
        random.shuffle(self.item_deck)
        random.shuffle(self.boss_monster_deck)
        random.shuffle(self.std_monster_deck)

    def restock_shop(self):
        while len(self.shop_inventory) < 3 and self.item_deck:
            self.shop_inventory.append(self.item_deck.pop(0))

    def merchant_action(self):
        print("--- THE MERCHANT'S STATIC SHOP ---")
        print("Cost: Discard any 2 cards from your hand to take 1.")
        print("-" * 35)
        for i, item in enumerate(self.shop_inventory):
            print(f"{i+1}. {item['name']} - {item['effect']}")
        
        print("\n0. Exit Shop")
        choice = input("\nSelect an item (1-3): ")
        if choice in ['1', '2', '3']:
            idx = int(choice) - 1
            bought_item = self.shop_inventory.pop(idx)
            self.restock_shop()
            clear_screen()
            print(f"[+] You traded 2 cards for: {bought_item['name']}")
        else:
            clear_screen()

    def interactive_boss_fight(self, boss):
        print(f"!!! BOSS: {boss['name'].upper()} ({boss['hp']} HP) !!!")
        print(f"Rules: {boss['mechanic']}")
        print(f"Escape Penalty: {boss['penalty']}")
        hp = boss['hp']
        round_n = 1
        
        while hp > 0:
            print(f"\n[ROUND {round_n}] Boss HP: {hp}")
            
            # Check if action_text and action_dmg are callable (for the Black Knight's alternating rounds)
            b_text = boss['action_text'](round_n) if callable(boss['action_text']) else boss['action_text']
            b_dmg_val = boss['action_dmg'](round_n) if callable(boss['action_dmg']) else boss['action_dmg']
            
            print(f"Boss readies attack: {b_text} ({b_dmg_val} Incoming Damage)")
            print("\nYour Turn (3 AP Max). Options: Attack, Defend, Heal, or Flee.")
            
            move = input("Enter Damage you are dealing (or type 'flee'): ").lower()
            if move == 'flee':
                print(f"\nEscaped! {boss['penalty']}")
                self.boss_monster_discard.append(boss)
                return
            
            defended = input("Did you spend 1 AP to Defend this round? (y/n): ").lower() == 'y'
            
            try:
                p_dmg = int(move)
            except ValueError:
                p_dmg = 0

            # SIMULTANEOUS RESOLUTION
            clear_screen()
            print(f"--- ROUND {round_n} CLASH ---")
            
            # 1. Player deals damage to Boss
            hp -= p_dmg
            print(f"-> You struck the Boss for {p_dmg} damage.")
            
            # 2. Boss deals damage to Player
            final_incoming_dmg = b_dmg_val
            if defended and b_dmg_val > 0:
                final_incoming_dmg = b_dmg_val // 2
                print(f"-> You raised your guard! Incoming damage halved.")
                
            print(f"-> The Boss struck you for {final_incoming_dmg} damage.")
            
            # 3. Check for mutual destruction
            if hp <= 0:
                print("\n" + "*"*30)
                print(f"THE DUST SETTLES... YOU DEFEATED {boss['name']}!")
                if final_incoming_dmg > 0:
                    print(f"(But you still took {final_incoming_dmg} damage in the final clash!)")
                print("*"*30)
                self.boss_monster_discard.append(boss)
                return

            round_n += 1

    def draw_standard_monster(self):
        if not self.std_monster_deck:
            self.std_monster_deck.extend(self.std_monster_discard)
            self.std_monster_discard.clear()
            random.shuffle(self.std_monster_deck)
            
        card = self.std_monster_deck.pop(0)
        print(f"--- MONSTER ENCOUNTER ---")
        print(f"Enemy: {card['name']}")
        print(f"Roll Needed: {card['target']} (on 1d6)")
        print(f"Penalty: {card['penalty']}")
        print(f"Reward: {card['reward']}")
        self.std_monster_discard.append(card)

    def draw_item(self):
        if self.item_deck:
            card = self.item_deck.pop(0)
            print(f"--- RELIC DRAWN ---\n{card['name']}\n{card['effect']}")
            self.item_discard.append(card)

    def show_quick_rules(self):
        print("========================================")
        print("           QUICK REFERENCE GUIDE        ")
        print("========================================")
        print("\n[ ITEM SACRIFICE (Hand Management) ]")
        print("  • Discard 1 Card: +1 or -1 to movement roll.")
        print("  • Discard 2 Cards: Evade a Trap (Take no penalty).")
        
        print("\n[ SIMULTANEOUS COMBAT (3 AP Per Round) ]")
        print("Both players reveal their actions at the exact same time. Damage is taken simultaneously.")
        print("  • Punch (1 AP): Deal 10 Damage.")
        print("  • Desperate Throw (1 AP): Discard 1 card to deal 15 Damage.")
        print("  • Defend (1 AP): Reduce all incoming damage this round by 50%.")
        print("  • Use Weapon (2-3 AP): Read card for damage. Discard after.")
        print("  • Heal: 2 AP on the board. 3 AP inside the Arena.")
        
        print("\n[ PVP TIE-BREAKER ]")
        print("  • If both players drop to 0 HP in the exact same round, roll 1d6. Highest survives with 1 HP.")
        print("========================================\n")

    def main_menu(self):
        while True:
            clear_screen()
            print("========================================")
            print("   BATTLE ARENA: DIGITAL DM (v5.0)      ")
            print("========================================")
            print("1. Draw RELIC (Treasure Cache)")
            print("2. Draw MONSTER (Skull Tile)")
            print("3. Draw BOSS (Gatekeeper Tile)")
            print("4. Visit THE MERCHANT (Shop)")
            print("5. View Quick Rules")
            print("0. Quit")
            
            c = input("\nChoice: ")
            if c == '0': break
            clear_screen()
            
            if c == '1': self.draw_item()
            elif c == '2': self.draw_standard_monster()
            elif c == '3':
                if self.boss_monster_deck:
                    self.interactive_boss_fight(self.boss_monster_deck.pop(0))
                else:
                    print("All Bosses Defeated! Reshuffling...")
                    self.boss_monster_deck.extend(self.boss_monster_discard)
                    self.boss_monster_discard.clear()
                    random.shuffle(self.boss_monster_deck)
            elif c == '4': self.merchant_action()
            elif c == '5': self.show_quick_rules()
            
            input("\nPress Enter to return...")

if __name__ == "__main__":
    GameDecks().main_menu()