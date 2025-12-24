public class Main {
    public static void main(String[] args) {
        // Создаем первую точку с координатами (3, 4)
        Point point1 = Point.createPoint(3, 4);

        // Создаем вторую точку с координатами (1, 2)
        Point point2 = Point.createPoint(1, 2);

        // Вычисляем расстояние между точками
        double distance = point1.getDistance(point2);

        // Выводим результат
        System.out.println("Точка 1: (" + point1.x + ", " + point1.y + ")");
        System.out.println("Точка 2: (" + point2.x + ", " + point2.y + ")");
        System.out.println("Расстояние между точками: " + distance);
    }
}
