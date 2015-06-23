%%Script to analyse data for cell migration project
rows = 1800;
TotalCells = 69;
TotalSets = 10;
folders = dir('CellMigration2D_cc3d*');

MMP = zeros(rows,10);
    
for setCount = 1:TotalSets
    cd(folders(setCount).name);
        fileName = strcat('MMP.csv');
        a = csvread(fileName, 0, 2, [0 2 rows-1 2]);
        MMP(1:rows,setCount) = a(1:rows);
cd ..
end
    

for i=1:1800
    MMP(i,11) = mean(MMP(i,1:10));
    MMP(i,12) = std(MMP(i,1:10));
end