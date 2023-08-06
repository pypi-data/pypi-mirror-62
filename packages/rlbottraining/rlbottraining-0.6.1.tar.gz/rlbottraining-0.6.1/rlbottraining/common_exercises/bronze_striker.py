from dataclasses import dataclass
from math import pi

from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

from rlbottraining.common_exercises.common_base_exercises import StrikerExercise
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise import Playlist


@dataclass
class BallInFrontOfGoal(StrikerExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 4400, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(900 * rng.n11(), 3000, 0),
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
        )


@dataclass
class FacingAwayFromBallInFrontOfGoal(StrikerExercise):
    car_start_x: float = 0
    car_start_y: float = 2400

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 4400, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(self.car_start_x, self.car_start_y, 0),
                        rotation=Rotator(0, -pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=True,
                    double_jumped=True,
                    boost_amount=20)
            },
        )


# The ball is rolling towards goal but you still need to put it in
class RollingTowardsGoalShot(StrikerExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(1000 * rng.n11(), rng.uniform(0, 1500), 100),
                velocity=Vector3(0, 550, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, -2500, 18),
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    boost_amount=87),
                1: CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
            },
        )


def make_default_playlist() -> Playlist:
    return [
        BallInFrontOfGoal('Facing ball'),
        RollingTowardsGoalShot('Rolling Shot'),
        FacingAwayFromBallInFrontOfGoal('Facing directly away from ball', car_start_x=0),
        FacingAwayFromBallInFrontOfGoal('Facing away from ball 1', car_start_x=1500.),
        FacingAwayFromBallInFrontOfGoal('Facing away from ball 2', car_start_x=-400.),
        FacingAwayFromBallInFrontOfGoal('Facing away from opponents goal', car_start_x=200., car_start_y=5100),
    ]
