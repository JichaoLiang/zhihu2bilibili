# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = 0
    b = '123'
    c = 0.1
    list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    firstelement = list1[0]
    lastelement = list1[-1]
    selected = list1[0:5]
    selected2 = list1[1::2]
    selected3 = list1[::-1]
    yuanzu = (0, 1, 2)
    position = (10,20)

    dict = { 'key1':1, 'key2':2, 0:1 }
    val1 = dict['key1']

    hospitallookup = {
        '口腔科': '张三',
        '麻醉科': '李四',
        '骨科': ['王五', '赵柳']
    }

    tianjinhospitalslookup = {
        '天津医院': None,
        '西青医院': hospitallookup
    }

    print('西青医院口腔科' + tianjinhospitalslookup['西青医院']['口腔科'])
    print('口腔科大夫名称 ' + hospitallookup['口腔科'])
    print(f'口腔科大夫名称 {hospitallookup["口腔科"]}')

    print('value1: ' + str(val1))

    print('dict: ' + str(dict))

    print("selected " + str(selected))
    print("selected2 " + str(selected2))
    print("selected3 " + str(selected3))
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
