#include "genetic.hpp"

/* 随机生成字符序列 */
string Random_string(int num)
{
    // ASCII码 [32,126] 包含了所有可见字符，共有95个
    string result = "";
    for (int i = 0; i < num; i++)
    {
        int ascii = 32 + rand() % 95;
        result += char(ascii);
    }
    return result;
}

/* 由父母生成子代 */
string generate_child(string mother, string father, int mid)
{
    string child = "";
    for (int i = 0; i<mid; i++)
    {
        child = child + mother[i];
    }
    for (int i = mid; i<father.size(); i++)
    {
        child = child + father[i];
    }
    return child;
}

/* 子代发生变异 */
string mutate(string child)
{
    string mutate = child;
    mutate[rand()%mutate.size()] = char(32+rand()%95);
    return mutate;
}
/* 计算适应性评分 */
double Fitness_score(string src_str, string g_str)
{
    double score = 0;
    for (int i = 0; i < src_str.size(); i++)
    {
        score += (src_str[i] - g_str[i]) * (src_str[i] - g_str[i]);
    }
    if (0 == score) { return 200; }
    else { return 100/score; }
}

/* 快速排序，根据适应性评分对解池中的解序列进行排序 */
void quick_sort(string src_str, vector<string> &solution, int head, int tail)
{
    if (tail-head<=1) { return ; }
    int begin = head, end = tail-1;
    string pivot = solution[begin];
    while (begin < end)
    {
        while (Fitness_score(src_str, solution[end]) <= Fitness_score(src_str, pivot) && (begin<end))
        {
            end--;
        }
        string temp = solution[begin];
        solution[begin] = solution[end];
        solution[end] = temp;

        while (Fitness_score(src_str, solution[begin]) > Fitness_score(src_str, pivot) && begin<end)
        {
            begin++;
        }
        string temp2 = solution[begin];
        solution[begin] = solution[end];
        solution[end] = temp2;
    }

    quick_sort(src_str, solution, head, begin);
    quick_sort(src_str, solution, end+1, tail);
}

/* 遗传算法主体 */
void Genetic_something(string some_str)
{
    int solution_num = 1000;
    vector<string> gene_pool; // 解池，也就是初始基因
    for (int i = 0; i < solution_num; i++)
    {
        srand(time(NULL) + i); // 随机数种子，这个不好用
        string result = Random_string(some_str.size());
        gene_pool.push_back(result);
    }

    quick_sort(some_str, gene_pool, 0, gene_pool.size());    // 对解序列进行排序
    
    double score_sum = 0;
    vector <double> scores;    // 解序列的分数
    vector <double> proportion; // 分数比例
    for (int i = 0; i<solution_num; i++)
    {
        scores.push_back(Fitness_score(some_str, gene_pool[i]));
        score_sum += Fitness_score(some_str, gene_pool[i]);
        // cout << Fitness_score(some_str, gene_pool[i]) << endl;
    }

    /* 产生的子代解的个数与解池的个数相同 */
    for (int i = 0; i<solution_num; i++)
    {
        proportion.push_back(scores[i]/score_sum);
    }
 
    /* 采用轮盘赌算法从解池中选择两组解作为父母 */    // 考虑如果选中的父母解是相同的，应该如何处理？
    vector <string> parent_pool = gene_pool;
    vector <string> child_pool;
    int i=5000;
    while (i-->0)
    {
        
        for (int i = 0; i<solution_num; i++)
        {
            // mother and father
            string parents[2];
            int mid = some_str.size()/2;
            for (int j=0; j<2; j++)
            {
                int choose = 0;
                double rd_num =  double(random()%10000)/10000;
                for (int k = 0; k<solution_num; k++)
                {
                    rd_num = rd_num - proportion[k];
                    if (rd_num<=0)
                    {
                        choose = k;
                        break;
                    }
                }
                parents[j] = parent_pool[choose];
            }
            double mutate_num =  double(random()%10000)/10000;
            string child = generate_child(parents[0], parents[1], mid);
            if (mutate_num < 0.05) { child = mutate(child); }
            child_pool.push_back(child);
        }

        // 为解序列排序
        quick_sort(some_str, child_pool, 0, child_pool.size());    // 对解序列进行排序
        double score_sum = 0;
        vector <double> scores;    // 解序列的分数
        vector <double> proportion; // 分数比例
        for (int i = 0; i<solution_num; i++)
        {
            scores.push_back(Fitness_score(some_str, child_pool[i]));
            score_sum += Fitness_score(some_str, child_pool[i]);
        }

        // 产生的子代解的个数与解池的个数相同
        for (int i = 0; i<solution_num; i++)
        {
            proportion.push_back(scores[i]/score_sum);
        }
        cout << child_pool[1] << "\t" << some_str << endl;
        if (scores[0] == 200) { break; }

        parent_pool.clear();
        for (int i=0; i<solution_num; i++)
        {
            parent_pool.push_back(child_pool[i]);
        }
        child_pool.clear();
    }
}
