%% Machine Learning Online Class
%  Exercise 7 | Principle Component Analysis and K-Means Clustering
%
%  Instructions
%  ------------
%
%  This file contains code that helps you get started on the
%  exercise. You will need to complete the following functions:
%
%     pca.m
%     projectData.m
%     recoverData.m
%     computeCentroids.m
%     findClosestCentroids.m
%     kMeansInitCentroids.m
%
%  For this exercise, you will not need to change any code in this file,
%  or any other files other than those mentioned above.
%

%% Initialization
clear ; close all; clc

%% ================= Part 1: Find Closest Centroids ====================
%  To help you implement K-Means, we have divided the learning algorithm 
%  into two functions -- findClosestCentroids and computeCentroids. In this
%  part, you should complete the code in the findClosestCentroids function. 
%
fprintf('Finding closest centroids.\n\n');
 
% Load an example dataset that we will be using
X = csvread('Angles.csv');
X = X(2:end,:);
% Select an initial set of centroids
K = 6; % 3 Centroids
initial_centroids = [109,109,109,109,109,109;
                     114,112,110,108,106,104;
                     125,117,110,105,100, 91;
                     130,127,122,119, 80, 78;
                     140,125,108, 97, 90, 84;
                     180,180, 95, 95, 84, 84];

% Find the closest centroids for the examples using the
% initial_centroids
idx = findClosestCentroids(X, initial_centroids);

fprintf('Closest centroids for the first 5 examples: \n')
fprintf(' %d \n', idx(1:5));
%fprintf('\n(the closest centroids should be 1, 3, 2 respectively)\n');




%% ===================== Part 2: Compute Means =========================
%  After implementing the closest centroids function, you should now
%  complete the computeCentroids function.
%
fprintf('\nComputing centroids means.\n\n');

%  Compute means based on the closest centroids found in the previous part.
centroids = computeCentroids(X, idx, K, initial_centroids);

fprintf('Centroids computed after initial finding of closest centroids: \n')
fprintf(' %f %f %f %f %f %f \n' , centroids');
%fprintf('\n(the centroids should be\n');
%fprintf('   [ 2.428301 3.157924 ]\n');
%fprintf('   [ 5.813503 2.633656 ]\n');
%fprintf('   [ 7.119387 3.616684 ]\n\n');



pause;

%% =================== Part 3: K-Means Clustering ======================
%  After you have completed the two functions computeCentroids and
%  findClosestCentroids, you have all the necessary pieces to run the
%  kMeans algorithm. In this part, you will run the K-Means algorithm on
%  the example dataset we have provided. 
%
fprintf('\nRunning K-Means clustering on example dataset.\n\n');

% Load an example dataset
X = csvread('CN4_Angles_all_cat_12000.csv');
%X = X(2:end,:);
% Settings for running K-Means
K = 9;
max_iters = 20;

% For consistency, here we set centroids to specific values
% but in practice you want to generate them automatically, such as by
% settings them to be random examples (as can be seen in
% kMeansInitCentroids).
initial_centroids = [109,109,109,109,109,109;
                     111,110,110,108,107,106;
                     114,112,110,108,106,104;
                     125,117,110,105,100, 91;
                     130,127,122,119, 80, 78;
                     135,112,106,103, 99, 94;
                     140,125,108, 97, 90, 84;
                     180,100,100,100,100,100;
                     180,180, 95, 95, 84, 84];

% Run K-Means algorithm. The 'true' at the end tells our function to plot
% the progress of K-Means
[centroids, idx] = runkMeans(X, initial_centroids, max_iters, true);
fprintf('\nK-Means Done.\n\n');

fprintf('Program paused. Press enter to continue.\n');
pause;

