// #include <bits/stdc++.h>
#include <unordered_map>
#include <vector>

#define INF 1e20
#define EPS 1e-8
using namespace std;

int dcmp(double x) {
	if (fabs(x) < EPS)
		return 0;
	return x>0 ? 1:-1;
}


// typedef int node_t;
typedef vector<pair<int, double> > edgeVector_t;

struct Hungarian_t {
    struct vertex_t {
        int v;
        double w;

        vertex_t(int v = 0, double w = 0)
            : v(v)
            , w(w)
        {
        }
    };

    vector<int> yx, xy;
    vector<double> lx, ly;
    vector<bool> S, T;
    vector<double> slack;
    vector<edgeVector_t> weights;

    int Tsz, Wsz;

    Hungarian_t()
    {
        clear();
    }

    void init(int n = 0)
    {
        clear();
        yx.resize(Tsz, -1);
        xy.resize(Wsz, -1);
        lx.resize(Wsz, 0);
        ly.resize(Tsz, 0);
        S.resize(Wsz, false);
        T.resize(Tsz, false);
        slack.resize(Tsz, 0);
    }

    void clear()
    {
        yx.clear();
        xy.clear();
        lx.clear();
        ly.clear();
        S.clear();
        T.clear();
        slack.clear();
    }

    void build(int Tsz, int Wsz, vector<edgeVector_t>& weights)
    {
        this->Tsz = Tsz;
        this->Wsz = Wsz;
        this->weights = weights;
        //assert(Tsz >= Wsz);
        int vertexN = max(Tsz, Wsz);

        init(vertexN);
    }

    bool dfs(int x)
    {
        int y;
        S[x] = true;

        // TODO: 86-88循环
        edgeVector_t& edges = weights[x];
        for (int i = 0; i < edges.size(); ++i) {
            int y = edges[i].first;
            double w = edges[i].second;
            if (T[y])
                continue;

            double tmp = lx[x] + ly[y] - w;
            if (dcmp(tmp) == 0) {
                T[y] = true;
                if (yx[y] == -1 || dfs(yx[y])) {
                    yx[y] = x;
                    xy[x] = y;
                    return true;
                }
            } else {
                slack[y] = min(slack[y], tmp);
            }
        }

        return false;
    }

    bool update()
    {
        double mn = INF;
        for (int i = 0; i < Tsz; ++i) {
            if (!T[i]) {
                mn = min(mn, slack[i]);
            }
        }
        if (mn == INF || dcmp(mn) == 0) {
            return false;
        }
        for (int i = 0; i < Wsz; ++i) {
            if (S[i])
                lx[i] -= mn;
        }
        for (int i = 0; i < Tsz; ++i) {
            if (T[i])
                ly[i] += mn;
            else
                slack[i] -= mn;
        }
        return true;
    }

    void weightedMaximumMatch()
    {
        fill(lx.begin(), lx.end(), 0.0);
        fill(ly.begin(), ly.end(), 0.0);
        fill(xy.begin(), xy.end(), -1);
        fill(yx.begin(), yx.end(), -1);
        for (int x = 0; x < Wsz; ++x) {
            edgeVector_t& edges = weights[x];
            for (int i = 0; i < edges.size(); ++i) {
                int y = edges[i].first;
                double tmp = edges[i].second;
                lx[x] = max(lx[x], tmp);
            }
        }

        for (int x = 0; x < Wsz; ++x) {
            if (weights[x].empty()) {
                continue;
            }
            fill(slack.begin(), slack.end(), INF);
            for (;;) {
                fill(S.begin(), S.end(), false);
                fill(T.begin(), T.end(), false);
                if (dfs(x)) {
                    break;
                } else {
                    if (!update()) {
                        break;
                    }
                }
            }
        }
    }

    void match(vector<int>& w_alloc)
    {
        // cout << "Run Hungarian Algo, Tsz: " << Tsz << " Wsz: " << Wsz << endl;
        w_alloc.clear();
        weightedMaximumMatch();

        for (int x = 0; x < Wsz; x++) {
            // cout << "x: " << x << " " << xy[x] << endl;
            // fflush(stdout);
            w_alloc.push_back(xy[x]);
        }
#ifdef LOCAL_DEBUG
        for (int x = 0; x < Wsz; ++x) {
            assert(xy[x] != -1);
        }
#endif
    }
};

extern "C" {
double MaxProfMatching(const double *cost, int n, int m, int *Lmate)  {
    vector<edgeVector_t> weights;
    // convert cost into weights
    for (int i = 0; i < n; i++) {
        edgeVector_t edges;
        for (int j = 0; j < m; j++) {
            if (dcmp(cost[m * i + j]) >= 0) {
                edges.push_back(make_pair(j, cost[m * i + j]));
            }
        }
        weights.push_back(edges);
    }
    vector<int> w_alloc;
    Hungarian_t hungarian;
    hungarian.build(m, n, weights);
    hungarian.match(w_alloc);
    // convert w_alloc to Lmate and Rmate
    double value = 0;
    for (int i = 0; i < w_alloc.size(); i++) {
        int mate = w_alloc[i];
        Lmate[i] = mate;
        if (mate != -1) {
            value += cost[i * m + mate];
        }
    }
    return value;
}
}
