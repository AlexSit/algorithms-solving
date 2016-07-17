using System;

namespace KaratsubaMultiplication
{
    class Program
    {
        static void Main(string[] args)
        {
            var random = new Random();

            const int power = 3;
            for (int i = 0; i < 10; i++)
            {
                var minValue = (int)Math.Pow(10, power);
                var maxValue = (int)Math.Pow(10, power + 1) - 1;

                var A = 160;//random.Next(minValue, maxValue);
                var B = 182;//random.Next(minValue, maxValue);

                var result = DoKaratsubaMultiplication(A, B, 0);

                Console.WriteLine($"Result: {result}");
                var expectedResult = A * B;
                Console.WriteLine($"Expected result = {expectedResult}");
                Console.WriteLine(result == expectedResult ? "Correct!" : "Failed!");
                Console.ReadKey(); 
            }
        }

        private static int ExtractRightPart(int B, double c, double n)
        {
            return B - (int)(c * Math.Pow(10, Math.Floor(n / 2)));
        }

        private static int ExtractLeftPart(int A, double n)
        {
            return (int)Math.Floor(A / Math.Pow(10, Math.Floor(n / 2)));
        }

        private static int DoKaratsubaMultiplication(int A, int B, int level)
        {
            if (A == 0 || B == 0)
            {
                return 0;
            }

            if (A == 1)
            {
                return B;
            }

            if (B == 1)
            {
                return A;
            }

            var n1 = (int)Math.Ceiling(Math.Log10(A));
            var n2 = (int)Math.Ceiling(Math.Log10(B));
            var n = Math.Min(n1, n2);
            if (n == 1 || n == 0)
            {
                return A*B;
            }

            var a = ExtractLeftPart(A, n);
            var b = ExtractRightPart(A, a, n);
            var c = ExtractLeftPart(B, n);
            var d = ExtractRightPart(B, c, n);

            Console.WriteLine($"level = {level}");
            Console.WriteLine($"A = {A}");
            Console.WriteLine($"B = {B}");
            Console.WriteLine($"n = {n}");
            Console.WriteLine($"a = {a}");
            Console.WriteLine($"b = {b}");
            Console.WriteLine($"c = {c}");
            Console.WriteLine($"d = {d}");
            Console.WriteLine();

            Console.WriteLine($"Karatsuba ac (level={level})");
            int ac = DoKaratsubaMultiplication(a, c, level + 1);
            Console.WriteLine($"Karatsuba bd (level={level})");
            int bd = DoKaratsubaMultiplication(b, d, level + 1);

            Console.WriteLine($"Karatsuba gauss (level={level})");
            var gaussTrick = DoKaratsubaMultiplication(a + b, c + d, level + 1) - ac - bd;

            var result = (int)(Math.Pow(10, n) * ac + Math.Pow(10, Math.Floor((double)n / 2)) * gaussTrick + bd);
            Console.WriteLine($"result: {result}, (level={level})");
            return result;
        }
    }
}