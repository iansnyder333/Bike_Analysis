# Bike_Analysis
## Author: Ian Snyder
## Instructor: Alexandros Labrinidis
## Teaching Assistant: Evangelos Karageorgos

### Goal
The goal of this project is to expose you with a real data science problem, looking at the end-to-end pipeline. 

* [Task 1] access historical bike rental data for 2021 from HealthyRidePGH and summarize the rental data  
* [Task 2] create graphs to show the popularity of the different rental stations, given filter conditions  
* [Task 3] create graphs to show the rebalancing issue  
* [Task 4] cluster the data to group similar stations together, using a variety of clustering functions and visualize the results of the clustering.

---
### Task 2 
Sample Calculations and Graphs use the following parameters:
filter_month = "09/2021"
filter_stationID = 49881

![image](https://user-images.githubusercontent.com/58576523/236684688-28b4406b-f488-40d8-980a-5bfc2efae7f1.png)

![image](https://user-images.githubusercontent.com/58576523/236684700-79949092-3acd-44ee-ace4-74ca08b9c7e6.png)

![image](https://user-images.githubusercontent.com/58576523/236684709-8525ebc5-4460-4c79-88f3-db9a10653bed.png)

![image](https://user-images.githubusercontent.com/58576523/236684724-9e1c2b9e-7527-48c2-861c-16d3fe7e5781.png)

---
### Task 3


![image](https://user-images.githubusercontent.com/58576523/236684750-cb3fcd89-f0d2-4a37-be08-fdc4912d5439.png)

![image](https://user-images.githubusercontent.com/58576523/236684758-e97719b3-8f44-47be-a276-02ec2635e2a0.png)

---
### Task 4


![image](https://user-images.githubusercontent.com/58576523/236684790-1a635003-9427-4b6a-a5e3-f9e3e0982660.png)

![image](https://user-images.githubusercontent.com/58576523/236684797-11fe7403-3ade-4986-b0f5-5e82dfef6a77.png)

![image](https://user-images.githubusercontent.com/58576523/236684945-870527d9-b144-4413-b755-29c51472ce17.png)

![image](https://user-images.githubusercontent.com/58576523/236684959-399cedcc-2d68-40a3-b1a5-964024f56d7b.png)



### Conclusion 
Based on my analysis, I determined that the optimal algorithim for cluster analysis on the Q3 bike data to be Kmeans clustering with 7 clusters. I came to this conclusion by using the Elbow Method to evaluate K values up to 30+ clusters. The Elbow Method involves calculating the sum of squared errors within clusters for each value of k, The goal is to minimize the sum of squared errors while still considering the cost of adding clusters. This optimization involves creating a plot of the sum of squared errors within clusters for a consistent range of k-values, and finding the point where the change in error diminishes as k increases, which looks like an elbow on the graph. Below is the results from the elbow method which lead me to beleive an optimal value for k was somewhere between 7 and 10, but upon graphical inspection in 4.2 plot1 and plot2, I decided plot1 with 7 clusters was more balanced and consistent, leading to my conclusion that 7 is probably the better choice. I had very little success when using the DBSCAN algorithim, I used 12 as the minimum points as it is two times the number of dimensions in the data, when chooisng my epsilon value, I used the elbow method again but this time calculating the distance each datapoint was from its 12th nearest neighbor, and sorted the plot, to generate the elbow plot. The code I used to generate the DBSCAN elbow plot was taken and adapted from https://medium.com/@tarammullin/dbscan-parameter-estimation-ff8330e3a3bd. I found an ideal epsilon value would be somewhere between 50-110 , but upon actually testing these values I had no success creating a diverse cluster plot. DBSCAN typically works well for irregular and noisy data where determining, as it does not require an optimal k value like in Kmeans. Since our data was fairly consistent with only a few massive outliers, a Kmeans cluster was adequate and fairly easy to optimize.

### Supporting Information 
![image](https://user-images.githubusercontent.com/58576523/236684858-3dd894b1-de68-4bd3-8f15-33483d882ca9.png)
![image](https://user-images.githubusercontent.com/58576523/236684867-a92a7805-3220-4a17-ba08-965640a20fa9.png)

