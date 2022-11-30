import tkinter as tk
import random
import pyttsx3

# main window & logo image
Math_fun = tk.Tk()
Math_fun.title("Fun.math")
Math_fun.resizable(False, False)
Math_fun.config(bg="Lavender")
Math_fun.geometry('650x650')
im = tk.PhotoImage(file="logo.png")
# the function that say the last 10 minitues
engine = pyttsx3.init()

def readTime(time):
    if not time:
        engine.say(f" Oops, time up")
        engine.runAndWait()
    else:
        engine.say(f" {time} ")
        engine.runAndWait()

# function call when submit button is pressed
def submit():
    global choosingRange, levelTime, time_left
    temp = rangeChooser(userLevel)
    choosingRange = temp[0]
    levelTime = temp[1]
    time_left = levelTime
    questionTextBox.pack()
    answer_entry.pack()

    next_btn.grid(column=3, row=0, sticky="w")
    questionFrame.pack()
    question_track_label.pack()
    easy_btn.grid_forget()
    medium_btn.grid_forget()
    hard_btn.grid_forget()
    guidFrame.pack_forget()
    timer_label.grid(row=0, column=0, sticky="e")
    level_label.config(text=f"Level: {userLevel}")
    highScore_label.config(text=f"HighScore :{highScore_dict[userLevel]}")
    level_label.grid(row=0, column=1)
    highScore_label.grid(row=1, column=1, sticky="w")

    startGame()

# Game starter function
def startGame():
    global time_left, levelTime
    if time_left == levelTime:
        timer_label.config(fg="gray1")
        countdown()
    displayQuestion()

# Function that display the game on the screen
def displayQuestion():
    global questioNo, question, question_answer, index
    questioNo = choosingRange[index]
    answer_entry.focus_set()
    question = dict_data[str(questioNo)][0]
    question_answer = dict_data[str(questioNo)][1]

    questionTextBox.insert(tk.END, question)

# check the result, update the score and generate the new question
# it is called when the next button is pressed
def check_result():
    global index, correct_answer, score
    questionTextBox.delete("1.0", "end")
    if answer_entry.get().strip() == question_answer:
        correct_answer += 1
        score += 20
    index += 1
    answer_entry.delete(0, tk.END)
    result = f"{correct_answer} correct answers out of {index} questions"
    question_track_label.config(text=result)
    if time_left > 0 and index < 5:
        displayQuestion()


def partyFinish():
    global score
    resultFrame.pack()
    message = f"Congrats, your score is {score}"
    resultLabel.config(text=message)
    resultLabel.pack()

    questionTextBox.pack_forget()
    next_btn.grid_forget()
    questionFrame.pack_forget()
    restart_btn.grid(column=2, row=1, sticky="w", padx=5)
    answer_entry.pack_forget()
    close_btn.grid(column=0, row=1, sticky="e", padx=5)
    questionFrame.pack()
    if score > int(highScore_dict[userLevel]):
        updateHighScore()

# closing the game
def closeGame():
    Math_fun.destroy()

# Restart the game to the initial format
def restartGame():
    global index, score, correct_answer
    index, score, correct_answer = 0, 0, 0
    question_track_label.pack_forget()
    resultFrame.pack_forget()
    highScore_label.grid_forget()
    timer_label.grid_forget()
    close_btn.grid_forget()
    restart_btn.grid_forget()
    guidelines_label.config(text=instructions)
    level_label.config(text="Level")
    easy_btn.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5)
    medium_btn.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5)
    hard_btn.grid(row=1, column=2, padx=5, pady=5, ipadx=5, ipady=5)
    questionFrame.pack_forget()
    result = f"0 correct answer out of 0 questions"
    question_track_label.config(text=result)
# Update the high score in the csv file

def updateHighScore():
    highScore_dict[userLevel] = str(score)
    string = ""
    for i in highScore_dict:
        string += f"{i},{highScore_dict[i]}\n"
    with open("highScore.csv", "w") as file:
        file.write(string)

# function that control the time
def countdown():
    global time_left

    # if a game is in play
    if time_left >= 0 and index < 5:
        if time_left <= 10:
            readTime(time_left)
        if time_left == 10:
            timer_label.config(fg="red")
        timer_label.config(text="Time left: "
                                + str(time_left))
        time_left -= 1

        timer_label.after(1000, countdown)
    else:
        partyFinish()
# return the range in with the level questions are and the time of that level

def rangeChooser(level):
    if level == "medium":
        return [random.sample(list(range(22, 40)), 5), 90]
    elif level == "hard":
        return [random.sample(list(range(41, 61)), 5), 150]
    else:
        return [random.sample(list(range(0, 22)), 5), 75]

def easyMethod():
    global userLevel
    userLevel = "easy"
    submit()

def mediumMethod():
    global userLevel
    userLevel = "medium"
    submit()

def hardMethod():
    global userLevel
    userLevel = "hard"
    submit()

# for the logoImage
i = tk.Label(Math_fun, image=im, width=250, height=250)
i.pack()
# for the information such as time,level,high score, so on

guidFrame = tk.Frame(Math_fun, padx=5, pady=5, width=650, height=50, bg="lavender")
guidFrame.pack()
infoFrame = tk.Frame(Math_fun, padx=5, pady=5, width=650, height=50, bg="lavender")
infoFrame.pack()

instructions = '''Tickle your brain with this fun.math by answering math questions
     with a timer running. Lets see how many questions you can answer.
Each question is worth 20 points.\nChoose your level to start the game .'''
guidelines_label = tk.Label(guidFrame, text=instructions, font=('Times New Roman', 15, 'bold'), bg="lavender")
guidelines_label.grid(padx=5, pady=5, ipadx=5, ipady=5)
# level entry and level
level_label = tk.Label(infoFrame, text='Level', font=('Times New Roman', 15, 'bold'), bg="lavender")

level_label.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)
easy_btn = tk.Button(infoFrame, text="Easy", font=('Times New Roman', 10, 'bold'), bg="chartreuse2", command=easyMethod)
medium_btn = tk.Button(infoFrame, text="Medium", font=('Times New Roman', 10, 'bold'), bg="MediumOrchid3",
                       command=mediumMethod)
hard_btn = tk.Button(infoFrame, text="Hard", font=('Times New Roman', 10, 'bold'), bg="firebrick3", command=hardMethod)
easy_btn.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5)
medium_btn.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5)
hard_btn.grid(row=1, column=2, padx=5, pady=5, ipadx=5, ipady=5)

# timer label
timer_label = tk.Label(infoFrame, text="Time", font=('Times New Roman', 15, 'bold'), bg="lavender")
# High score label
highScore_label = tk.Label(infoFrame, text="", font=('Times New Roman', 15, 'bold'), bg="lavender")
# answer_entry
answer_entry = tk.Entry(Math_fun, font=('calibri', 10, 'normal'))
# question text box
questionTextBox = tk.Text(Math_fun, width=100, height=5, font=('Times New Roman', 15, 'bold'), bg="lavender", bd=0,
                          padx=5, pady=20)
# question track how many correct
question_track_label = tk.Label(Math_fun, text="", font=('Times New Roman', 15, 'bold'), bg="lavender")
# result frame which contains result label
resultFrame = tk.Frame(Math_fun)
resultLabel = tk.Label(resultFrame, text="", bg="lavender", font=('Times New Roman', 15, 'bold'))
# question frame that's contains next,restart,close buttons
questionFrame = tk.Frame(Math_fun, bg="lavender", padx=5, pady=5, width=650, height=50)
next_btn = tk.Button(questionFrame, text="Next", font=('Times New Roman', 15, 'bold'), command=check_result, fg="white",
                     bg="DarkOliveGreen1")
restart_btn = tk.Button(questionFrame, text="Restart", font=('Times New Roman', 15, 'bold'), command=restartGame,
                        fg="white", bg="SlateGray3")
close_btn = tk.Button(questionFrame, text="Close", font=('Times New Roman', 15, 'bold'), command=closeGame, fg="white",
                      bg="red2")
# # GLOBAL VARIABLE INITIALISATION
# question,its number and answer variable initialisation
questioNo, question, question_answer = 0, "", ""
# level value taken from the level entry
userLevel = ""
choosingRange, time_left = 0, 0
index, correct_answer, levelTime, score = 0, 0, 0, 0
dict_data = {}
highScore_dict = {}
with open("questionsFile.csv", "r") as file:
    for line in file.readlines():
        datas = line.split(",")
        dict_data[datas[0]] = [datas[1], datas[2][0:len(datas[2]) - 1]]

with open("highScore.csv", "r") as file:
    for line in file.readlines():
        data = line.split(",")
        highScore_dict[data[0]] = data[1][0:len(data[1]) - 1]

myCopyRight = u"\u00A9"
copyrightFrame = tk.Frame(Math_fun, )
copyrightLabel = tk.Label(copyrightFrame, text=f"{myCopyRight} by Aishwarya-Mohamed", font=("Arial", 10, "normal"),
                          bg="bisque")
copyrightFrame.pack(side="bottom", fill="x")
copyrightLabel.pack()
Math_fun.mainloop()

