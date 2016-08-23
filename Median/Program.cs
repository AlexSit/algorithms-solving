using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace Median
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("START START START");
            var basePath = "../../inputs";
            var paths = new List<string>
            {                
                "tc1.txt",                
                //"median.txt"
            };

            foreach (var path in paths)
            {
                using (var file = File.OpenText(Path.Combine(basePath, path)))
                {
                    var text = file.ReadToEnd();
                    var answer = ReadInputAndSolve(text);

                    //var answer = GetAnswer(input);

                    Console.WriteLine($"Actual ANSWER: {answer}");
                }
            }
            Console.WriteLine("the end");
            Console.ReadKey();
        }

        private static int ReadInputAndSolve(string text)
        {
            var lines = text.Split('\n').Where(x => !string.IsNullOrWhiteSpace(x)).ToList();
            var linesCount = lines.Count;

            var m = new int[linesCount];
            var heap = new Heap();
            for (var i = 0; i < linesCount; i++)
            {
                var number = int.Parse(lines[i]);
                AddToHeap(heap, number);
                var mk = GetMedian(heap);
                m[i] = mk;
            }

            var medianSum = m.Aggregate(0, (i, i1) => i + i1);
            var answer = medianSum%10000;
            return answer;
        }

        private static int GetMedian(Heap heap)
        {
            throw new NotImplementedException();
        }

        private static void AddToHeap(Heap heap, int number)
        {
            throw new NotImplementedException();
        }
    }

    internal class Heap
    {
    }
}
