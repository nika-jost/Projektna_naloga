
for number in [1, 5, 6, 9, 0, 3, 0]:
    try:
        print(10 / number)

        if number == 3:
            raise ValueError

    except ZeroDivisionError:
        print("Nemoremo dividat z 0")
    except:
        print("Drugačni error")    


for number in [1, 5, 6, 9, 0, 3, 0]:
    if number == 5:
        continue
    else:
        print(number)


for number in [1, 5, 6, 9, 0, 3, 0]:
    if number == 6:
        break
    else:
        print(number)