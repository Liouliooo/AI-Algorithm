
# coding: utf-8

# In[15]:

import random
import numpy as np
import sys
import copy
# constant
(alpha, beta, rho, Q) = (1.0, 2.0, 0.5, 100.0)
(city_num, ant_num, iter_max) = (76, 70, 50)

# city distance
distance_graph = []
# ant's phernomone
pheromone_graph = []

class Ant(object):
    '''
    蚁群算法解决TSP问题
    此类，描述了一只蚂蚁走一遍城市的：路径，总的路径长度，每只蚂蚁的信息素含量都是Q，
    所以，走的距离越短的蚂蚁，在当前路径段，信息含量越高。蚂蚁选择下一个城市的概率受当前
    信息素含量的影响。
    ID: 蚂蚁编号
    total_distance: 蚂蚁经过的所有路程
    path：蚂蚁行走的路程节点存放到path中，第一个节点随机产生
    move_count：蚂蚁行走步数
    current_city：蚂蚁当前所在city
    open_table_city：蚂蚁行走标记，走过一个城市标记为False，未走过标记为True
    
    ant = Ant(0)
    print (ant.__dict__) # 打印Ant类的所有属性
    '''
    def __init__(self, ID):
        self.ID = ID
        return    # __init__ method should return None
    
    def __lt__(self, other):    # 类之间比较的时候调用这个方法
        return self.total_distance < other.total_distance
    
    def __ant_begin(self):
        # 在这个函数中，要定义所有的类的属性
        self.path = []
        self.total_distance = 0.0
        self.move_count = 0
        self.current_city = -1
        self.open_table_city = [True for i in xrange(city_num)]
        
        city_index = random.randint(1,city_num-1) # random select a city
        self.current_city = city_index
        self.path.append(city_index)  # list can be changed,
        self.open_table_city[city_index] = False
        self.move_count = 1
        return
    
    def __choice_next_city(self):
        # 轮盘赌算法
        next_city = -1
        select_citys_prob = [0.0 for i in xrange(city_num)]
        total_prob = 0.0
        
        for i in xrange(city_num):
            if (self.open_table_city[i]):
                try :
                    select_citys_prob[i] = pow(pheromone_graph[self.current_city][i],alpha) *                    pow((1.0 / distance_graph[self.current_city][i]),beta)
                    # total_prob中保存了当前城市到其他所有城市的概率的和
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError:
                    print 'Division Error!'
                    sys.exit(1)
        
        # select city by way of roulette
        if (total_prob > 0.0):
            temp_prob = random.uniform(0.0, total_prob)
            for i in xrange(city_num):
                if self.open_table_city[i]:
                    # 概率大的城市，更有可能被选中
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break
        if (next_city == -1):
            for i in xrange(city_num):
                if (self.open_table_city[i]):
                    next_city = i
                    break;
        return next_city
    
    def __cal_total_distance(self):
        temp_distance = 0.0
        for i in xrange(1,city_num):
            start, end = self.path[i], self.path[i-1]
            temp_distance += distance_graph[start][end]
            
        end = 0
        temp_distance += distance_graph[start][end]
        self.total_distance = temp_distance
        return
    
    def __move(self, next_city):
        self.path.append(next_city)
        self.open_table_city[next_city] = False
        
        # self.total_distance += distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1
        return
    
    def search_path(self):
        self.__ant_begin()
        while (self.move_count < city_num):
            next_city = self.__choice_next_city()
            self.__move(next_city)
        self.__cal_total_distance()
        return
    

class TSP(object):
    '''
    此类描述了，所有蚂蚁走完一遍城市之后：更新信息素含量，然后再让所有蚂蚁走一遍；如此循环，结果会越来接近于
    全局最优解。
    '''
    def __init__(self, data_path):
        self.load_data(data_path)
        global distance_graph, pheromone_graph
        # ditance matrix
        distance_graph = [[0.0 for col in xrange(city_num)] for raw in xrange(city_num)]
        # pheromone matrix
        pheromone_graph = [[1.0 for col in xrange(city_num)] for raw in xrange(city_num)]
        
        self.ants = [Ant(ID) for ID in xrange(ant_num)]    # Ant, each element is a Ant class.
        self.best_ant = Ant(-1)
        self.best_ant.total_distance = 1 << 31
    
        for i in xrange(city_num):
            for j in xrange(city_num):
                temp_distance = pow((distance_x[i]-distance_x[j]),2) + pow((distance_y[i]-distance_y[j]),2)
                temp_distance = pow(temp_distance, 0.5)
                distance_graph[i][j] = float(int(temp_distance + 0.5))
                pheromone_graph[i][j] = 1.0
        return
    
    def load_data(self, data_path):
        global distance_x,distance_y,city_num, ant_num
        distance_x = []
        distance_y = []
        with open(data_path,'r') as data:
            for index, line in enumerate(data):
                if (line.strip()):
                    xy = line.split(' ')
                    distance_x.append(int(xy[1]))
                    distance_y.append(int(xy[2]))
        return
    
    def search_path(self):
        for i in range(iter_max):
            for ant in self.ants:
                ant.search_path()
                if ant<self.best_ant:
                    self.best_ant = copy.deepcopy(ant)
            self.__update_pheromone_graph()
        return
    
    def __update_pheromone_graph(self):
        # temp_pheromone中保存了所有蚂蚁走过之后，每条路径上信息素含量
        temp_pheromone = [ [0.0 for col in xrange(city_num)] for raw in xrange(city_num)]
        for ant in self.ants:
            for i in xrange(1,city_num):
                start, end = ant.path[i-1], ant.path[i]
                temp_pheromone[start][end] += Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]
                
            end = ant.path[0]
            temp_pheromone[start][end] += Q / ant.total_distance
            temp_pheromone[end][start] = temp_pheromone[start][end]
            
        for i in xrange(city_num):
            for j in xrange(city_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * rho + temp_pheromone[i][j]
        return 
    
if __name__ == '__main__':
    test = TSP('ei76.tsp')
    test.search_path()
    
    print 'Best Path: ',test.best_ant.path
    print 'Best Distance: ', test.best_ant.total_distance

