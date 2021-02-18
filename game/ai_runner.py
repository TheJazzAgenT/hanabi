from game.action import Action
from game.ai_player import AIPlayer
from game.game import Statistics


class AIRunner:
    def __init__(self, game, ai="alphahanabi", ai_params={}, strategy_log=False):
        self.game = game
        self.ai_players = [AIPlayer(id=count, ai_runner=self, player=player, ai=ai, ai_params=ai_params, strategy_log=strategy_log)
                        for count, player in enumerate(game.players)]

        # call players' initializations
        for ai_player in self.ai_players:
            ai_player.initialize()

    def run_turn(self, ai_player):
        action = ai_player.get_turn_action()
        return self.game.run_turn(ai_player.player, action)

    def run_game(self):
        """
        Run the game, yielding (current_player, turn) after each turn.
        At the end, save statistics about the game.
        """
        self.end_game = False
        current_ai_player = self.ai_players[0]

        while not self.end_game:
            # do turn
            turn, self.end_game = self.run_turn(current_ai_player)

            # temporarily store this turn, for get_current_status()
            self.this_turn = turn

            # yield current player and turn
            yield current_ai_player, turn

            # inform all players
            for player in self.ai_players:
                player.feed_turn(turn)

            # change current player
            current_ai_player = current_ai_player.next_player()

        self.statistics = Statistics(
            score = self.game.get_current_score(),
            lives = self.game.lives,
            hints = self.game.hints,
            num_turns = len(self.game.turns)
        )

    def log_turn(self, turn, ai_player):
        action = turn.action
        print("Turn %d (player %d):" % (turn.number, ai_player.id), end=' ')
        if action.type in [Action.PLAY, Action.DISCARD]:
            print(action.type, self.game.discard_pile[-1], "(card %d)," % action.card_pos, end=' ')
            print("draw %r" % ai_player.player.hand[action.card_pos])

        elif action.type == Action.HINT:
            print(action.type, end=' ')
            print("to player %d," % action.player_id, end=' ')
            print("cards", action.cards_pos, end=' ')
            print("are", end=' ')
            print(action.value)

        print()