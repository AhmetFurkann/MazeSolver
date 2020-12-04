import numpy as np
import cv2


class MazeSolver():

    def __init__(self):
        self.row = None
        self.col = None
        self.image = ImageToMaze("C:\\Users\\Ahmet\\PycharmProjects\\maze_solving\\mazes_img\\maze_2.jpg")
        self.maze = self.image.get_maze_image()
        self.working_maze_image = self.image.get_working_maze_image()
        self.row, self.col = self.find_first_location()

    def find_first_location(self):
        for sep in range(0, len(self.working_maze_image)):
            self.row = sep
            if 0 in self.working_maze_image[sep]:
                self.col = self.working_maze_image[sep].tolist().index(0)
                break
        return self.row, self.col

    def check_directions(self, current_node_pos):
        (n, s, e, w) = (False, False, False, False)
        (n_e, n_w, s_e, s_w) = (False, False, False, False)
        row, col = current_node_pos

        if row == 0:
            s = True if self.working_maze_image[row + 1, col] == 0 else False
            e = True if self.working_maze_image[row, col + 1] == 0 else False
            w = True if self.working_maze_image[row, col - 1] == 0 else False
            s_e = True if self.working_maze_image[row + 1, col + 1] == 0 else False
            s_w = True if self.working_maze_image[row + 1, col - 1] == 0 else False
        else:
            n = True if self.working_maze_image[row - 1, col] == 0 else False
            s = True if self.working_maze_image[row + 1, col] == 0 else False
            e = True if self.working_maze_image[row, col + 1] == 0 else False
            w = True if self.working_maze_image[row, col - 1] == 0 else False

            n_e = True if self.working_maze_image[row - 1, col + 1] == 0 else False
            n_w = True if self.working_maze_image[row - 1, col - 1] == 0 else False
            s_e = True if self.working_maze_image[row + 1, col + 1] == 0 else False
            s_w = True if self.working_maze_image[row + 1, col - 1] == 0 else False

        return {"N": n, "S": s, "E": e, "W": w,
                "N_E": n_e, "N_W": n_w, "S_E": s_e, "S_W": s_w}

    def move(self, case, current_pos):
        self.row, self.col = current_pos
        if case["W"] and case["N_W"] and case["S_W"]:
            if case["S"] and case["S_E"]:
                self.col += 1
            else:
                self.row += 1

        elif case["S_E"] and case["E"] and case["N_E"]:
            if case["N"] and case["N_W"]:
                self.col -= 1
            else:
                self.row -= 1

        elif case["S_W"] and case["S"] and case["S_E"]:
            self.col += 1
        elif case["S_W"] and case["S"]:
            self.col += 1
        elif case["N"] and case["N_E"]:
            self.col -= 1
        elif case["S_W"]:
            self.row += 1
        elif case["N_W"]:
            self.col -= 1
        elif case["S_E"]:
            self.col += 1
        elif case["N_E"]:
            self.row -= 1
        return self.row, self.col

    def implement_movement(self):

        case = self.check_directions((self.row, self.col))
        colored = cv2.rectangle(self.maze, (self.col, self.row), (self.col + 2, self.row + 2), (0, 255, 0), 1)
        self.row, self.col = self.move(case, (self.row, self.col))
        return colored


class ImageToMaze:
    def __init__(self, image_path):
        self.__maze = cv2.imread(image_path, 0)
        self.__working_maze_image = self.set_working_maze_image()
        self.__maze = self.__working_maze_image
        self.__maze = self.set_maze_image()

    def set_maze_image(self):
        self.__maze = np.where(self.__maze == 1, 255, self.__maze)
        self.__maze = cv2.cvtColor(self.__maze, cv2.COLOR_GRAY2RGB)
        return self.__maze

    def set_working_maze_image(self):
        ret, working_image = cv2.threshold(self.__maze, 200, 255, cv2.THRESH_BINARY)
        working_image = np.where(working_image == 255, 1, working_image)
        working_image = self.crop(working_image)
        working_image = self.crop_the_bottom_side(working_image)
        return working_image

    def get_maze_image(self):
        return self.__maze

    def get_working_maze_image(self):
        return self.__working_maze_image

    def crop(self, working_image):
        number_of_element = len(working_image)
        for sep in range(number_of_element):
            if int(sum(working_image[sep]) / number_of_element) != 1:
                return working_image[sep:]

    def crop_the_bottom_side(self, working_image):
        reversed_working_image = working_image[::-1]
        cropped = self.crop(reversed_working_image)
        orginal = working_image[::-1]
        return orginal


maze_solver = MazeSolver()
maze_solver.implement_movement()
