from game.card import get_appearance


class AIPlayer:
    """
    A Player class works as a wrapper around the Strategy class of the corresponding player.
    In particular, it has to take care of hiding information not known to the player.
    """

    def __init__(self, id, ai_runner, player, ai, ai_params, strategy_log=False):
        # my id (order of play)
        self.id = id

        # game
        self.ai_runner = ai_runner
        self.game = ai_runner.game

        # initial hand of cards
        self.player = player

        # AI to be used, with parameters
        self.ai = ai
        self.ai_params = ai_params

        # create strategy object
        Strategy = __import__('ai.%s.strategy' % self.ai, globals(), locals(), fromlist=['Strategy'], level=1).Strategy

        self.strategy = Strategy(verbose=strategy_log, params=ai_params)

    def next_player(self):
        return self.ai_runner.ai_players[(self.id + 1) % self.game.num_players]

    def other_players(self):
        return {i: ai_player for (i, ai_player) in enumerate(self.ai_runner.ai_players) if ai_player != self}


    def initialize(self):
        # called once after all players are created, before the game starts
        self.initialize_strategy()


    def initialize_strategy(self):
        """
        To be called once before the beginning.
        """
        self.strategy.initialize(
            id = self.id,
            num_players = self.game.num_players,
            k = self.game.k,
            board = self.game.board,
            deck_type = self.game.deck_type,
            my_hand = get_appearance(self.player.hand, hide=True),
            hands = {i: get_appearance(ai_player.player.hand) for (i, ai_player) in self.other_players().items()},
            discard_pile = get_appearance(self.game.discard_pile),
            deck_size = len(self.game.deck)
        )
        self.update_strategy()

    def update_strategy(self):
        """
        To be called immediately after every turn.
        """
        self.strategy.update(
            hints = self.game.hints,
            lives = self.game.lives,
            my_hand = get_appearance(self.player.hand, hide=True),
            hands = {i: get_appearance(ai_player.player.hand) for (i, ai_player) in self.other_players().items()},
            discard_pile = get_appearance(self.game.discard_pile),
            turn = self.game.get_current_turn(),
            last_turn = self.game.last_turn,
            deck_size = len(self.game.deck)
        )


    def get_turn_action(self):
        # update strategy (in case this is the first turn)
        self.update_strategy()

        # choose action for this turn
        action = self.strategy.get_turn_action()
        action.apply(self.game)
        return action


    def feed_turn(self, turn):
        # update strategy
        self.update_strategy()

        # pass information about what happened during the turn
        self.strategy.feed_turn(turn.player.id, turn.action)