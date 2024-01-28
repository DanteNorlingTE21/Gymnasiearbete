import os

directory = "C:/Users/dante.norling/Desktop/Gymnasiearbete/Logged Games"

Human_Draw_AI = 0
Human_Win_AI = 0
Human_Lose_AI = 0

Human_Draw_Minmax = 0
Human_Win_Minmax = 0
Human_Lose_Minmax = 0

AI_Draw_Human = 0
AI_Win_Human = 0
AI_Lose_Human = 0

AI_Draw_Minmax = 0
AI_Win_Minmax = 0
AI_Lose_Minmax = 0

Minmax_Draw_AI = 0
Minmax_Win_AI = 0
Minmax_Lose_AI = 0

Minmax_Draw_Human = 0
Minmax_Win_Human = 0
Minmax_Lose_Human = 0



for filename in os.listdir(directory):
    f = open(directory + '/'+ filename, "r")
    results = f.readlines()

    if "MinMax" in results[2]:
        if "None" in results[1]:
            if "AI" in results[3]:
                Minmax_Draw_AI += 1
            elif "Human" in results[3]:
                Minmax_Draw_Human += 1
        elif "1" in results[1]:
            if "AI" in results[3]:
                Minmax_Win_AI += 1
            elif "Human" in results[3]:
                Minmax_Win_Human += 1
        elif "2" in results[1]:
            if "AI" in results[3]:
                Minmax_Lose_AI += 1
            elif "Human" in results[3]:
                Minmax_Lose_Human += 1
    
    elif "AI" in results[2]:
        if "None" in results[1]:
            if "MinMax" in results[3]:
                AI_Draw_Minmax += 1
            elif "Human" in results[3]:
                AI_Draw_Human += 1
        elif "1" in results[1]:
            if "MinMax" in results[1]:
                AI_Win_Minmax += 1
            elif "Human" in results[3]:
                AI_Win_Human += 1
        elif "2" in results[1]:
            if "MinMax" in results[3]:
                AI_Lose_Minmax += 1
            elif "Human" in results[3]:
                AI_Lose_Human += 1

    elif "Human" in results[2]:
        if "None" in results[1]:
            if "AI" in results[3]:
                Human_Draw_AI += 1
            elif "MinMax" in results[3]:
                Human_Draw_Minmax += 1
        elif "1" in results[1]:
            if "AI" in results[3]:
                Human_Win_AI += 1
            elif "MinMax" in results[3]:
                Human_Win_Minmax += 1
        elif "2" in results[1]:
            if "AI" in results[3]:
                Human_Lose_AI += 1
            elif "MinMax" in results[3]:
                Human_Lose_Minmax += 1

 
    f.close()

print("Human vs AI, Win,draw,loss", Human_Win_AI, Human_Draw_AI, Human_Lose_AI)
print("Human vs Minmax, Win,draw,loss", Human_Win_Minmax, Human_Draw_Minmax, Human_Lose_Minmax)
print("AI vs Human, Win,draw,loss", AI_Win_Human, AI_Draw_Human, AI_Lose_Human)
print("AI vs Minmax, Win,draw,loss", AI_Win_Minmax, AI_Draw_Minmax, AI_Lose_Minmax)
print("Minmax vs AI, Win,draw,loss", Minmax_Win_AI, Minmax_Draw_AI, Minmax_Lose_AI)
print("Minmax vs Human, Win,draw,loss", Minmax_Win_Human, Minmax_Draw_Human, Minmax_Lose_Human)
