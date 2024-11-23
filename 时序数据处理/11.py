for i in range(1,101):
    for x in range(i,101):
        if i*x == 100:
            print(i,x)
            i=x+1
            print("i=",i)
            print("x=",x)
            break

