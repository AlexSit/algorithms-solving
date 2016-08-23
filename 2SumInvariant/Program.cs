using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace _2SumInvariant
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("START START START");
            var basePath = "../../inputs";
            var paths = new List<string>
            {                
                //"tc1.txt",
                //"tc2.txt",
                "2sum.txt"
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

        private static long GetAnswer(Hashtable input)
        {
            List<Tuple<long, long>> answer = new List<Tuple<long, long>>();
            var sums = new Hashtable();
            for (long t = -10000; t <= 10000; t++)
            {
                if (!sums.ContainsKey(t))
                {
                    foreach (var key in input.Keys)
                    {
                        var x = (long) key;
                        var y = t - x;
                        if (x != y)
                        {
                            if (input.ContainsKey(y))
                            {
                                answer.Add(new Tuple<long, long>(x, y));
                                sums.Add(t, true);
                                break;
                            }
                        }
                    }
                }
            }                                

            return answer.Count;
        }

        private static long ReadInputAndSolve(string text)
        {
            var sums = new Dictionary<long,long>();
            for (long i = -10000; i <= 10000; i++)
            {
                sums.Add(i, i);
            }

            long currentSumCount = 0;

            var input = new Hashtable();
            var lines = text.Split('\n').Where(x => !string.IsNullOrWhiteSpace(x)).Select(long.Parse).Distinct().ToList();
            var linesCount = lines.Count;
            var min = lines.Min();
            var max = lines.Max();
            for(var i = 0; i < linesCount; i++)
            {                
                input.Add(i, true);                

                currentSumCount += CheckSumCriteria(input, i, ref sums);                
            }

            return currentSumCount;
        }

        private static long CheckSumCriteria(Hashtable input, long x, ref Dictionary<long, long> sums)
        {
            long foundSumCount = 0;
            var pairs = sums.ToList();
            var count = pairs.Count;
            for (int i = 0; i < count; i++)
            {                                
                var t = sums[pairs[i].Key];
                var y = (t - x);
                if (input.ContainsKey(y))
                {
                    sums.Remove(t);
                    count--;
                    foundSumCount++;
                }                
            }

            return foundSumCount;
        }
    }
}
