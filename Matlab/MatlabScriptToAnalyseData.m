%%Script to analyse data for cell migration project
rows = 1800;
TotalCells = 69;
TotalSets = 10;
folders = dir('CellMigration2D_cc3d*');

distance = zeros(TotalSets*TotalCells,1);
MPD = zeros(TotalSets*TotalCells,1);
displacement = zeros(TotalSets*TotalCells,1);

FiberDeg = zeros(10,1);
    
for setCount = 1:TotalSets
    cd(folders(setCount).name);
        centroid = zeros(rows,TotalCells*2);
        for i = 1:TotalCells
            fileName = strcat('Data',num2str(i),'.csv');
            a = csvread(fileName, 0, 1, [0 1 rows-1 2]);
            for r = 1:rows
                centroid(r,(i-1)*2+1)=a(r,1);
                centroid(r,(i-1)*2+2)=a(r,2);
            end
        end

    for i = 1:TotalCells
        maxDisplacement = 0;
        for r = 2:rows
            disp = sqrt((centroid(r,(i-1)*2+1)-centroid(1,(i-1)*2+1))^2+(centroid(r,(i-1)*2+2)- centroid(1,(i-1)*2+2))^2);
            if(disp > maxDisplacement)
                maxDisplacement = disp;
            end 
            distance((setCount-1)*TotalCells+i) = distance((setCount-1)*TotalCells+i)+ sqrt((centroid(r,(i-1)*2+1)-centroid(r-1,(i-1)*2+1))^2+(centroid(r,(i-1)*2+2)- centroid(r-1,(i-1)*2+2))^2);
        end
        displacement((setCount-1)*TotalCells+i) = sqrt((centroid(r,(i-1)*2+1)-centroid(1,(i-1)*2+1))^2+(centroid(r,(i-1)*2+2)- centroid(1,(i-1)*2+2))^2);
        MPD((setCount-1)*TotalCells+i) = maxDisplacement;
    end
    
%    FDSeq = csvread('FiberDegraded.csv', 0, 1, [0 1 rows-1 1]);
%    FD(setCount) = sum(sum(FDSeq));
cd ..
end
    [distance MPD displacement]