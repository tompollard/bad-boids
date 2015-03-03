import boids as bd
from nose.tools import assert_almost_equal, assert_raises, assert_equal, assert_not_equal
import os
import yaml
import copy
import numpy as np

# nose_paramaterized lets us use the @parameterized decorator
# to pass a list of functions through each test
from nose_parameterized import parameterized

@parameterized([[bd.update_boids],[bd.update_boids_faster]])
def test_bad_boids_regression(update_function):
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
    boid_data=regression_data["before"]
    boid_data=update_function(boid_data)
    for after,before in zip(regression_data["after"],boid_data):
        for after_value,before_value in zip(after,before): 
            assert_almost_equal(after_value,before_value,delta=0.01)

def test_initialise_creates_correct_no_of_boids():
    number_of_boids = 17
    boids = bd.initialise_boids(number_of_boids)
    for item in boids: # unpack xs,ys,xvs,xys
        assert_equal(len(item), number_of_boids)

@parameterized([[bd.update_boids],[bd.update_boids_faster]])
def test_update_boids_input(update_function):
    input_data = [1,2,3,4,5]
    with assert_raises(ValueError):
        update_function(input_data)

@parameterized([[bd.update_boids],[bd.update_boids_faster]])
def test_only_one_boid_shows_no_flocking_behaviour(update_function):
    x_pos,y_pos,x_vel,y_vel = [1.0],[1.0],[2.0],[7.0]
    boid = (x_pos, y_pos, x_vel, y_vel)
    initial_boid = copy.deepcopy(boid)
    boid = update_function(boid)
    # new positions equal initial position + velocity
    assert_equal(boid[0][0],initial_boid[0][0]+initial_boid[2][0])
    assert_equal(boid[1][0],initial_boid[1][0]+initial_boid[3][0])

@parameterized([[bd.update_boids],[bd.update_boids_faster]])
def test_two_identical_boids_move_to_new_positions(update_function):
    x_pos = [1.0,1.0]
    y_pos = [1.0,1.0]
    x_vel = [2.0,2.0]
    y_vel = [7.0,2.0]
    boids = (x_pos, y_pos, x_vel, y_vel)
    initial_boids = copy.deepcopy(boids)
    boids = update_function(boids)
    boids = np.array(boids)
    assert_not_equal(boids[0:2].tolist(),initial_boids[0:2])

