"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import random
import numpy as np

# Deliberately terrible code for teaching purposes


def initialise_boids(number_of_boids):
    boid_rng = range(number_of_boids)
    boids_x = [random.uniform(-450, 50.0) for boid in boid_rng]
    boids_y = [random.uniform(300.0, 600.0) for boid in boid_rng]
    boid_x_velocities = [random.uniform(0, 10.0) for boid in boid_rng]
    boid_y_velocities = [random.uniform(-20.0, 20.0) for boid in boid_rng]
    boids = (boids_x, boids_y, boid_x_velocities, boid_y_velocities)
    return boids


def update_boids_faster(boids):
    ''' This is where our faster boids will live '''
    boids = np.array(boids)
    xs, ys, xvs, yvs = boids
    boid_num = len(xs)
    
    # Fly towards the middle
    newxs = (xs - np.sum(xs)/float(boid_num)) * 0.01
    xvs = xvs - newxs
    newys = (ys - np.sum(ys)/float(boid_num)) * 0.01
    yvs = yvs - newys

    # Fly away from nearby boids
    xs_array = xs-xs[np.newaxis].T # broadcasting
    ys_array = ys-ys[np.newaxis].T # broadcasting
    nearby_boid_idx = (xs_array)**2 + (ys_array)**2 < 100
    xs_array[~nearby_boid_idx] = 0 # remove values outside range
    ys_array[~nearby_boid_idx] = 0 # remove values outside range
    xvs = xvs + xs_array.sum(axis=0)
    yvs = yvs + ys_array.sum(axis=0) 

    # Try to match speed with nearby boids
    # for i in range(len(xs)):
    #     for j in range(len(xs)):
    #         # Try to match speed with nearby boids
    #         if (xs[j] - xs[i])**2 + (ys[j] - ys[i])**2 < 10000:
    #             xvs[i] = xvs[i] + (xvs[j] - xvs[i]) * 0.125 / len(xs)
    #             yvs[i] = yvs[i] + (yvs[j] - yvs[i]) * 0.125 / len(xs)
    
    # arraywise. broadcast and use index
    # passes with 0.06 delta on regression test
    xs_array = xs-xs[np.newaxis].T
    ys_array = ys-ys[np.newaxis].T
    nearby_boid_idx = (xs_array)**2 + (ys_array)**2 < 10000
    xvs_array = xvs - xvs[np.newaxis].T # speed of nearby
    yvs_array = yvs - yvs[np.newaxis].T # speed of nearby
    xvs_array[~nearby_boid_idx] = 0 # remove values outside range
    yvs_array[~nearby_boid_idx] = 0 # remove values outside range
    xvs = xvs - xvs_array.sum(axis=0) * 0.125/boid_num
    yvs = yvs - yvs_array.sum(axis=0) * 0.125/boid_num 

    # Move according to velocities
    xs = xs + xvs
    ys = ys + yvs

    boids = np.array([xs, ys, xvs, yvs])
    return boids


def update_boids(boids):
    xs, ys, xvs, yvs = boids
    # Fly towards the middle
    for i in range(len(xs)):
        for j in range(len(xs)):
            xvs[i] = xvs[i] + (xs[j] - xs[i]) * 0.01 / len(xs)
    for i in range(len(xs)):
        for j in range(len(xs)):
            yvs[i] = yvs[i] + (ys[j] - ys[i]) * 0.01 / len(xs)
    # Fly away from nearby boids
    for i in range(len(xs)):
        for j in range(len(xs)):
            if (xs[j] - xs[i])**2 + (ys[j] - ys[i])**2 < 100:
                xvs[i] = xvs[i] + (xs[i] - xs[j])
                yvs[i] = yvs[i] + (ys[i] - ys[j])
    # Try to match speed with nearby boids
    for i in range(len(xs)):
        for j in range(len(xs)):
            if (xs[j] - xs[i])**2 + (ys[j] - ys[i])**2 < 10000:
                xvs[i] = xvs[i] + (xvs[j] - xvs[i]) * 0.125 / len(xs)
                yvs[i] = yvs[i] + (yvs[j] - yvs[i]) * 0.125 / len(xs)
    # Move according to velocities
    for i in range(len(xs)):
        xs[i] = xs[i] + xvs[i]
        ys[i] = ys[i] + yvs[i]

    return boids

# initialise boids
boids = initialise_boids(100)

figure = plt.figure()
axes = plt.axes(xlim=(-500, 1500), ylim=(-500, 1500))
scatter = axes.scatter(boids[0], boids[1])


def animate(frame):
    update_boids(boids)
    scatter.set_offsets(zip(boids[0], boids[1]))


anim = animation.FuncAnimation(figure, animate,
                               frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
