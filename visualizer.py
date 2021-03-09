import asyncio
from matplotlib import pyplot as plt

import requester


def main():
    user_input = requester.get_args()

    main_text = user_input[0]
    main_number = user_input[1]

    skills_count = asyncio.run(requester.skills_count(main_text, main_number))
    names = [name for name, number in skills_count]
    values = [number for name, number in skills_count]

    fig = plt.figure()
    plt.bar(names, values)
    plt.show()
    fig.savefig('plot.png')


if __name__ == "__main__":
    main()
