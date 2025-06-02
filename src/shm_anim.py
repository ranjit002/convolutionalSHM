import argparse
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy import integrate


def main():
    args = parse()

    duration = args.duration
    frequency = args.frequency
    length = args.length
    # Damping
    gamma = 0.0
    out_file = args.out

    # Initial conditions
    theta_0, theta_dot_0 = -np.pi / 2, 0

    dt = 0.01
    times = np.arange(0, duration, dt)

    print("Solving ODE...")
    solution = integrate.odeint(
        lambda state, t: derivatives(state, t, frequency, gamma, length),
        np.array([theta_0, theta_dot_0]), 
        times
        )

    thetas = solution[:, 0]

    print("Plotting animation...")
    # Set up figure
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.axis("off")

    ax.set_xlim(-1.1 * length, 1.1 * length)
    ax.set_ylim(-1.1 * length, 1.1 * length)
    line, = ax.plot([], [], "o-", lw=2, markersize=10, c="k")

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        theta = thetas[frame]
        x = length * np.sin(theta)
        y = -length * np.cos(theta)
        line.set_data([0, x], [0, y])
        return line,

    ani = FuncAnimation(fig, update, frames=len(times), init_func=init, blit=True, interval=dt * 1000)

    print("Saving animation...")
    ani.save(out_file, fps=int(1/dt), dpi=200)
    print(f"Saved animation to {out_file}")

def derivatives(
    state: List[float], time: float, frequency: float, gamma: float, length: float
) -> np.ndarray:
    """find derivatives

    Args:
        state (List[float]): theta, angular velocityr
        time (float):
        frequency (float):
        gamma (float): damping

    Returns:
        np.ndarray: [theta double dot, theta dot]
    """
    theta_ddot = state[1]
    theta_dot = -frequency * np.sin(state[0])

    theta_dot -= 2 * gamma * length * state[1]

    return np.array([theta_ddot, theta_dot])

def parse():
    parser = argparse.ArgumentParser(description="Animation for SHM pendulum")

    parser.add_argument("-t", "--time", type=int, help="Duration of movie in seconds", dest="duration", required=True)
    parser.add_argument("-f", "--freq", type=float, help="SHM oscillation frequency", dest="frequency", required=True)
    parser.add_argument("-l", "--len", type=float, help="Length of oscillator", dest="length", default=1)
    parser.add_argument("-o", "--out", type=str, help="Output file name", default="pendulum.mp4")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main()
