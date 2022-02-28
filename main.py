import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class Tiger(object):
    def __init__(self, border_length):
        # random etween -2 and 2
        self.x = 4 * np.random.rand() - 2
        self.y = 4 * np.random.rand() - 2

        self.border_length = border_length
        self.border = self.init_border()

    def move(self):
        move_x = (0.5 * np.random.rand() - 0.25)
        move_y = (0.5 * np.random.rand() - 0.25)
        for i in range(len(self.border)):
            self.border[i][0] = self.border[i][0] + move_x  # Update X
            self.border[i][1] = self.border[i][1] + move_y  # Update Y

    def init_border(self):
        out = [[self.x, self.y]]

        t = np.linspace(-np.pi / 2, np.pi / 2, self.border_length)
        x = 0.1 * np.sin(t)
        y = 0.1 * np.cos(t)

        for i in range(len(t)):
            out.append([self.x + x[i], self.y + y[i]])

        return out

    def get_all_x(self):
        out = []
        for i in range(len(self.border)):
            out.append(self.border[i][0])
        return out

    def get_all_y(self):
        out = []
        for i in range(len(self.border)):
            out.append(self.border[i][1])
        return out


class S(object):
    def __init__(self):
        self.number_of_tigers = 20
        self.border_length = 6

        self.tigers = self.generate_tigers()
        self.chain = []

        self.fig, self.ax = plt.subplots()

        self.animation = None

        self.x_dot_data = []
        self.y_dot_data = []

    def save_actual_tigers(self):
        self.x_dot_data.clear()
        self.y_dot_data.clear()

        for tiger in range(self.number_of_tigers):
            self.x_dot_data.append(self.tigers[tiger].get_all_x())
            self.y_dot_data.append(self.tigers[tiger].get_all_y())

        self.x_dot_data = sum(self.x_dot_data, [])
        self.y_dot_data = sum(self.y_dot_data, [])


    def save_actual_chain(self):
        self.chain.clear()
        self.chain = self.convexHull()

    def running_tigers(self):
        self.animation = FuncAnimation(self.fig, self.animate_tigers, frames=1000, interval=10)

    def animate_tigers(self, step):
        print(step)
        plt.clf()

        self.moves_tigers()
        self.save_actual_tigers()
        self.save_actual_chain()
        self.print_chain()
        self.print_tigers()

    def moves_tigers(self):
        for tiger in range(self.number_of_tigers):
            self.tigers[tiger].move()

    def generate_tigers(self):
        tigers = []
        for tiger in range(self.number_of_tigers):
            tigers.append(Tiger(self.border_length))
        return tigers

    def print_chain(self):
        for i in range(len(self.chain) - 1):
            plt.plot([self.chain[i][0], self.chain[i + 1][0]], [self.chain[i][1], self.chain[i + 1][1]], 'b--')

    def print_tigers(self):
        # self.plot_tigers.set_data(self.x_dot_data, self.y_dot_data)
        plt.plot(self.x_dot_data, self.y_dot_data, 'ro', ms=2)

    def left_index(self):
        minn = 0
        for i in range(1, len(self.x_dot_data)):
            if self.x_dot_data[i] < self.x_dot_data[minn]:
                minn = i
            elif self.x_dot_data[i] == self.x_dot_data[minn]:
                if self.y_dot_data[i] > self.y_dot_data[minn]:
                    minn = i
        return minn

    def orientation(self, p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def convexHull(self):

        number_of_points = self.number_of_tigers * (1 + self.border_length)
        # There must be at least 3 points
        if self.number_of_tigers < 3:
            return

        # Find the leftmost point
        l = self.left_index()

        hull = []

        p = l
        q = 0
        while True:

            # Add current point to result
            hull.append(p)

            q = (p + 1) % self.number_of_tigers

            for i in range(number_of_points):

                # If i is more counterclockwise
                # than current q, then update q
                if self.orientation([self.x_dot_data[p], self.y_dot_data[p]],
                                    [self.x_dot_data[i], self.y_dot_data[i]],
                                    [self.x_dot_data[q], self.y_dot_data[q]]) == 2:
                    q = i

            p = q

            # While we don't come to first point
            if p == l:
                break

        # Print Result
        hull.append(l)

        output = []
        for each in range(len(hull)):
            output.append([self.x_dot_data[hull[each]], self.y_dot_data[hull[each]]])

        return output


s = S()
s.running_tigers()
plt.show()
