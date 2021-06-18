#%%
import matplotlib.pyplot as plt

def autopct_generator(limit):
    """Remove percent on small slices."""
    def inner_autopct(pct):
        return ('%.2f%%' % pct) if pct > limit else ''
    return inner_autopct

# Data to plot
labels = 'CN 1', 'CN 2', 'CN 3', 'CN 4', 'CN 5','CN 6','CN 7', 'CN 8', 'CN 9', 'CN 10', 'CN 11','CN 12', 'CN 13+'
sizes = [4128,526,1779,9707,1444,12503,1751,2984,1360,856,140,1476,59]
total = sum(sizes)
#colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
#explode = [0 for _ in range(13)]  # explode 1st slice

# Plot
fig, ax1 = plt.subplots(figsize=(6, 5))
#box = ax1.get_position()
#ax1.set_position([box.x0, box.y0, box.width * 1.3, box.height])
fig.subplots_adjust(0.3,0,1,1)
ax1.pie(sizes, autopct=autopct_generator(7), shadow=True, startangle=140)
plt.legend(
    loc='upper left',
    labels=['%s:  %d' % (
        l, s) for l, s in zip(labels, sizes)],
    prop={'size': 12},
    bbox_to_anchor=(0.0, 1),
    bbox_transform=fig.transFigure
)
ax1.axis('equal')
plt.show()
# %%
xlabel = '1', '2', '3', '4', '5',' 6','7', '8', '9', '10', '11','12', '13+'
plt.bar(labels, sizes)
plt.xticks(rotation=70)
plt.show()
# %%
