import functools
from blessed import Terminal
import sys
import characters
import textwrap
import threading
import argparse

echo = functools.partial(print, end='', flush=True)

class Cell:

    def __init__(self):
        self.value = 0
        self.disabled = False
        self.subscribersX = Publisher()
        self.subscribersY = Publisher()

    def update(self, value, msg=""):
        if self.disabled:
            raise ValueError('Cell cannot be updated, currently disabled')

        # enabling
        if self.value == 'a' and value != 'a':
            if msg != "vertical":
                self.subscribersX.notify("enable")
        elif self.value == 'b' and value != 'b':
            if msg != "horizontal":
                self.subscribersY.notify("enable")

        # disabling
        if value == 'a':
            self.subscribersX.notify("disable", "vertical")
        elif value == 'b':
            self.subscribersY.notify("disable", "horizontal")
        self.value = value

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({self.value!r}, disabled={self.disabled!r})'

    def disable(self, msg):
        if self.value:
            # raise ValueError
            self.update(0, msg)
        self.disabled = True

    def enable(self):
        self.disabled = False

    def notify(self, event, msg=""):
        match event:
            case "disable":
                self.disable(msg)
            case "enable":
                self.enable()
            


class Publisher:

    def __init__(self):
        self.subscribers = []

    def addSubscriber(self, sub):
        try:
            if len(sub):
                self.subscribers.extend(sub)
        except TypeError:
            self.subscribers.append(sub)

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({self.subscribers!r})'

    def notify(self, event, msg=""):
        for sub in self.subscribers:
            sub.notify(event, msg)


class Tableau:

    def __init__(self, size, term):
        self.size = size
        self.term = term
        self.cells = [[Cell() for _ in range(size - i)] for i in range(size)]
        self.active_cell = (0,0)
        self.notification_area = (term.height-2, self.size)
        for i in range(size):
            row = []
            for j in range(0, size-i):
                self.cells[i][j].subscribersX.addSubscriber(row)
                row.append(self.cells[i][j])

        for j in range(size):
            col = []
            for i in range(0, size-j):
                self.cells[i][j].subscribersY.addSubscriber(col)
                col.append(self.cells[i][j])

        self.grid_rows = []

    def get(self,i ,j):
        return self.cells[i][j]

    def print(self):
        for row in self.cells:
            print(f'{row!r}')

    def render_grid(self, scale = 1):
        self.grid_rows = []
        n = self.size
        
        for i in range(n):
            rows = [self.term.dim ,self.term.dim] * scale
            for j in range(n - i):
                # top left corner
                if i == 0 and j == 0:
                    rows[0] += characters.ulcorner
                elif i == 0:
                    rows[0] += characters.ttee
                elif j == 0:
                    rows[0] += characters.ltee
                else:
                    rows[0] += characters.bigplus

                rows[1] += characters.vline
                rows[0] += characters.hline*(3 * scale)

                rows[1] += ' '
                if self.cells[j][i].disabled:
                    value, markup = self.compile_cell((j,i))
                    value += markup
                    rows[1] += self.term.normal +  value + self.term.dim
                elif self.cells[j][i].value: 
                    value, markup = self.compile_cell((j,i))
                    value += markup
                    rows[1] += self.term.normal +  value + self.term.dim
                else:
                    rows[1] +=  '  '

                

                if j == self.size - i - 1:
                    if i == 0:
                        rows[0] += characters.urcorner
                    else:
                        rows[0] += characters.bigplus + characters.hline * 3 + characters.lrcorner
                    rows[1] += characters.vline + self.term.normal
                    rows[0] += self.term.normal
                    
            self.grid_rows.extend(rows)


        bottom_row = self.term.dim + characters.llcorner
        for col in range(1, 4):
            bottom_row += characters.btee if col % 4 == 0 else characters.hline
        bottom_row += characters.lrcorner + self.term.normal

        self.grid_rows.append(bottom_row)

        return self.grid_rows

    def draw(self, empty=False):
        grid_rows = self.render_grid()
        for index, row in enumerate(grid_rows):
            echo(self.term.move_xy(self.size, self.size + index) + row)


    def compile_cell(self, position):
        cell = self.cells[position[0]][position[1]]
        value = cell.value if cell.value else " "

        if cell.disabled:
            value = 'x'


        markup = ' '

        return value, markup

    def draw_cell(self, position):
        value, markup = self.compile_cell(position)
        value += markup
        echo(self.term.move(*self.to_term(position)) + value)

    def draw_highlighted_cell(self, position):
        value, markup = self.compile_cell(position)
        value = self.term.underline(value) + markup
        echo(self.term.move(*self.to_term(position)) + value)

    def draw_cursor_cell(self, position):
        value, markup = self.compile_cell(position)
        value = self.term.reverse(value) + markup
        echo(self.term.move(*self.to_term(position)) + value)

    def update_cell(self, position, value):
        i, j = position
        if not self.cells[i][j].disabled:
            self.cells[i][j].update(value)
            
        
            self.draw_cursor_cell(position)
            self.draw()

    def to_term(self, position):
        point_x, point_y = position
        term_x = self.size + (4 * point_x) + 2
        term_y = self.size  + (2 * point_y) + 1
        return (term_y, term_x)

    
    def confirm_quit(self):

        confirmation = self.get_notification_input(
                            "Are you sure you want to quit? (y/n)",
                            char_limit=1, blocking=True, timeout=5)
        return confirmation.lower() == 'y'


    def confirm_clear(self):
        confirmation = self.get_notification_input("Clear Tableau? (y/n)",
                                                   char_limit=1,
                                                   blocking=True,
                                                   timeout=5)
        return confirmation.lower() == 'y'


    def get_notification_input(self, message, timeout=5, char_limit=3,
                               input_condition=str.isalnum, blocking=False):

        # If there's already a notification timer running, stop it.
        try:
            self.notification_timer.cancel()
        except:
            pass

        input_phrase = message + " "
        key_input_place = len(input_phrase)
        echo(self.term.move(*self.notification_area) +
             self.term.reverse(input_phrase) +
             self.term.clear_eol)

        user_input = ''
        keypress = None
        while keypress != '' and len(user_input) < char_limit:
            keypress = self.term.inkey(timeout)
            if input_condition(keypress):
                user_input += keypress
                echo(self.term.move(self.notification_area[0],
                                    self.notification_area[1] +
                                    key_input_place),
                     user_input)
            elif keypress.name in ['KEY_DELETE', 'KEY_BACKSPACE']:
                user_input = user_input[:-1]
                echo(self.term.move(self.notification_area[0],
                                    self.notification_area[1] +
                                    key_input_place),
                     user_input + self.term.clear_eol)
            elif blocking and keypress.name not in ['KEY_ENTER', 'KEY_ESCAPE']:
                continue
            else:
                break

        return user_input

    def send_notification(self, message, timeout=5):
        self.notification_timer = threading.Timer(timeout,
                                                  self.clear_notification_area)
        self.notification_timer.daemon = True
        echo(self.term.move(*self.notification_area) +
             self.term.reverse(message) + self.term.clear_eol)
        self.notification_timer.start()

    def clear_notification_area(self):
        echo(self.term.move(*self.notification_area) + self.term.clear_eol)

    def compile_latex(self):
        # setup
        latex = r"""
\begin{figure}[H]
\setlength{\unitlength}{0.5cm}
\begin{center}
\begin{picture}(""" + str(self.size) + ', ' + str(self.size)+')'
        
        #vertical lines
        latex += '\n\n %vertical lines \n'
        latex += r'\put(0,0){\line(0,1){' + str(self.size) + '}}'
        latex += '\n'
        for i in range(self.size, 0, -1):
            latex += r'\put('+ str(self.size - i + 1) + ', ' + str(self.size - i) + r'){\line(0,1){' + str(i) + '}}'
            latex += '\n'

        latex += '\n\n %horizontal lines \n'
        for i in range(self.size):
            latex += r'\put(0, ' + str(i) + r'){\line(1,0){' + str(i + 1) + '}}'
            latex += '\n'
        latex += r'\put(0, ' + str(self.size) + r'){\line(1,0){' + str(self.size) + '}}' + '\n\n\n'

        cell_values = ""
        for i in range(self.size):
            for j in range(self.size - i):
                if self.cells[i][j].value:
                    cell_values +=  r'\put(' + str(j + 0.25) + ',' + str((self.size - i - 1) + 0.25) + '){'
                    cell_values += r'$\alpha$' if  self.cells[i][j].value == 'a' else r'$\betta$'
                    cell_values +='}' + '\n'
        if cell_values:
            latex += '\n% cell values\n'
            latex+= cell_values

        latex += r'\end{picture}' + '\n'
        latex += r'\caption{A staircase tableau of size $'+ str(self.size)+ '$.}' + '\n'
        latex += r'\end{center}' + '\n'
        latex += r'\end{figure}' + '\n'

        
        return latex


class Cursor:
    def __init__(self, position, grid):
        self.position = position
        self.grid = grid
        self.grid.draw_cursor_cell(position)

    def move_right(self):
        if self.position[0] == self.grid.size - self.position[1] - 1:
            return
        self.grid.draw_cell(self.position)
        self.position = (self.position[0] + 1, self.position[1])
        self.grid.draw_cursor_cell(self.position)

    def move_left(self):
        if self.position[0] == 0:
            return
        self.grid.draw_cell(self.position)
        self.position = (self.position[0] - 1, self.position[1])
        self.grid.draw_cursor_cell(self.position)



    def move_down(self):
        if self.position[1] == self.grid.size - self.position[0] - 1:
            return
        self.grid.draw_cell(self.position)
        self.position = (self.position[0], self.position[1] + 1)
        self.grid.draw_cursor_cell(self.position)

    def move_up(self):
        if self.position[1] == 0:
            return
        self.grid.draw_cell(self.position)
        self.position = (self.position[0], self.position[1] - 1)
        self.grid.draw_cursor_cell(self.position)

    def set_selected_cell(self,key):
        self.grid.update_cell(self.position, key)
        self.grid.draw_cursor_cell(self.position)

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='tableaulab',
        description="""tableaulab is a terminal-based staircase tableau editor interface. Use it to make, edit and export latex for staircaise tableaux.
        Use arrow keys navigate.""",
        usage=textwrap.dedent("""\
            tableaulab [-h]
            options: talbeaulab [--width INT]"""))

    parser.add_argument('--size', action='store', type=int, help="""\
        size of the staircase tableau (default 5)""")

    

    args = parser.parse_args()
    n = args.size

    term = Terminal()
    tableau = Tableau(n, term)

    puzzle_width = max(4 * n, 40)
    puzzle_height = 2 * n

    min_width = (puzzle_width
                 + n
                 + 2) # a little breathing room

    min_height = (puzzle_height
                  + n # includes the top bar + timer
                  + 2 # padding above clues
                  + 3 # clue area
                  + 2 # toolbar
                  + 2) # again, just some breathing room

    necessary_resize = []
    if term.width < min_width:
        necessary_resize.append("wider")
    if term.height < min_height:
        necessary_resize.append("taller")

    if necessary_resize:
        exit_text = textwrap.dedent("""\
        This puzzle is {} columns wide and {} rows tall.
        The terminal window must be {} to properly display 
        it.""".format(
            n, n,
            ' and '.join(necessary_resize)))
        sys.exit(' '.join(exit_text.splitlines()))
        
    echo(term.enter_fullscreen())
    echo(term.clear())
    software_version = '1.0.0'
    tableau_info = f'Staircase Tableau of size {n} :  '
    software_info = 'TableauLab ' + software_version
    tb_width = len(tableau_info)
    sf_width = len(software_info)
    headline = " {:<{tb_w}}{:>{sw_w}} ".format(
        tableau_info, software_info,
        tb_w=tb_width, sw_w=sf_width)

    with term.location(x=0, y=0):
        echo(term.dim + term.reverse(headline) + term.normal)

    tableau.draw()
    cursor = Cursor((0,0), tableau)
    
    toolbar = ''
    commands = [("^Q", "Quit"),
                ("^C", "Copy to clipboard"),
                # ("^G", "go to"),
                ("^X", "Clear")]

    if term.width >= 15 * len(commands):
        for shortcut, action in commands:
            shortcut = term.reverse(shortcut)
            toolbar += "{:<30}".format(' '.join([shortcut, action]))

        with term.location(x=n, y=term.height):
            echo(toolbar)
    else:
        tableau.notification_area = (tableau.notification_area[0] - 1, n)
        command_split = int(len(commands)/2) - 1
        for idx, (shortcut, action) in enumerate(commands):
            shortcut = term.reverse(shortcut)
            toolbar += "{:<30}".format(' '.join([shortcut, action]))

            if idx == command_split:
                toolbar += '\n' + n * ' '

        with term.location(x=n, y=term.height - 2):
            echo(toolbar)



    to_quit = not sys.stdout.isatty()


    info_location = {'x': n, 'y': n + 2 * n + 2}

    with term.raw(), term.hidden_cursor():
        while not to_quit:
            
            keypress = term.inkey()

            if keypress.name == 'KEY_RIGHT':
                cursor.move_right()
            elif keypress.name == 'KEY_LEFT':
                cursor.move_left()
            elif keypress.name == 'KEY_UP':
                cursor.move_up()
            elif keypress.name == 'KEY_DOWN':
                cursor.move_down()
            elif keypress in ('a', 'b'):
                cursor.set_selected_cell(keypress)
            elif keypress.name == 'KEY_BACKSPACE':
                cursor.set_selected_cell(0)
            elif keypress  == 'p':
                break


            # ctrl-q
            if keypress.name == 'KEY_CTRL_Q':
                to_quit = tableau.confirm_quit(True)
                if not to_quit:
                    tableau.send_notification("Quit command canceled.")

            # ctrl-s
            elif keypress == chr(19):
                pass

            # ctrl-c
            elif keypress == chr(3):
                latex = tableau.compile_latex()
                term.clipboard_copy(latex)
                tableau.send_notification("Latex copied to clipboard.")
            # # ctrl-g
            # elif keypress == chr(7):
            #     cursor.go_to_numbered_square()

            # ctrl-x
            elif keypress == chr(24):
                confirm = tableau.confirm_clear()
                if confirm:
                    tableau.send_notification("Puzzle cleared.")
                    for i in range(n):
                        for j in range(n - i):
                            cell = tableau.cells[i][j]
                            if cell.value:
                                cell.update(0)
                                tableau.draw_cell((i, j))
                            if cell.disabled:
                                cell.enable()
                                cell.update(0)
                                tableau.draw_cell((i, j))

                else:
                    tableau.send_notification("Clear command canceled.")


         

    echo(term.exit_fullscreen())
