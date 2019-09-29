from matplotlib import pyplot as plt
import requester


skills = requester.get_most_demanded_skills(30, requester.count_key_skills(requester.get_vacancies('python')))
names = [name for number, name in skills]
values = [number for number, name in skills]

fig = plt.figure()
plt.bar(names, values)
plt.show()
fig.savefig('plot.png')