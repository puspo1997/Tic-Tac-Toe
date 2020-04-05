import random

import tkinter as tk
import tkinter.ttk as ttk


class AppMain:

    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master, width=250, height=150, relief='sunken')
        self.frame.pack_propagate(False)
        self.play = ttk.Button(self.frame, text='Play',
                               command=lambda: PlayMenu(do=0))       
        self.qb = ttk.Button(self.frame, text="Quit", command=root.destroy)

        self.main_window()

    def main_window(self):
        self.remove_widgets()
        self.frame.pack(padx=25, pady=75)
        self.play.pack(side='top', pady=(33, 0))
        self.qb.pack(side='top', pady=(0, 32))

    def remove_widgets(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()


class PlayMenu(AppMain):

    def __init__(self, do):
        self.do = do
        self.label = ttk.Label(root, text='Choose your side',
                               font=('', 20))
        self.frame = ttk.Frame(root, width=250, height=150, relief='sunken')
        self.frame.pack_propagate(False)
        self.player_x = ttk.Button(self.frame, text='X',
                                   command=lambda: GameWindow(pl='X', pc='O'))
        self.player_o = ttk.Button(self.frame, text='O',
                                   command=lambda: GameWindow(pl='O', pc='X'))
        self.back = ttk.Button(self.frame, text='Back',
                               command=lambda: AppMain(master=root))

        if do == 'redeclare':
            global statusLib
            statusLib = [None for v in range(25)]

        self.play_menu()

    def play_menu(self):
        r = AppMain(master=root)
        r.remove_widgets()
        self.label.pack(side='top', pady=(25, 0))
        self.frame.pack(padx=25, pady=25)
        self.player_x.grid(column=0, row=0, padx=(5, 0), pady=(5, 0))
        self.player_o.grid(column=1, row=0, padx=(0, 5), pady=(5, 0))
        self.back.grid(column=0, row=1, sticky='w, e', padx=(5, 5), pady=(0, 5),
                       columnspan=2)


class GameWindow(AppMain):

    def __init__(self, pl, pc):
        self.pl, self.pc, self.stop_game = pl, pc, False
        self.frame = ttk.Frame(root, width=650, height=700)
        self.frame.pack_propagate(False)
        self.canvas = tk.Canvas(self.frame, width=600, height=600)
        self.restart = ttk.Button(self.frame, text='Wanna Play Again',
                                  command=lambda: PlayMenu(do='redeclare'))
        self.game_window()

    def game_window(self):
        r = AppMain(master=root)
        r.remove_widgets()
        self.frame.pack()
        self.canvas.pack(side='top', pady=(25, 0))
        self.restart.pack(side='bottom', pady=20)
        self.draw_board()
        self.canvas.bind('<Button-1>', self.square_selector)
        if self.pl == 'O':
            self.computer_move()

    def draw_board(self):
        self.canvas.create_line(0, 100, 500, 100)
        self.canvas.create_line(0, 200, 500, 200)
        self.canvas.create_line(0, 300, 500, 300)
        self.canvas.create_line(0, 400, 500, 400)
        
        self.canvas.create_line(100, 0, 100,500)
        self.canvas.create_line(200, 0, 200,500)
        self.canvas.create_line(300, 0,300,500)
        self.canvas.create_line(400, 0,400,500)
    def square_selector(self, event):
        self.player_move(square=(event.x // 100 * 5+ event.y // 100))

    def player_move(self, square):
        if statusLib[square] is None:
            self.make_move(sq=square, symbol=self.pl, turn='player')
            if not self.stop_game:
                self.computer_move()

    def computer_move(self):
        status, square = 0, None
        while status is not None:
            square = random.randint(0, 24)
            status = statusLib[square]
        self.make_move(sq=square, symbol=self.pc, turn='computer')

    def make_move(self, sq, symbol, turn):
        self.draw_move(symbol=symbol, sq=sq)
        statusLib[sq] = symbol
        self.end_game(this_move=turn, symbol=symbol)

    def draw_move(self, symbol, sq):
        pos = [50 + sq // 5 * 100, 50 + sq % 5 * 100]
        self.canvas.create_text(pos, text=symbol, font=('', 20),
                                anchor='center')

    def end_game(self, this_move, symbol):
        condition = self.check_end_game(symbol=symbol)
        self.stop_game = condition[0]
        text = ''
        if condition[0]:
            self.canvas.unbind('<Button-1>')
            if this_move == 'player' and not condition[1]:
                text = 'You win'
            elif this_move == 'computer' and not condition[1]:
                text = 'You lose'
            elif condition[1]:
                text = 'It\'s a tie'
            self.finisher(fin=condition[3])
            self.canvas.create_text(200, 300, text=text,
                                    font=('French Script MT', 50),
                                    fill='#EE2C2C')

    @staticmethod                                
    def check_end_game(symbol):
        
        
        if statusLib[0] == statusLib[1] == statusLib[2] == statusLib[3] == statusLib[4]== symbol:
            return [True,False,True,False, 1]
        elif statusLib[5] == statusLib[6] == statusLib[7] == statusLib[8] == statusLib[9]== symbol:
            return [True,False,True, False, 2]
        elif statusLib[10] == statusLib[11] == statusLib[12] == statusLib[13] == statusLib[14]== symbol:
            return [True,False,True, False, 3]
        elif statusLib[15] == statusLib[16] == statusLib[17] == statusLib[18] == statusLib[19]== symbol:
            return [True,False,True, False, 4]
        elif statusLib[20] == statusLib[21] == statusLib[22] == statusLib[23] == statusLib[24]== symbol:
            return [True, False,True,False, 5]
        elif statusLib[0] == statusLib[5] == statusLib[10] == statusLib[15] == statusLib[20]== symbol:
            return [True, False,True,False, 6]
        elif statusLib[1] == statusLib[6] == statusLib[11] == statusLib[16] == statusLib[21]== symbol:
            return [True,False,True, False, 7]
        elif statusLib[2] == statusLib[7] == statusLib[12] == statusLib[17] == statusLib[22]== symbol:
            return [True,False,True, False, 8]
        elif statusLib[3] == statusLib[8] == statusLib[13] == statusLib[18] == statusLib[23]== symbol:
            return [True,False,True, False, 9]
        elif statusLib[4] == statusLib[9] == statusLib[14] == statusLib[19] == statusLib[24]== symbol:
            return [True, False,True, False, 10]
        elif statusLib[0] == statusLib[6] == statusLib[12] == statusLib[18] == statusLib[24]== symbol:
            return [True, False,True,False, 11]
        elif statusLib[4] == statusLib[8] == statusLib[12] == statusLib[16] == statusLib[20]== symbol:
            return [True, False,True,False, 12]
        elif all(k is not None for k in statusLib):
            return [True, True,True,True, 0]
        else:
            return [False, False,False,False, 0]

    
    def finisher(self, fin):
        lib = [[50, 50, 50, 500],  [150, 50, 150, 500],  [250, 50, 250,  500], [350,50,350,500], [450,50,450,500],
               [50, 100, 50, 500], [150, 100, 150, 500], [250, 100, 250, 500],[350,100,350,500],[450,100,450,500],
               [50, 150, 50, 500], [150, 150, 150, 500], [250, 150, 250, 500],[350,150,350,500],[450,150,450,500],
               [50, 200, 50, 500], [150, 200, 150, 500], [250, 200, 250, 500],[350,200,350,500],[450,200,450,500],
               [50, 250, 50, 500], [150, 250, 150, 500], [250, 250, 250, 500],[350,250,350,500]]

        
            
        

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Tic~Tac~Toe')
    root.minsize(width=300, height=300)

    statusLib = [None for i in range(25)]
    mode = tk.IntVar()

    AppMain(master=root)
    root.mainloop()

