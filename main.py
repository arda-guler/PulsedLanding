import tkinter as tk
import time
import matplotlib.pyplot as plt

from vessel import *

def main():
    screen_x = 1280
    screen_y = 720

    screen_x_2 = 640
    screen_y_2 = 360

    window = tk.Tk()
    window.geometry('1280x720')
    window.title("PulsedLanding")

    canvas = tk.Canvas(window, width=screen_x, height=screen_y, bg='black')
    canvas.pack(anchor=tk.CENTER, expand=True)

    def space2screen(x, y):
        return [screen_x_2 + x, screen_y_2 - y]

    grav_accel = -9.81/6

    # pos, vel, dry_mass, prop_mass, mdot, thrust
    lander = Vessel(500, -100, 500, 2000, 100, 50000)

    stimes = []
    throttles = []
    poss = []
    vels = []
    masses = []
    props = []

    dt = 0.05
    cycle = 0
    sim_time = 0
    running = True
    while running:
        canvas.delete("all")

        # PWM
        if lander.pos > 50:
            if lander.vel * -1 > lander.pos * 0.3:
                lander.activate_engine()
            else:
                lander.deactivate_engine()

        else:
            if lander.vel < -15:
                lander.activate_engine()
            else:
                lander.deactivate_engine()

        # physics
        lander.update_physics(grav_accel, dt)

        if lander.pos < 0:
            lander.pos = 0
            lander.vel = 0
            running = False

        # render lander
        lander_screen_pos = space2screen(0, lander.pos)
        canvas.create_rectangle(lander_screen_pos[0] - 5, lander_screen_pos[1], lander_screen_pos[0] + 5, lander_screen_pos[1] - 20, fill="green")

        # render engine plume
        if lander.throttle:
            canvas.create_rectangle(lander_screen_pos[0] - 3, lander_screen_pos[1], lander_screen_pos[0] + 3, lander_screen_pos[1] + 10, fill="orange")

        # render ground
        canvas.create_rectangle(0, screen_y_2, screen_x, screen_y, fill="gray")

        canvas.update()
        window.update()

        cycle += 1
        sim_time = cycle * dt
        stimes.append(sim_time)
        throttles.append(lander.throttle)
        poss.append(lander.pos)
        vels.append(lander.vel)
        masses.append(lander.dry_mass + lander.prop_mass)
        props.append(lander.prop_mass)

        time.sleep(dt)

    plt.plot(stimes, throttles)
    plt.title("Engine Activation Profile")
    plt.xlabel("Time (s)")
    plt.ylabel("Throttle")
    plt.grid()
    plt.show()

    plt.plot(stimes, poss)
    plt.title("Altitude")
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.grid()
    plt.show()

    plt.plot(stimes, vels)
    plt.title("Vertical Velocity")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.grid()
    plt.show()

    plt.plot(stimes, masses)
    plt.title("Total Mass")
    plt.xlabel("Time (s)")
    plt.ylabel("Vessel Mass (kg)")
    plt.grid()
    plt.show()

    plt.plot(stimes, props)
    plt.title("Propellant Mass")
    plt.xlabel("Time (s)")
    plt.ylabel("Prop. Mass (kg)")
    plt.grid()
    plt.show()

main()
