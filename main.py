import sys


def main():

    if len(sys.argv) < 2:
        sys.argv = ['main.py'] + [f'D{i}' for i in range(1, 26)]

    for arg in sys.argv[1:]:
        try:
            code = __import__(f'{arg}.code', fromlist=[arg]).Code()
            print(f"================= {arg} ===================")
            code.run()
            print("=========================================")
        except ModuleNotFoundError:
            print(f'Unknown argument: {arg}')

    print('Bye!')


if __name__ == '__main__':
    main()
