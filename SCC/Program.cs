using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace SCC
{
    class Program
    {
        private static int _t = 0;
        private static Dictionary<int, int> _finishingTimes = new Dictionary<int, int>();
        private static int _currentLeaderNumber = 0;
        private static int[] _leaders;

        private static int[] _answer = new int[5]; 

        static void Main(string[] args)
        {
            var paths = new List<string>
            {
                "tc1.txt",
                //"tc2.txt",
                //"tc3.txt",
                //"tc4.txt"
                //"input.txt"               
            };

            var testCases = new List<TestCase>();

            foreach (var path in paths)
            {
                using (var file = File.OpenText(path))
                {
                    var text = file.ReadToEnd();

                    List<Tuple<int, int>> input;
                    int[] answer;
                    ProcessTestCaseText(text, out input, out answer);

                    testCases.Add(
                        new TestCase
                        {
                            FilePath = path,
                            Input = input,
                            Answer = answer
                        }
                    );
                }
            }
            foreach (var testCase in testCases)
            {
                AssertTestCase(testCase);
            }

            Console.WriteLine("the end");
            Console.ReadKey();
        }

        private static void AssertTestCase(TestCase testCase)
        {
            Console.WriteLine($"test case: {testCase.FilePath}");

            int[] actualAnswer = null;
            
            //var log = "";
            try
            {
                Scc(testCase.Input);
                actualAnswer = _answer;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                return;
            }
        
            if (actualAnswer == null)
            {
                throw new Exception("Couldn't find the answer!");
            }

            Console.WriteLine($"Expected: {testCase.Answer}, Actual: {actualAnswer}");
            if (testCase.Answer.SequenceEqual(actualAnswer) && testCase.Answer != null)
            {
                throw new Exception($"Test case {testCase.FilePath} failed!");
            }
            Console.WriteLine("-------------------");
            Console.WriteLine();
        }

        private static void Scc(List<Tuple<int, int>> input)
        {
            var convertedInput = PrepareInput(input);
            _leaders = new int[convertedInput.Count];

            DfsForFinishingTimes(convertedInput);
            DfsForScc(convertedInput);

            CollectTop5Leaders();
        }

        private static void CollectTop5Leaders()
        {
            var leaders = new Dictionary<int, List<int>>();
            for (int i = 0; i < _leaders.Length; i++)
            {
                if (!leaders.ContainsKey(_leaders[i]))
                {
                    leaders[i + 1] = new List<int>();
                }

                leaders[i + 1].Add(_leaders[i]);
            }

            var topLeaders = leaders.OrderByDescending(x => x.Value.Count).Take(5).ToList();
            for (int i = 0; i < topLeaders.Count; i++)
            {
                _answer[i] = topLeaders[i].Value.Count;
            }
        }

        private static List<NodeInfo> PrepareInput(List<Tuple<int, int>> input)
        {
            //var result = new List<Tuple<bool, int[]>>();
            //for (int i = 0; i < input.Count; i++)
            //{
            //    if(result.length)
            //}
            return input.GroupBy(x => x.Item1, x=>x.Item2, (key, values) => new NodeInfo
            {
                I = key,
                Explored = false,
                DestinationNodes = values.ToArray()
            }).ToList();            
        }

        private static void DfsForFinishingTimes(List<NodeInfo> input)
        {
            _t = 0;
            for (var i = input.Max(x=>x.I); i >= 1; i--)
            {
                if (!input[i - 1].Explored)
                {
                    DfsReversed(input, i);
                }
            }
        }

        private static void DfsReversed(List<NodeInfo> input, int i)
        {
            var node = input[i - 1];
            node.Explored = true;
            var destinationNodes = input.Where(x => x.DestinationNodes.Contains(i)).Select(x => x.I);
            foreach (var dstNodeIndex in destinationNodes)
            {
                var dstNode = input[dstNodeIndex - 1];
                if (!dstNode.Explored)
                {
                    DfsReversed(input, dstNodeIndex);
                }
            }
            _t++;            
            _finishingTimes[i - 1] = _t;
        }

        private static void Dfs(List<NodeInfo> input, int i)
        {
            var node = input[i - 1];
            node.Explored = true;
            _leaders[i - 1] = _currentLeaderNumber;
            foreach (var dstNodeIndex in node.DestinationNodes)
            {
                var dstNode = input[dstNodeIndex - 1];
                if (!dstNode.Explored)
                {
                    Dfs(input, dstNodeIndex);
                }
            }            
        }

        private static void DfsForScc(List<NodeInfo> input)
        {
            _currentLeaderNumber = 0;
            for (var i = input.Max(x => x.I); i >= 1; i--)
            {
                if (!input[i - 1].Explored)
                {
                    _currentLeaderNumber = i;
                    Dfs(input, i);
                }
            }
        }

        private static void ProcessTestCaseText(string text, out List<Tuple<int, int>> input, out int[] answer)
        {
            var lines = text.Split('\n')
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .ToList();

            answer = null;
            input = new List<Tuple<int, int>>();

            for (int i = 0; i < lines.Count; i++)
            {
                if (lines[i].ToLower().Contains("ans"))
                {
                    var answerString = lines[i].Split(':', '-')[1];
                    answer = answerString.Split(',').Select(int.Parse).ToArray();
                    return;
                }
                
                input.Add(ProcessLine(lines[i]));
            }
        }

        private static Tuple<int, int> ProcessLine(string line)
        {
            var numbers = line
                .Split(' ')
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .Select(x => int.Parse(x.Trim()))
                .ToList();

            return new Tuple<int, int>(numbers[0], numbers[1]);
        }
    }
}
