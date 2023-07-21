# Optimization of crop flow
## Mohammad Ahnaf Sadat

In the data analysis section of the project, we observed that product prices vary across different stores and cities. This variability presents local food farms with an opportunity to sell their products in high-priced areas.

In this section, our focus is on analyzing crop distribution strategies for local food farms. The goal is to devise strategies that maximize the combined profit for all the counties involved in the distribution process.

We have selected tomatoes to illustrate our approach. Our approach involves:

1.	Estimation of the demand and supply for tomatoes across Iowa.

The estimation we got is in “Supply_Demand_Estimation > S_D_Estimated.xlsx”.

And a detailed guide on how we came up with the numeric is briefly discussed in “Supply_Demand_Estimation > Guide_to_Supply_Demand_Estimation.docx”.


2.	Supply and demand visualization across Iowa.

We have used “Tableau” to create the visualizations. A limited guide on how to produce the visualization is in “Tableau_Visualization > Guide_to_supply_demand_visualization.docx”.
 

3.	Developing the optimization model

We have only used a subset (24 counties out of 99 counties) of the data to develop the optimization model. The optimization is capable of handling 99 counties. 

The data used for the optimization model can be found in “Optimization_Model > Subset_data.csv”. And a comprehensive guide for this step is available in “Optimization_Model > Guide_to_optimization_of_crop_flow.docx”. 

4.	Solution visualization

We have used “Flow map” extension of PowerBI to generate the visualization. For this we have used the “Solution_Visualization > power_bi_data.csv” generated from step 3 mentioned in this document. The resulting visualization can be found in “Solution_Visualization > Flow.pbix”

A complete guide on how to use the flow map in PowerBI can be found here:
https://www.sqlshack.com/flow-map-chart-in-power-bi-desktop/
