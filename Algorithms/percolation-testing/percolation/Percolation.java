import edu.princeton.cs.algs4.WeightedQuickUnionUF;

public class Percolation {
    private boolean[] isOpen;
    private WeightedQuickUnionUF fullUF;
    private WeightedQuickUnionUF openUF;
    private int n;
    private int openCnt; // number Of open sites

    private final int[] dr = { -1, 1, 0, 0 };
    private final int[] dc = { 0, 0, -1, 1 };

    public Percolation(int n) { // create n-by-n grid, with all sites blocked
        if (n <= 0) 
            throw new IllegalArgumentException();
        isOpen = new boolean[n * n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                isOpen[i * n + j] = false;
        fullUF = new WeightedQuickUnionUF(n * n + 1); // extra 1 space as first row's root
        openUF = new WeightedQuickUnionUF(n * n + 2); // extra 2 space as first row's and last row's root
        this.n = n;
        this.openCnt = 0;
    }

    public void open(int row, int col) { // open site (row, col) if it is not open already
        int r = row - 1, c = col - 1;
        if (r < 0 || r >= n || c < 0 || c >= n) {
            throw new java.lang.IndexOutOfBoundsException();
        }
        if (!isOpen[r * n + c]) {
            isOpen[r * n + c] = true;
            openCnt++;
            for (int i = 0; i < 4; i++) {
                int nr = r + dr[i];
                int nc = c + dc[i];
                if (0 <= nr && nr < n && 0 <= nc && nc < n && isOpen[nr * n + nc]) {
                    openUF.union(r * n + c, nr * n + nc);
                    fullUF.union(r * n + c, nr * n + nc);
                }
            }
            if (r == 0) {
                openUF.union(r * n + c, n * n);
                fullUF.union(r * n + c, n * n);
            }
            else if (r == n - 1) {
                openUF.union(r * n + c, n * n + 1);
            }
        }
    }

    public boolean isOpen(int row, int col) { // is site (row, col) open?
        int r = row - 1, c = col - 1;
        if (r < 0 || r >= n || c < 0 || c >= n) 
            throw new java.lang.IndexOutOfBoundsException();
        return isOpen[r * n + c];
    }

    public boolean isFull(int row, int col) { // is site (row, col) full?
        int r = row - 1, c = col - 1;
        if (r < 0 || r >= n || c < 0 || c >= n) {
            throw new java.lang.IndexOutOfBoundsException();
        }
        return isOpen[r * n + c] && fullUF.connected(r * n + c, n * n);
    }

    public int numberOfOpenSites() { // number of open sites
        return openCnt;
    }

    public boolean percolates() { // does the system percolate?
        return openUF.connected(n * n, n * n + 1);
    }

    public static void main(String[] args) { // test client (optional)
    }
}