/*
C functions to speed up calculations of the model.
*/

#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

double mod(int num, int div){
    // Implements a mod function for that always maps
    // to the range [0,div).

    double res = fmod(num,div);
    return (res >= 0) ? res : res+div;
}

double Magnetization(long* conf, int L){
  double sum = 0;
  int index = 0;

  for(int i = 0; i < L; i++){
    for(int j = 0; j < L; j++){
        sum =  sum + conf[index++];
    }
  }

  return sum;
}

double Energy(long* conf, int L){
  double sum = 0;
  int index = 0, down, right;

  for (int i = 0; i < L; i++){
    for (int j = 0; j < L; j++){
        down = mod(index + L, L);
        right = mod(index + 1, L);
        sum = sum + conf[index]*(conf[down]+conf[right]);
    }
  }
  return sum;
}

void MCSweeps(long* conf, int L, double T, int Nstep){
  int x, y, i_l, i_r, i_u, i_d, index = 0;
  double Enn, dE, P_b, P_flip, r;
  int np[L], nm[L];

  for (int i = 0; i < L; i++){
    np[i] = i+1;
    nm[i] = i-1;
  }
  np[L-1] = 0;
  nm[0] = L-1;

  srand(time(0));

  for(int i = 0; i < Nstep; i++){
    for(int j = 0; j < L*L; j++){
      x = fmod(rand(), L);
      y = fmod(rand(), L);

      index = mod(x*L + y, L*L);

      i_u = mod(nm[x]*L + y, L*L);
      i_d = mod(np[x]*L + y, L*L);
      i_l = mod(x*L + nm[y], L*L);
      i_r = mod(x*L + np[y], L*L);

      //printf("Index (%d): %d %d %d %d \n", index, i_l, i_r, i_u, i_d);


      Enn = -1.0 * conf[index]*(conf[i_l] + conf[i_r]
                              + conf[i_u] + conf[i_d]);

      dE = -2*Enn;

      P_b = (double)exp(-dE/T);

      P_flip = (P_b < 1.0) ? P_b : 1.0;

      r = ((double) rand() / (RAND_MAX));
      //printf("r = %lf P = %lf", r, P_flip);

      if (P_flip > r){
        conf[index] = -1.0 * conf[index];
      }

    }
  }
  return;
}
