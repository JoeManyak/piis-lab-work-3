if __name__ == '__main__':
    print("Possible methods:\n 1. negamax\n 2. negascout\n 3. pvs")
    method = int(input("Choose method by entering number: "))
    while True:
        if 0 < method < 4:
            break
        else:
            print("Wrong method, try again")
            method = input("Choose method: ")
