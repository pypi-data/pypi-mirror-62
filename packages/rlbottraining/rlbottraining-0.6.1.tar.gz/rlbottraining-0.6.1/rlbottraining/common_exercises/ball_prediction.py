from dataclasses import dataclass, field
from typing import Dict, Optional, Callable, List
from threading import Thread

from rlbot.matchconfig.match_config import MatchConfig, PlayerConfig, Team
from rlbot.training.training import Pass, Fail, Grade
from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.utils.logging_utils import get_logger
from rlbot.utils.rendering.rendering_manager import RenderingManager
from rlbot.utils.structures.ball_prediction_struct import BallPrediction, Slice as BallAtTime
from rlbot.utils.structures.game_interface import GameInterface

from rlbottraining.training_exercise import TrainingExercise, Playlist
from rlbottraining.grading.grader import Grader
from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.common_graders.timeout import PassOnTimeout
from rlbottraining.match_configs import make_empty_match_config
from rlbottraining.paths import BotConfigs
from rlbottraining.rng import SeededRandomNumberGenerator

"""
This module contains exercises which does not test any bots at all!
But it does test ball prediction.
"""

################### Type Defenitions ###################

# A function which gets data from the GameInterface to predict the the ball.
PredictionFunc = Callable[[GameInterface], BallPrediction]
PredictionFunc_ = Callable[[], BallPrediction]  # This version is a closure over its data source (GameInterface).

################### Grader ###################

class FailOnInconsistentBallPrediction(Grader):
    SAMPLES_PER_SECOND = 17

    def __init__(self, prediction_func: PredictionFunc_, max_duration_seconds=2.0):
        super().__init__()
        self.prediction_func = prediction_func
        self.pass_on_timeout = PassOnTimeout(max_duration_seconds)
        self.max_duration_seconds = max_duration_seconds
        self.num_samples = int(self.max_duration_seconds * self.SAMPLES_PER_SECOND)
        self.first_sample_time = None

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        # TODO: Fail on inconsistency
        sample_times = self.get_sample_times(tick.game_tick_packet.game_info.seconds_elapsed)
        return self.pass_on_timeout.on_tick(tick)

    def get_sample_times(self, potential_first_sample_time) -> List[float]:
        if self.first_sample_time is None:
            self.first_sample_time = potential_first_sample_time
        return [
            self.first_sample_time + i * (1/self.SAMPLES_PER_SECOND)
            for i in range(self.num_samples)
        ]

    def get_samples(self, prediction: BallPrediction, sample_times: List[float]) -> List[Optional[BallAtTime]]:
        out = [None] * self.num_samples
        prediction_i = 0
        for out_i, prediction_time in enumerate(sample_times):
            # Always pick the first sample after or at the sample time.
            while (prediction_i < prediction.num_slices and
                   prediction.slices[prediction_i].game_seconds < prediction_time):
                prediction_i += 1
            if prediction_i >= prediction.num_slices:
                break
            out[out_i] = prediction.slices[prediction_i]
        return out


    def render(self, renderer: RenderingManager):
        prediction: BallPrediction = self.prediction_func()
        renderer.begin_rendering('prediction')
        if not prediction.num_slices:
            renderer.end_rendering()
            return

        colors =  [
            renderer.create_color(255, 255, 100, 100),
            renderer.create_color(255, 255, 255, 100),
            renderer.create_color(255, 100, 255, 100),
            renderer.create_color(255, 100, 255, 255),
            renderer.create_color(255, 100, 100, 255),
            renderer.create_color(255, 255, 100, 255)
        ]

        sample_times = self.get_sample_times(prediction.slices[0].game_seconds)
        samples = self.get_samples(prediction, sample_times)

        for i, sample in enumerate(samples):
            if not sample:
                continue
            location = sample.physics.location
            color = colors[i%len(colors)]
            renderer.draw_rect_3d(location, 8, 8, True, color, True)

        renderer.end_rendering()

################### Exercise definitions ###################

def make_ball_prediction_match_config() -> MatchConfig:
    match_config = make_empty_match_config()
    match_config.player_configs = [
        # RocketLeague doesn't like being started without any players.
        PlayerConfig.bot_config(BotConfigs.brick_bot, Team.BLUE),
    ]
    return match_config

cars_in_goal = {
    0: CarState(
        physics=Physics(
            location=Vector3(0, -5700, 30),
            rotation=Rotator(0, 0, 0),
            velocity=Vector3(0, 0, 0),
            angular_velocity=Vector3(0, 0, 0)),
        jumped=True,
        double_jumped=True,
        boost_amount=100),
}

@dataclass
class BallPredictionExercise(TrainingExercise):
    match_config: MatchConfig = field(default_factory=make_ball_prediction_match_config)

@dataclass
class PredictBallInAir(BallPredictionExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        def n11():
            """A Shorthand to get a random value between negative 1 and 1. """
            nonlocal rng
            return rng.uniform(-1, 1)
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(200*n11(), 1000*n11(), 1000),
                velocity=Vector3(100*n11(), 500*n11(), 700),
                angular_velocity=Vector3(0, 0, 0))),
            cars=cars_in_goal,
        )

@dataclass
class SlidingIntoRolling(BallPredictionExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        speed = rng.uniform(10, 1800)
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 4000, 100),
                velocity=Vector3(rng.uniform(-1, 1) * speed, -2*speed, 0),
                angular_velocity=Vector3(0,0,0))),
            cars=cars_in_goal
        )


################### Playlist ###################

def make_ball_prediction_exercises(prediction_func: PredictionFunc) -> Playlist:
    # Initialize game_interface in a thread as it needs a whiel to get ready.
    game_interface: Optional[GameInterface] = None
    def init_interface():
        nonlocal game_interface
        interface = GameInterface(get_logger(f'FailOnInconsistentBallPrediction'))
        interface.load_interface()
        game_interface = interface
    Thread(target=init_interface, daemon=True).start()

    def wrapped_prediction_func():
        nonlocal game_interface
        nonlocal prediction_func
        if game_interface is None:
            return BallPrediction()
        return prediction_func(game_interface)
    ball_prediction_grader = FailOnInconsistentBallPrediction(wrapped_prediction_func)

    ball_prediction_exercise_classes = [
        PredictBallInAir,
        SlidingIntoRolling,
    ]
    return [
        cls(name=cls.__name__, grader=ball_prediction_grader)
        for cls in ball_prediction_exercise_classes
    ]

def default_prediction_func() -> PredictionFunc:
    prediction_struct = BallPrediction()
    def prediction_func(game_interface: GameInterface) -> BallPrediction:
        nonlocal prediction_struct
        game_interface.update_ball_prediction(prediction_struct)
        return prediction_struct
    return prediction_func


def make_default_playlist() -> Playlist:
    """
    This special function gets called by run_module()
    """
    return make_ball_prediction_exercises(
        default_prediction_func()
    )
