import asyncio
from matplotlib import pyplot as plt

import requester


def create_plot(number, text, bars, numbers):
    bars = [bar.replace(' ', '\n') for bar in bars]

    fig, ax = plt.subplots()
    fig.set_figheight(6)
    fig.set_figwidth(10)
    ax.set(
        title = '{} наиболее востребованных навыков для {}'.format(number, text),
    )

    ax.barh(bars, numbers, color = 'darkblue')

    plt.show()
    fig.savefig('plot.png')


def main():
    user_input = requester.get_args()

    main_text = user_input[0]
    main_number = user_input[1]

    skills_count = asyncio.run(requester.skills_count(main_text, main_number))
    skills_count.reverse()
    names = [name for name, number in skills_count]
    values = [number for name, number in skills_count]

    create_plot(main_number, main_text, names, values)


if __name__ == "__main__":
    main()
