import boids as bd
from nose.tools import assert_almost_equal, assert_raises, assert_equal, assert_not_equal
import os
import yaml
import copy

def test_bad_boids_regression():
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
    boid_data=regression_data["before"]
    bd.update_boids(boid_data)
    for after,before in zip(regression_data["after"],boid_data):
        for after_value,before_value in zip(after,before): 
            assert_almost_equal(after_value,before_value,delta=0.01)

def test_initialise_creates_correct_no_of_boids():
    number_of_boids = 17
    boids = bd.initialise_boids(number_of_boids)
    for item in boids: # unpack xs,ys,xvs,xys
        assert_equal(len(item), number_of_boids)

def test_update_boids_input():
    input_data = [1,2,3,4,5]
    with assert_raises(ValueError):
        bd.update_boids(input_data)

def test_only_one_boid_shows_no_flocking_behaviour():
    x_pos,y_pos,x_vel,y_vel = [1.0],[1.0],[2.0],[7.0]
    boid = (x_pos, y_pos, x_vel, y_vel)
    initial_boid = copy.deepcopy(boid)
    bd.update_boids(boid)
    # new positions equal initial position + velocity
    assert_equal(boid[0][0],initial_boid[0][0]+initial_boid[2][0])
    assert_equal(boid[1][0],initial_boid[1][0]+initial_boid[3][0])

def test_two_indentical_boids_move_to_new_positions():
    x_pos = [1.0,1.0]
    y_pos = [1.0,1.0]
    x_vel = [2.0,2.0]
    y_vel = [7.0,2.0]
    boids = (x_pos, y_pos, x_vel, y_vel)
    initial_boids = copy.deepcopy(boids)
    bd.update_boids(boids)
    assert_not_equal(boids[0:2],initial_boids[0:2])

