%% Initial Tank Hydrosurveyor trial

%% Cory Toburen 5/30/2023
clear;clc;
%% Read in Excel Data

table = readtable('plot_workspace.xlsx');

% All data is recorded in one file
% Indexing is used to parse data into 6 trials
% Converted to cm

VB_range{1} = table.VBDepth_m_(1:255)*100; 

VB_range{2} = table.VBDepthT2_m_(1:244)*100;

VB_range{3} = table.VBDepthT2_m_(256:560)*100;

VB_range{4} = table.VBDepthT2_m_(589:870)*100;

VB_range{5} = table.VBDepthT2_m_(887:1058)*100;

VB_range{6} = table.VBDepth_m__1(1:181)*100;


% Measured depths converted to cm

meas_depth(1) = 63.5*2.54; 

meas_depth(2) = 58.75*2.54;

meas_depth(3) = 53.5*2.54;

meas_depth(4) = 46.5*2.54;

meas_depth(5) = 42*2.54;

meas_depth(6) = 65.5*2.54;


for i = 1:6
    VB_mean(i) = mean(VB_range{i});
end


%% Plot measured vs mean

figure(1);clf;

plot(VB_mean,meas_depth,'k*','markersize',8)
hold on
grid on


xlim([100 170])
ylim([100 170])

xlabel('Recorded Average Depth','FontSize',18)
ylabel('Measured Depth','FontSize',18)


%% Calculate and ioncorporate STD into plot 

% Calculate standard deviation
% Creates a variable showing the STD range for each mean trial value
for i = 1:6
    VB_STD(i) = std(VB_range{i});
    VB_meanSTD{i} = [VB_mean(i)-VB_STD(i),VB_mean(i)+VB_STD(i)];
end


%% Linear Regression

% There appears to be some vertical offset (each of the recorded means are slightly
% above the y=x line)
% Couild have been caused by error in the first measurement as all other
% measurements were based off the first 
% Linear regression is used as well as the y = x line to show correlation  
p = polyfit(VB_mean,meas_depth,1);
%f = polyval(p,VB_mean);


figure(3);clf;




x = [100:180];
y = 1.0317*x-1.6709; % From polyfit
y2 = x;


plot(x,y,'r-','LineWidth',2.2)
grid on
hold on
plot(x,y2,'k--','LineWidth',2.2)

plot(VB_mean,meas_depth,'ko','markersize',12,'Linewidth',2.5)

for i = 1:6
    plot([VB_meanSTD{i}(1) VB_meanSTD{i}(2)],[meas_depth(i) meas_depth(i)],'k-')
end


xlim([100 170])
ylim([100 170])

xlabel('HydroSurveyor Recorded Average Depth (cm)','FontSize',18)
ylabel('Measured Depth (cm)','FontSize',18)
legend('Linear Regression line (y = 1.032*x-1.67)','y = x','Recorded Average vs Measured Depth','Location','Northwest','FontSize',18)
title('Hydrosurveyor Tank Test','FontSize',18)
