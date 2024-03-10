# PPHA 30537
# Spring 2023
# Homework 6

# Madhukar Battula

# Madhukar Battula
# madhukarbattula

# Due date: Monday May 8th before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.

##################

#NOTE: All of the plots the questions ask for should be saved and committed to
# your repo under the name "q1_plot.png", "q2_plot.png", etc. If a question calls
# for more than one plot, name them "q1a_plot", "q1b_plot", etc.
#%%
# Question 1: With the x and y values below, create a plot using only Matplotlib.
# You should plot y1 as a scatter plot and y2 as a line, using different colors
# and a legend.  You can name the data simply "y1" and "y2".  Make sure the
# axis labels are legible.  Add a title that reads "HW6 Q1".

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

x = pd.date_range(start='1990/1/1', end='1991/12/1', freq='MS')
y1 = np.random.normal(10, 2, len(x))
y2 = [np.sin(v)+10 for v in range(len(x))]

fig, ax = plt.subplots()
ax.scatter(x, y1, color='green', label='y1')
ax.plot(x, y2, color='purple', linestyle='solid', label='y2')
ax.set_xlabel('Date')
ax.set_ylabel('Values of Y')
ax.set_title('HW6 Q1')
plt.xticks(rotation=45)
ax.legend(loc='best')

fig.savefig('q1_plot.png', dpi=300, bbox_inches='tight')

#%%
# Question 2: Using only Matplotlib, reproduce the figure in this repo named
# question_2_figure.png.

x = np.linspace(10, 19, 5)
y1 = x
y2 = -1*x + 29

fig, ax = plt.subplots()
ax.plot(x, y1, color='blue', label='Blue')
ax.plot(x, y2, color='red', label='Red')
ax.set_title('X marks the spot')
ax.legend(loc='center left')

fig.savefig('q2_plot.png', dpi=300, bbox_inches='tight')
plt.show()

#%%
# Question 3: Load the mpg.csv file that is in this repo, and create a
# plot that tests the following hypothesis: a car with an engine that has
# a higher displacement (i.e. is bigger) will get worse gas mileage than
# one that has a smaller displacement.  Test the same hypothesis for mpg
# against horsepower and weight.

mpg_data = pd.read_csv('mpg.csv')

# Hypothesis 1: Displacement vs. MPG
fig, ax = plt.subplots()
ax.scatter(mpg_data['displacement'], mpg_data['mpg'], color='green', alpha=0.5)
ax.set_xlabel('Displacement')
ax.set_ylabel('MPG')
ax.set_title('Hypothesis 1: Displacement vs. MPG')

fig.savefig('q3a_plot.png', dpi=300, bbox_inches='tight')
plt.show()
# As per the Hypothesis 1 testing, there is a negative corelation between 
# displacement and mpg data, i.e., as displacement increases, mpg decreases.

# Hypothesis 2: Horsepower vs. MPG
fig, ax = plt.subplots()
ax.scatter(mpg_data['horsepower'], mpg_data['mpg'],color='blue', alpha=0.5)
ax.set_xlabel('Horsepower')
ax.set_ylabel('MPG')
ax.set_title('Hypothesis 2: Horsepower vs. MPG')

fig.savefig('q3b_plot.png', dpi=300, bbox_inches='tight')
plt.show()
# As per the Hypothesis 2 testing, there is a negative corelation between 
# horsepower and mpg data, i.e., as horsepower increases, mpg decreases.

# Hypothesis 3: Weight vs. MPG
fig, ax = plt.subplots()
ax.scatter(mpg_data['weight'], mpg_data['mpg'],color='orange', alpha=0.5)
ax.set_xlabel('Weight')
ax.set_ylabel('MPG')
ax.set_title('Hypothesis 3: Weight vs. MPG')

fig.savefig('q3c_plot.png', dpi=300, bbox_inches='tight')
plt.show()
# As per the Hypothesis 3 testing, there is a negative corelation between 
# weight and mpg data, i.e., as weight increases, mpg decreases.

#%%
# Question 4: Continuing with the data from question 3, create a scatter plot 
# with mpg on the y-axis and cylinders on the x-axis.  Explain what is wrong 
# with this plot with a 1-2 line comment.  Now create a box plot using Seaborn
# that uses cylinders as the groupings on the x-axis, and mpg as the values
# up the y-axis.

fig, ax = plt.subplots()
ax.scatter(mpg_data['cylinders'], mpg_data['mpg'], color='magenta', alpha=0.5)
ax.set_xlabel('Count of Cylinders')
ax.set_ylabel('MPG')
ax.set_title('Scatter Plot of MPG vs. Cylinders')

fig.savefig('q4a_plot.png', dpi=300, bbox_inches='tight')
plt.show()
# The data points are overlapping, and this makes it difficult to visualize 
# the density of the data by using a scatter plot.


sns.boxplot(x='cylinders', y='mpg', data=mpg_data)
plt.xlabel('Count of Cylinders')
plt.ylabel('MPG')
plt.title('Box Plot of MPG vs. Cylinders')
plt.savefig('q4b_plot.png', dpi=300, bbox_inches='tight')
plt.show()
# A box plot clearly shows the distribution of mpg for each cylinder value 
# and makes it easier to visualize any differences in the data.

#%%
# Question 5: Continuing with the data from question 3, create a two-by-two 
# grid of subplots, where each one has mpg on the y-axis and one of 
# displacement, horsepower, weight, and acceleration on the x-axis.  To clean 
# up this plot:
#   - Remove the y-axis tick labels (the values) on the right two subplots - 
#     the scale of the ticks will already be aligned because the mpg values 
#     are the same in all axis.  
#   - Add a title to the figure (not the subplots) that reads "Changes in MPG"
#   - Add a y-label to the figure (not the subplots) that says "mpg"
#   - Add an x-label to each subplot for the x values
# Finally, use the savefig method to save this figure to your repo.  If any
# labels or values overlap other chart elements, go back and adjust spacing.

fig, axs = plt.subplots(2, 2, figsize=(12, 12), sharey=True)

fig.suptitle('Changes in MPG')
fig.text(0.04, 0.5, 'mpg', ha='center', va='center', rotation='vertical')
xlabels = ['Displacement', 'Horsepower', 'Weight', 'Acceleration']
for i, ax in enumerate(axs.flat):
    ax.set_xlabel(xlabels[i])

sns.scatterplot(data=mpg_data, x='displacement', y='mpg', ax=axs[0][0])
sns.scatterplot(data=mpg_data, x='horsepower', y='mpg', ax=axs[0][1])
sns.scatterplot(data=mpg_data, x='weight', y='mpg', ax=axs[1][0])
sns.scatterplot(data=mpg_data, x='acceleration', y='mpg', ax=axs[1][1])

plt.savefig('q5_plot.png', dpi=300, bbox_inches='tight')
plt.show()

#%%
# Question 6: Are cars from the USA, Japan, or Europe the least fuel
# efficient, on average?  Answer this with a plot and a one-line comment.

mpg_data['origin'] = mpg_data['origin']\
    .replace({'usa': 'USA', 'japan': 'Japan', 'europe': 'Europe'})
sns.boxplot(x='origin', y='mpg', data=mpg_data)
plt.title('Fuel efficiency by country of origin')
plt.xlabel('Origin')
plt.ylabel('MPG')

plt.savefig('q6_plot.png', dpi=300, bbox_inches='tight')
plt.show()
# Cars from the USA are least fuel efficient followed by Europe and then Japan.

#%%
# Question 7: Using Seaborn, create a scatter plot of mpg versus displacement,
# while showing dots as different colors depending on the country of origin.
# Explain in a one-line comment what this plot says about the results of 
# question 6.

mpg_data['origin'] = mpg_data['origin']\
    .replace({'usa': 'USA', 'japan': 'Japan', 'europe': 'Europe'})
sns.scatterplot(data=mpg_data, x='displacement', y='mpg', hue='origin')
plt.title('Scatter Plot of MPG vs. Displacement')
plt.xlabel('Displacement')
plt.ylabel('MPG')
plt.legend(title='Country of Origin')

plt.savefig('q7_plot.png', dpi=300, bbox_inches='tight')
plt.show()
# Cars from Japan have highest fuel efficiency, followed by Europe and USA that 
# has least fuel efficiency. This is consistent with the results of Question 6.

#%%