import random , os
from PIL import Image, ImageDraw

def check_1(x , temp_array ,  sudoku_array) :  # Check for the Block in which the cell exist
    flag_1 = True
    if len(temp_array) < 3 :
        j = 2
        l = 0
    elif len(temp_array) < 6 :
        j = 5
        l = 3
    else :
        j = 8
        l = 6
#-------------------------------------------------------
    i = len(sudoku_array)
    if len(sudoku_array) < 3 :
        o = 0
    elif len(sudoku_array) < 6 :
        o = 3
    else :
        o = 6
#-----------------------------------------------------
    for m in range(o,i) :
        for n in range(l,j+1) :
            if x == sudoku_array[m][n] :
                flag_1 = False
                break
        if x == sudoku_array[m][n] :
            break
    return flag_1


########################################################


def check_2(x, counter, sudoku_array) :  # Check for the recurrance of number in its consequent column
    flag_2 = True
    for k in range(len(sudoku_array)) :
        if x == sudoku_array[k][counter] :
            flag_2 = False
            break
    return flag_2


########################################################


def sudoku_generator(sudoku_array , sudoku) :
    for k in range(9) :   # Counter for going through each row
        rows = []
        count = 0
        x = random.randint(4,6)   # Choose whether to leave 4, 5 or 6 fields blank in a row
        exclude = []   # The Indices to be excluded from the row
        while count != x : 
           random_exclusion = random.randint(0,8)
           if random_exclusion not in exclude :
               exclude.append(random_exclusion)
               count+=1
        for j in range(9) :
            if j not in exclude :
                rows.append(sudoku_array[k][j])
            else :
                rows.append(" ")  # Here space means empty space in the row
        sudoku.append(rows)


########################################################


def board_generator(file_name) :
    img = Image.new('RGB' , (378 , 378) , color = (255 , 255 , 255))
    draw = ImageDraw.Draw(img)
    for i in range(1,10) :
        draw.line((0,42*i , 378,42*i), fill=0)
        draw.line((42*i,0 , 42*i,378), fill=0)
    img.save(file_name + ".png")


########################################################


def board_filler(sudoku_array , file_name) :
    img = Image.open(file_name + ".png")
    draw = ImageDraw.Draw(img)
    for x in range(9) :
        for y in range(9) : 
            draw.text((19 + 42*y , 19 + 42*x) , str(sudoku_array[x][y]) , fill = 0 )
    img.save(file_name + ".png")


########################################################


def brute_generator(sudoku_array) : # The main sudoku Generating Algo. , at least the starting point
    all_possibilities = [1,2,3,4,5,6,7,8,9]
    possibilities = all_possibilities.copy()
    blacklist = []
    counter = 0
    temp_array = []
    while counter != 9 :
        if len(blacklist) == len(possibilities) :  # This condition is to reset our work if the row being generated is not suitable
            all_possibilities = [1,2,3,4,5,6,7,8,9]
            possibilities = all_possibilities.copy()
            blacklist = []
            counter = 0
            temp_array = []
            continue
        x = random.choice(possibilities)
        if x not in blacklist :
            if len(sudoku_array) != 0 :
                check_1_bool = check_1(x, temp_array , sudoku_array)
                if check_1_bool == False :
                    blacklist.append(x)
                    continue
                elif check_2(x, counter , sudoku_array) == False :
                    blacklist.append(x)
                    continue
            possibilities.remove(x)
            counter+=1
            temp_array.append(x)
            blacklist = []
    sudoku_array.append(temp_array)


###########################################################


ans = 0
clear = lambda: os.system('cls')
while ans!=2 :
    clear()
    ans = int(input(""" 
1.) Generate Sudoku
2.) Exit \n\n> """))
    if ans == 1 :
        directory_name = input("Name of directory to be in which sudoku will be saved , \nIf you want you can leave it empty then default values will be used :-  ")
        if directory_name :
            if not os.path.isdir(directory_name) :
                os.mkdir(directory_name)
            directory_name += "/"
        sudoku_array = []   # This will be the generated sudoku , and we will treat it as answer
        sudoku = []  # The real sudoku that we will make from the answer
        for i in range(9) :
            brute_generator(sudoku_array)
        board_generator(directory_name + "Answer")
        board_filler(sudoku_array, directory_name + "Answer")
#------------------------------------------------------------------
        board_generator(directory_name + "Sudoku")
        sudoku_generator(sudoku_array , sudoku)
        board_filler(sudoku , directory_name + "Sudoku")
    elif ans == 2 :
        exit
    else :
        print("Try again with the options from 1 and 2")
