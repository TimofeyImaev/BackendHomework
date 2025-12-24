class Point {
    double x, y;

    static Point createPoint(double x, double y) {
        var point = new Point();
        point.x = x;
        point.y = y;

        return point;
    }

    double getDistance(Point other) {
        double dx = this.x - other.x;
        double dy = this.y - other.y;

        return Math.sqrt(dx * dx + dy * dy);
    }
}