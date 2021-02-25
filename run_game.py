import sys
import argparse

from game.ai_runner import AIRunner
from game.game import Game

# TODO: aggiungere opzione -h (help)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ai", type=str, default="dummy", help="which bot to use [alphahanabi | deltahanabi | dummy | extremehanabi | superhanabi]")
    parser.add_argument("--num_players", "-n", type=int, default=5, help="Number of players in the game")
    parser.add_argument("--difficulty", "-p", type=str, default="hardest", help="[medium | hard | hardest]")
    parser.add_argument("--no_pause", "-c", action="store_false", help="run the game without pausing")
    parser.add_argument("--strategy_log", "-s", action="store_false", help="activate the strategy log")
    parser.add_argument("--shorter_log", "-t", action="store_true", help="print a shorter log of turns and status")
    parser.add_argument("--load_deck", "-l", type=str, default=None, help="load starting deck from a file")
    parser.add_argument("--save_deck", "-d", type=str, default="deck.txt", help="file name to save starting deck to")
    parser.add_argument("--repeat", "-r", type=int, default=None, help="run many games, until a score <= to the given score is reached")
    parser.add_argument("--interactive", "-i", action='store_true', help="run in interactive mode")
    parser.add_argument("--print_setup", "-q", action='store_true', help="quit immediately after showing the initial cards")
    parser.add_argument("--deck_type", type=str, default="deck50", help="variant to use [deck50, deck55]")
    args = parser.parse_args()

    # default values
    ai = args.ai
    ai_params = {}
    wait_key = args.no_pause
    num_players = args.num_players
    log = True
    strategy_log = args.strategy_log
    dump_deck_to = args.save_deck
    load_deck_from = args.load_deck
    short_log = args.shorter_log
    interactive = args.interactive
    quit_immediately = args.print_setup
    DECK_TYPE = args.deck_type
    repeat = args.repeat  # repeat until a bad result is reached

    counter = 0
    while True:
        # run game
        print("Starting game with %d players..." % num_players)
        print()

        game = Game(
            num_players=num_players,
            load_deck_from=load_deck_from,
            deck_type=DECK_TYPE
        )

        ai_runner = AIRunner(
            game=game,
            ai=ai,
            ai_params=ai_params,
            strategy_log=strategy_log
        )

        if interactive:
            # run in interactive mode
            from blessings import Terminal

            def print_main(term, num_players, ai, ai_params, short_log, turn=None, current_player=None, statistics=None):
                """
                Print main view.
                """
                CURSOR_Y = term.height - 15

                # clear everything
                print(term.clear())

                # move cursor
                print(term.move_y(CURSOR_Y))

                with term.location(y=0):
                    print(term.bold("Hanabi game"))

                with term.location(y=2):
                    print("Number of players: %d" % num_players)
                    print("AI: %s" % ai)
                    if "difficulty" in ai_params:
                        print("Difficulty: %s" % ai_params["difficulty"])
                    if load_deck_from is not None:
                        print("Deck file: %s" % load_deck_from)

                if turn is not None:
                    # log turn
                    with term.location(y=7):
                        if short_log:
                            game.log_turn_short(turn, current_player)
                        else:
                            game.log_turn(turn, current_player)

                    # log status
                    with term.location(y=9):
                        if short_log:
                            game.log_status_short()
                        else:
                            game.log_status()

                if statistics is not None:
                    # game ended
                    with term.location(y=9+10):
                        print(term.bold("Game ended"))
                        print(statistics)


            term = Terminal()
            with term.fullscreen():
                print_main(term, num_players, ai, ai_params, short_log)

                for current_ai_player, turn in game.run_game():
                    if wait_key:
                        cmd = input(":")
                        if cmd in ["c", "continue"]:
                            wait_key = False

                    print_main(term, num_players, ai, ai_params, short_log, turn=turn, current_player=current_ai_player)


                statistics = game.statistics
                print_main(term, num_players, ai, ai_params, short_log, turn=turn, current_player=current_ai_player, statistics=statistics)

                while True:
                    cmd = input(":")
                    print_main(term, num_players, ai, ai_params, short_log, turn=turn, current_player=current_ai_player, statistics=statistics)

                    if cmd in ["q", "quit"]:
                        break

                    else:
                        with term.location(y = term.height - 4):
                            # print "Unknown command \"%s\"" % cmd
                            pass


        else:
            # non-interactive mode
            if dump_deck_to is not None:
                print("Dumping initial deck to %s" % dump_deck_to)

            if not short_log:
                game.log_deck()
                game.log_status()

            if quit_immediately:
                break

            # now run the game
            for current_ai_player, turn in ai_runner.run_game():
                if wait_key:
                    input()
                if short_log:
                    game.log_turn_short(turn, current_ai_player)
                    game.log_status_short()
                else:
                    ai_runner.log_turn(turn, current_ai_player)
                    game.log_status()

            statistics = ai_runner.statistics
            print(statistics)


        counter += 1

        if repeat is None:
            break

        elif statistics.score <= repeat:
            print("Reached score <= %d after %d games" % (repeat, counter))
            break

        else:
            print()
            print("==========================")
            print()
