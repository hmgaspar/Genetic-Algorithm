function [i] = roulette(values,fitness)
n_rand = rand()*fitness;
sum_fit = 0;
for i=1:length(values),
    sum_fit = sum_fit + values(i);
    if sum_fit >= n_rand
           break;
    end
end
  