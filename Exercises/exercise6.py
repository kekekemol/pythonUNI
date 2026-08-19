def test():
    print("Please enter you test mark")
    testraw = float(input("enter test mark here:"))

    testweighted = (testraw/50)*10
    return testweighted
print("Your test weighted mark is:", test())

def quiz():
    print("Please enter you quiz mark")
    quizraw = float(input("enter quiz mark here:"))

    quizweighted = (quizraw/20)*10
    return quizweighted
print("Your quiz weighted mark is:", quiz())

def assgm1():
    print("Please enter you assignment 1 mark")
    assgm1raw = float(input("enter assignment 1 mark here:"))

    assgm1weighted = (assgm1raw/40)*20
    return assgm1weighted
print("Your assignment 1 weighted mark is:", assgm1())

def assgm2():
    print("Please enter you assignment 2 mark")
    assgm2raw = float(input("enter assignment 2 mark here:"))

    assgm2weighted = (assgm2raw/40)*20
    return assgm2weighted
print("Your assignment 2 weighted mark is:", assgm2())

def project():
    print("Please enter you project mark")
    projectraw = float(input("enter project mark here:"))

    projectweighted = (projectraw/100)*40
    return projectweighted
print("Your project weighted mark is:", project())

def totalassessment():
    total = testweighted() + quizweighted() + assgm1weighted() + assgm2weighted() + projectweighted()
    return total