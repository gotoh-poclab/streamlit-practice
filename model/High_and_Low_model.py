from dataclasses import dataclass, asdict
from typing import List, Literal, Optional, Dict

Choice = Literal["High", "Low"]
Outcome = Literal["win", "lose", "draw"]

@dataclass(frozen=True)
class RoundResult:
	round: int
	base_card: int
	player_choice: Choice
	result_card: int
	bet: int
	outcome: Outcome
	chips_after: int
	remaining_deck: List[int]

class GameState:
	def __init__(self, initial_chips: int = 100, deck: Optional[List[int]] = None, win_target: int = 3):
		self.initial_chips = initial_chips
		self.chips = initial_chips
		self.deck = deck[:] if deck is not None else list(range(1, 14))
		self.rounds: List[Dict] = []
		self.round_count = 0
		self.win_count = 0
		self.lose_count = 0
		self.draw_count = 0
		self.win_target = win_target

	def start_game(self, deck: Optional[List[int]] = None):
		self.__init__(initial_chips=self.initial_chips, deck=deck, win_target=self.win_target)

	def play_round(self, player_choice: Choice, bet: int) -> RoundResult:
		if len(self.deck) < 2:
			raise ValueError("デッキ不足でラウンドできません。")
		if not (1 <= bet <= self.chips):
			raise ValueError("不正なベット額です。")

		self.round_count += 1
		base_card = self._draw_card()
		result_card = self._draw_card()

		if player_choice == "High":
			if result_card > base_card:
				outcome = "win"; self.chips += bet; self.win_count += 1
			elif result_card == base_card:
				outcome = "draw"; self.draw_count += 1
			else:
				outcome = "lose"; self.chips -= bet; self.lose_count += 1
		else:  # Low
			if result_card < base_card:
				outcome = "win"; self.chips += bet; self.win_count += 1
			elif result_card == base_card:
				outcome = "draw"; self.draw_count += 1
			else:
				outcome = "lose"; self.chips -= bet; self.lose_count += 1

		rr = RoundResult(
			round=self.round_count,
			base_card=base_card,
			player_choice=player_choice,
			result_card=result_card,
			bet=bet,
			outcome=outcome,
			chips_after=self.chips,
			remaining_deck=self.deck[:],
		)
		self.rounds.append(asdict(rr))
		return rr

	def _draw_card(self) -> int:
		return self.deck.pop(0)

	def get_status(self) -> Dict:
		return {
			"initial_chips": self.initial_chips,
			"rounds": self.rounds,
			"game_end": "3 rounds finished" if self.round_count >= 3 else None,
		}

# ------------------------
# 簡易テスト（print出力）
# ------------------------
if __name__ == "__main__":
	# スライド例と同じシナリオを再現
	deck = [5, 9, 12, 13, 2, 1, 7, 8, 10, 11, 3, 4, 6]
	game = GameState(initial_chips=100, deck=deck)
	game.start_game(deck=deck)

	print("Round 1:", game.play_round("High", 10))
	print("Round 2:", game.play_round("Low", 20))
	print("Round 3:", game.play_round("Low", 30))

	print("\n最終状態:")
	print(game.get_status())
