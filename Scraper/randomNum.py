import random
def produceRandomNumWithOutDuplicated():
    numberPool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    number = []
    rand = random.Random()
    for i in range(0, 4):
        # pick 1 num from pool randomly
        randomNumber = rand.randint(0, len(numberPool) - 1)
        number.append(numberPool[randomNumber])
        numberPool.pop(randomNumber)

    print(number[0]*1000 + number[1] * 100 + number[2] * 10 + number[3])
    pass

if __name__ == '__main__':
    produceRandomNumWithOutDuplicated()