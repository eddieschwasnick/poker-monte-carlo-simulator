import random

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

def draw_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

def deal_flop(deck):
    return [draw_card(deck) for _ in range(3)]

def deal_turn(deck):
    return draw_card(deck)

def deal_river(deck):
    return draw_card(deck)

def evaluate_hand_strength(hand):
    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
             '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    rank_counts = {}
    for card in hand:
        value = ranks[card[:-1]]
        rank_counts[value] = rank_counts.get(value, 0) + 1

    sorted_ranks = sorted(rank_counts.items(), key=lambda x: (-x[1], -x[0]))
    score = 0
    for i, (rank, count) in enumerate(sorted_ranks):
        score += (15 ** (4 - i)) * count * rank  # weighting most significant cards more
    return score

def simulate_games(player_cards, num_simulations=10000):
    suits = ['H', 'D', 'C', 'S']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    full_deck = [rank + suit for rank in ranks for suit in suits]

    wins, ties, losses = 0, 0, 0

    for _ in range(num_simulations):
        deck = full_deck[:]
        for card in player_cards:
            deck.remove(card)
        deck = shuffle_deck(deck)

        opp_cards = [draw_card(deck), draw_card(deck)]
        flop = deal_flop(deck)
        turn = deal_turn(deck)
        river = deal_river(deck)
        community = flop + [turn, river]

        player_strength = evaluate_hand_strength(player_cards + community)
        opp_strength = evaluate_hand_strength(opp_cards + community)

        if player_strength > opp_strength:
            wins += 1
        elif player_strength < opp_strength:
            losses += 1
        else:
            ties += 1

    total = wins + losses + ties
    return wins / total, ties / total, losses / total

# Ask user for input
print("Enter your two cards (e.g. 'AH' for Ace of Hearts):")
card1 = input("Card 1: ").strip().upper()
card2 = input("Card 2: ").strip().upper()
player_cards = [card1, card2]

win_prob, tie_prob, loss_prob = simulate_games(player_cards)

print(f"Win Probability:  {win_prob:.4f}")
print(f"Tie Probability:  {tie_prob:.4f}")
print(f"Loss Probability: {loss_prob:.4f}")
