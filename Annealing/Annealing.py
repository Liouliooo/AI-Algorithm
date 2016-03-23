
# coding: utf-8

# In[3]:

## 程序出错，第一个应先想到的是缩进有没有错误.
import math
import random
import copy
import matplotlib.pyplot as plt

(city_num, alpha) = (76, 0.99)
distance_graph = [[0 for col in xrange(city_num)] for raw in xrange(city_num)]
# city coordinate
dis_x = []
dis_y = []
energe = []

class annealTSP(object):
    def __init__(self,data_path):
        self.city_roads = [i for i in range(city_num)]
        random.shuffle(self.city_roads)
        self.total_distance = 1 << 32
        self.temperature = 2000
        self.__load_data(data_path)
        self.best_distance = 1 << 32
        return
    
    def __load_data(self,data_path):
        global dis_x, dis_y
        global distance_graph
        
        # read data from file
        with open(data_path,'r') as data:
            for index, line in enumerate(data):
                if (line.strip()):
                    xy = line.split(' ')
                    dis_x.append(int(xy[1]))
                    dis_y.append(int(xy[2]))
        
        # city distance matrix
        for i in xrange(city_num):
            for j in xrange(city_num):
                temp_dis = pow((dis_x[i]-dis_x[j]),2)+pow((dis_y[i]-dis_y[j]),2)
                temp_dis = pow(temp_dis,0.5)
                distance_graph[i][j] = float(int(temp_dis + 0.5))
        return
        
    def disturb_tour(self):
        a = random.randint(0,city_num-1)
        b = random.randint(0,city_num-1)
        while a == b:
            a = random.randint(0,city_num-1)
            b = random.randint(0,city_num-1)
        # deepcopy and copy has huge difference.
        temp_path = copy.deepcopy(self.city_roads)        
        temp = temp_path[a]
        temp_path[a] = temp_path[b]
        temp_path[b] = temp
        return temp_path
    
    def total_dis(self,other):
        temp_distance = 0
        for i in range(city_num):
            start,end = other[i-1],other[i]
            temp_distance += distance_graph[start][end]
 
        return temp_distance
    
    def simulated_annealing(self):
        global energe
        while self.temperature > 0.001:
            pro_limit = 0
            count = 0
            while pro_limit < 1000 and count < 1000:
#                 print self.total_distance
                count += 1
                
                current_city_roads = self.city_roads         
                current_distance = self.total_dis(current_city_roads)
                
                next_city_roads = self.disturb_tour() # This is the problem.Every time when i call this function, the order has been changed.
                next_distance = self.total_dis(next_city_roads) # every time when I call this function, the value of self.total_ditance has been changed.

                delta_e = next_distance - current_distance
  
                if (delta_e < 0.0):
                    self.city_roads = next_city_roads
                    self.total_distance = next_distance
                    pro_limit = 0
                else:
                    prob = math.exp((-delta_e)/self.temperature)
                    if prob > random.uniform(0,1):
                        self.city_roads = next_city_roads
                        self.total_distance = next_distance
                        pro_limit = 0
                    pro_limit += 1
            if self.total_distance < self.best_distance:
                self.best_distance = self.total_distance
            
            energe.append(self.total_distance)
            self.temperature = alpha*self.temperature
            
#             print self.best_distance
        return

    
if __name__ == '__main__':
    test = annealTSP('ei76.tsp')
    test.simulated_annealing()

    print (test.city_roads)
    print (test.total_distance)
    print (test.best_distance)

    tem = [i+1 for i in range(len(energe))]

    # plt.scatter(tem, energe)
    plt.xlim(-100,1400)
    plt.plot(tem,energe)
    plt.title('Energy')
    plt.show()

