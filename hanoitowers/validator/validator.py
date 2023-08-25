from hanoitowers.config.constants import (
    GAMES_TO_PLAY_MAX,
    TURN_MAX_TIME_SECS_MIN, TURN_MAX_TIME_SECS_MAX,
    LOG_INPUT_ERROR_PREFIX_MSG,
    HANOY_MIN_DISCS, HANOY_MAX_DISCS,
    HANOY_SOLVERS,
)


class InputValidator:

    def __init__(self, games_to_play, turn_max_secs, hanoy_discs, solver):
        self.games_to_play = games_to_play
        self.turn_max_secs = turn_max_secs
        self.hanoy_discs = hanoy_discs
        self.solver = solver
        self.input_errors = []

    def validate_input(self):
        self.validate_games_to_play()
        self.validate_turn_max_secs()
        self.validate_disc_number()
        self.validate_solver()
        return self.input_errors

    def validate_games_to_play(self):
        if self.games_to_play is None:
            return
        if not (0 <= self.games_to_play <= GAMES_TO_PLAY_MAX):
            self.input_errors += [
                    f"{LOG_INPUT_ERROR_PREFIX_MSG}"
                    f"Games to play on each tournament must be between 2 and {GAMES_TO_PLAY_MAX}"]

    def validate_turn_max_secs(self):
        if self.turn_max_secs is None:
            return
        if not (TURN_MAX_TIME_SECS_MIN <= self.turn_max_secs <= TURN_MAX_TIME_SECS_MAX):
            self.input_errors += [
                    f"{LOG_INPUT_ERROR_PREFIX_MSG}"
                    f"Turn max seconds for game must be between {TURN_MAX_TIME_SECS_MIN} and {TURN_MAX_TIME_SECS_MAX}."]

    def validate_disc_number(self):
        if self.hanoy_discs is None:
            return
        if not (HANOY_MIN_DISCS <= self.hanoy_discs <= HANOY_MAX_DISCS):
            self.input_errors += [
                    f"{LOG_INPUT_ERROR_PREFIX_MSG}"
                    f"Hanoi discs must be between {HANOY_MIN_DISCS} and {HANOY_MAX_DISCS}"]

    def validate_solver(self):
        if not self.solver:
            return

        if self.solver not in HANOY_SOLVERS:
            self.input_errors += [
                    f"{LOG_INPUT_ERROR_PREFIX_MSG}"
                    f"Unexpected solver: {self.solver}. Available solvers: {', '.join(HANOY_SOLVERS)}"]
