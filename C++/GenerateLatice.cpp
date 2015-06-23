#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>

#define PI 3.14159265358979

void generateMatrix(int, int, int, int, int, double);
int generateLine(int, int, int, int, int, int*);

int main()
{
	generateMatrix(500,500,600,15,20,-10.0);
}

void generateMatrix(int rows, int cols, int noOfFibers, int minLengthOfFiber, int maxLengthOfFiber, double originalAlignment)
{

	int FiberPos[rows][cols];

	int x,y,x2,y2;
	int length;
	time_t t;
	double alignment;

	srand((unsigned) time(&t));
	/* Initializes random number generator */
	
	int cellID = 1;

	for (int fibreID = 1; fibreID <= noOfFibers; fibreID++) 
	{
		alignment = originalAlignment;
		length = minLengthOfFiber+rand()%(maxLengthOfFiber-minLengthOfFiber);

		printf("\nlength = %d\n",length);

		x = length+rand() % (cols-2*length);
		y = length+rand() % (rows-2*length);

		int * points = new int[length*9*2];

		printf("\nalignment = %lf\n",alignment);

		if(alignment<0.0 && alignment>-10.0)
		{
			alignment = double(rand()%10)/3.0;
		}

		if(alignment <= -10.0)
		{
			double yCentre = rows/2;
			double xCentre= cols/2;
			alignment = atan((y-yCentre)/(x-xCentre));
		}
		
		printf("\nAngle=%lf\n", alignment);

		//Calculating end points and generating line
		x2 = (int) round((double) x + (length - 1) * cos(alignment));
		y2 = (int) round((double) y + (length - 1) * sin(alignment));
		int pointCount = generateLine(x, y, x2, y2, length, points);
		
		printf("\nx=%d y=%d x2=%d y2=%d\n",x,y,x2,y2);

		for(int j=0;j<pointCount;j++)
		{
			int x=points[j*2+0];
			int y=points[j*2+1];
			if(FiberPos[x][y] == 0)
			{
				FiberPos[x][y] = 1;
				FILE *fp = fopen("Lattice_600Fibrers_Aligned.piff","a+");
				fprintf(fp,"%d Matrix %d %d %d %d 0 0\n",cellID,x,x,y,y);
				fclose(fp);
				cellID++;
			}
			else
			{
				/*double random = ((double)(rand()%100))/100.0;
				if(random > 0.5)
				{
							FiberPos[x][y] = 0;
							FILE *fp = fopen("Lattice_500Fibrers.piff","a+");
							fprintf(fp,"%d Medium %d %d %d %d 0 0\n",cellID,x-5,x+5,y-5,y+5);
							fclose(fp);
							cellID++;
				}*/
			}	
		}
	}
}

int generateLine(int x0, int y0, int x1, int y1, int lengthOfFiber, int * points)
{
	//printf("%d %d %d %d\n",x0, y0,x1,y1);
	int totalPoints=0;
	int sx, sy;
	int dx = abs(x1-x0);
	int dy = abs(y1-y0);
	if(x0 < x1) sx = 1;
	else sx = -1;
	if(y0 < y1) sy = 1;
	else sy = -1;
	int   err = dx-dy;

	while(1){
		//plot(x0,y0)
		//printf("%d %d\n",x0,y0);
		points[totalPoints*2+0]=x0;
		points[totalPoints*2+1]=y0;
		totalPoints++;
		if(x0 == x1 and y0 == y1) break;
		int e2 = 2*err;
		if (e2 > -dy)
		{
			err = err - dy;
			x0 = x0 + sx;
		}
		if (x0 == x1 && y0 == y1)
		{
			//printf("%d %d\n",x0,y0);
			points[totalPoints*2+0]=x0;
			points[totalPoints*2+1]=y0;
			totalPoints++;
			break;
		}

		if(e2 <  dx){
			err = err + dx;
			y0 = y0 + sy;
		}
	}

	return totalPoints;
}
