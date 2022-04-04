import numpy
import matplotlib
from matplotlib import pyplot
from matplotlib import animation
from astropy.time import Time
from astroquery.jplhorizons import Horizons

simulation_start_date = '2000-01-01'
simulation_duration = 22 * 365

mass_earth = 5.9722e24 / 1.98847e30
mass_moon = 7.3477e22 / 1.98847e30


class Object:
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r = numpy.array(r, dtype=float)
        self.v = numpy.array(v, dtype=float)
        self.xs = []
        self.ys = []
        self.plot = ax.scatter(r[0], r[1], color=color, s=rad**2, edgecolors=None, zorder=10)
        self.line, = ax.plot([], [], color=color, linewidth=1.4)


class SolarSystem:
    def __init__(self, thesun):
        self.thesun = thesun
        self.planets = []
        self.time = None
        self.timestamp = ax.text(.03, .94, "Date:", color="w", transform=ax.transAxes, fontsize="x-large")

    def add_planet(self, planet):
        self.planets.append(planet)

    def evolve(self):
        dt = 1
        self.time += dt
        plots = []
        lines = []
        for p in self.planets:
            p.r += p.v * dt
            acc = -2.959e-4 * p.r / numpy.sum(p.r ** 2) ** (3. / 2)  # in units of AU/day^2
            p.v += acc * dt
            p.xs.append(p.r[0])
            p.ys.append(p.r[1])
            p.plot.set_offsets(p.r[:2])
            p.line.set_xdata(p.xs)
            p.line.set_ydata(p.ys)
            plots.append(p.plot)
            lines.append(p.line)
        self.timestamp.set_text('Date: ' + Time(self.time, format='jd', out_subfmt='float').iso)
        return plots + lines + [self.timestamp]


pyplot.style.use('dark_background')
fig = pyplot.figure(figsize=[11, 20])
ax = pyplot.axes([0., 0., 1., 1.], xlim=(-30, 30), ylim=(-30, 30))
ax.set_aspect('equal')
ax.axis('off')
ss = SolarSystem(Object("Sun", 10, 'red', [0, 0, 0], [0, 0, 0]))
ss.time = Time(simulation_start_date).jd
colors = ['gray', 'orange', 'blue', 'chocolate', "yellow", 'blue', 'blue', 'blue']
sizes = [0.035, 0.087, 0.091, 0.048, 1, 0.833, 0.363, 0.352]
names = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', "Saturn", "Uranus", "Neptune"]
texty = [.47, .73, 1, 1.5, 5.3, 9.5, 19, 29]
for i, nasaid in enumerate([1, 2, 3, 4, 5, 6, 7, 8]):
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time, id_type='id').vectors()
    ss.add_planet(Object(nasaid, 20 * sizes[i], colors[i],
                         [numpy.double(obj[xi]) for xi in ['x', 'y', 'z']],
                         [numpy.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]))
    ax.text(0, - (texty[i] + 0.1), names[i], color=colors[i], zorder=1000, ha='center', fontsize='large')


def animate(i):
    return ss.evolve()


ani = animation.FuncAnimation(fig, animate, repeat=False, frames=simulation_duration, blit=True, interval=20)

matplotlib.pyplot.show()
