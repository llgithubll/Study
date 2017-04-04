import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.StdStats;

public class PercolationStats {
    private double mean = 0.0;
    private double std = 0.0;
    private double upperConf = 0.0;
    private double lowerConf = 0.0;

    public PercolationStats(int n, int trials) // perform trials independent experiments on an n-by-n grid
    {
        if (n <= 0 || trials <= 0) {
            throw new IllegalArgumentException();
        }
        double[] trialsRes = new double[trials];
        for (int t = 0; t < trials; t++) {
            Percolation p = new Percolation(n);
            for (int i = 0; i < n * n; i++) {
                int pt, r, c;
                do {
                    pt = (int)(Math.random() * n * n);
                    r = pt / n + 1;
                    c = pt % n + 1;
                } while(p.isOpen(r, c));
                p.open(r, c);
                if (p.percolates()) {
                    trialsRes[t] = 1.0 * i / (n * n);
                    break;
                }
            }
        }

        for (int t = 0; t < trials; t++) {
            mean += trialsRes[t];
        }
        mean /= trials;

        for (int t = 0; t < trials; t++) {
            std += (trialsRes[t] - mean) * (trialsRes[t] - mean);
        }
        std /= trials - 1;
        std = Math.sqrt(std);
        
        lowerConf = mean - 1.96 * std / Math.sqrt(trials + 0.0);
        upperConf = mean + 1.96 * std / Math.sqrt(trials + 0.0);
    }

    public double mean() // sample mean of percolation threshold
    {
        return mean;
    }

    public double stddev() // sample standard deviation of percolation threshold
    {
        return std;
    }

    public double confidenceLo() // low  endpoint of 95% confidence interval
    {
        return lowerConf;
    }

    public double confidenceHi() // high endpoint of 95% confidence interval
    {
        return upperConf;
    }

    public static void main(String[] args) // test client (described below)
    {
        PercolationStats ps = new PercolationStats(Integer.parseInt(args[0]),
                                                   Integer.parseInt(args[1]));
        System.out.println("mean                    = " + ps.mean());
		System.out.println("stddev                  = " + ps.stddev());
		System.out.println("95% confidence interval = " + ps.confidenceLo()
				+ ", " + ps.confidenceHi());                                                  
    }
}