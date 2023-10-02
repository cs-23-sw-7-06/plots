import matplotlib.pyplot as plt

def add_dot(ax, start, end):
    global added
    if not added:
        added = True
        ax.plot(start[0] + ((end[0]-start[0])/2), start[1] + ((end[1]-start[1])/2), color="blue", marker='o', label='node')
    else:
        ax.plot(start[0] + ((end[0]-start[0])/2), start[1] + ((end[1]-start[1])/2), color="blue", marker='o')

def make_box(ax, start, end, dot=True):
    ax.plot([start[0], start[0]], [start[1], end[1]], color="orange")
    ax.plot([start[0], end[0]], [start[1], start[1]], color="orange")
    ax.plot([end[0], end[0]], [start[1], end[1]], color="orange")
    ax.plot([start[0], end[0]], [end[1], end[1]], color="orange")
    ax.fill_between([start[0], end[0]], [end[1], end[1]], [start[1], start[1]], color='#eeeeee')
    if dot: add_dot(ax, start, end)
        
def line_between(ax, start, end, label=None):
    if label:
        ax.plot([start[0], end[0]], [start[1], end[1]], linestyle='dashed', label=label, color='purple')
    else:
        ax.plot([start[0], end[0]], [start[1], end[1]], linestyle='dashed', color='purple')

_, ax = plt.subplots()

ax.set_ylim(0, 100)
ax.set_xlim(0, 100)

added = False
make_box(ax, (55, 75), (65, 85))
make_box(ax, (50, 60), (65, 75))
make_box(ax, (85, 60), (75, 85))
make_box(ax, (55, 45), (65, 60))
make_box(ax, (85, 45), (75, 60))
make_box(ax, (50, 25), (65, 45))
make_box(ax, (85, 25), (75, 45))

ax.plot(70, 55, marker='o', color='red', label='hub')
ax.plot(60, 70, marker='o', color='green', label='user')

ax.legend(loc='upper left')

ax.set_title("Proximity Based Localization")


plt.axis('off')
plt.savefig("/tmp/proximity.pdf")
plt.show()

_, ax = plt.subplots()

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

make_box(ax, (55, 75), (65, 85), dot=False)
make_box(ax, (50, 60), (65, 75), dot=False)
make_box(ax, (85, 60), (75, 85), dot=False)
make_box(ax, (55, 45), (65, 60), dot=False)
make_box(ax, (85, 45), (75, 60), dot=False)
make_box(ax, (50, 25), (65, 45), dot=False)
make_box(ax, (85, 25), (75, 45), dot=False)

line_between(ax, (62, 32), (60, 70), 'strength measurement')
line_between(ax, (82, 55), (60, 70))
line_between(ax, (68, 80), (60, 70))

ax.plot(70, 55, marker='o', color='red', label='hub')
ax.plot(62, 32, marker='o', label='node', color='blue')
ax.plot(82, 55, marker='o', color='blue')
ax.plot(68, 80, marker='o', color='blue')
ax.plot(60, 70, marker='o', color='#00BB00', label='user')

ax.legend(loc='upper left')

ax.set_title("Triangulation Based Localization")

plt.axis('off')
plt.savefig("/tmp/triangulation.pdf")
plt.show()