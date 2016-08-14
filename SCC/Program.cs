using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;

namespace SCC
{
    class Program
    {
        private static int _t;
        private static Dictionary<int, int> _finishingTimes = new Dictionary<int, int>();
        private static int _currentLeaderNumber;
        private static int[] _leaders;

        private static List<NodeInfo> _convertedInput;
        private static int _convertedInputMax;
                
        private static int[] _answer = new int[5];

        private static int _currentDfsNumber;
        private static int _currentDfsReversedNumber;

        static void Main(string[] args)
        {
            var stackSize = 50*000*000;
            var thread = new Thread(Target, stackSize);
            thread.Start();
        }

        private static void Target()
        {
            Console.WriteLine("START START START");            
            var paths = new List<string>
            {
                //"tc1.txt",
                //"tc2.txt",
                //"tc3.txt",
                //"tc4.txt",
                "../../input.txt"
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
            ResetInputData();

            Console.WriteLine($"test case: {testCase.FilePath}");

            int[] actualAnswer;
            
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

            Console.WriteLine($"Expected: {string.Join(", ", testCase.Answer)}, Actual: {string.Join(", ", actualAnswer)}");
            if (!testCase.Answer.SequenceEqual(actualAnswer) && testCase.Answer != null)
            {
                throw new Exception($"Test case {testCase.FilePath} failed!");
            }
            Console.WriteLine("-------------------");
            Console.WriteLine();
        }

        private static void ResetInputData()
        {
            _t = 0;
            _finishingTimes = new Dictionary<int, int>();
            _currentLeaderNumber = 0;

            _answer = new int[5];
        }

        private static void Scc(List<Tuple<int, int>> input)
        {
            _convertedInput = PrepareInput(input);
            _leaders = new int[_convertedInput.Count];

            DfsForFinishingTimes();
            _convertedInput.ForEach(x => x.Explored = false);

            DfsForScc();

            CollectTop5Leaders();
        }

        private static void CollectTop5Leaders()
        {
            var leaders = new Dictionary<int, List<int>>();
            for (int i = 0; i < _leaders.Length; i++)
            {
                if (!leaders.ContainsKey(_leaders[i]))
                {
                    leaders[_leaders[i]] = new List<int>();
                }

                leaders[_leaders[i]].Add(i+1);
            }

            var topLeaders = leaders.OrderByDescending(x => x.Value.Count).Take(5).ToList();
            for (int i = 0; i < topLeaders.Count; i++)
            {
                _answer[i] = topLeaders[i].Value.Count;
            }
        }

        private static List<NodeInfo> PrepareInput(List<Tuple<int, int>> input)
        {
            var convertedInput = input.GroupBy(x => x.Item1, x=>x.Item2, (key, values) => new NodeInfo
            {
                I = key,
                Explored = false,
                DestinationNodes = values.ToArray()
            })
            .ToList();

            var count = convertedInput.Count;
            for (int i = 0; i < count; i++)
            {
                if (convertedInput[i].I != i + 1)
                {
                    convertedInput.Insert(i, new NodeInfo
                    {
                        I = i+1,
                        Explored = false,
                        DestinationNodes = new int[0]
                    });
                    count++;
                }
            }            

            _convertedInputMax = convertedInput.Max(x => x.I);
            return convertedInput.OrderBy(x=>x.I).ToList();            
        }

        private static void DfsForFinishingTimes()
        {
            _t = 0;
            for (var i = _convertedInputMax; i >= 1; i--)
            {
                if (!_convertedInput[i - 1].Explored)
                {
                    _currentDfsReversedNumber = i;
                    DfsReversed();
                }
            }
        }

        private static void DfsReversed()
        {
            var node = _convertedInput[_currentDfsReversedNumber - 1];
            node.Explored = true;
            //NOTE
            var destinationNodes = _convertedInput.Where(x => x.DestinationNodes.Contains(_currentDfsReversedNumber)); //            var destinationNodes = _convertedInput[i-1].DestinationNodes;
            foreach (var dstNodeIndex in destinationNodes)
            {
                var dstNode = _convertedInput[dstNodeIndex.I - 1];
                if (!dstNode.Explored)
                {
                    _currentDfsReversedNumber = dstNodeIndex.I;
                    DfsReversed();
                }
            }
            _t++;            
            _finishingTimes[_t] = _currentDfsReversedNumber;
            PrintIntermediateResult(_t);
        }

        private static void Dfs()
        {
            var node = _convertedInput[_currentDfsNumber - 1];
            node.Explored = true;
            _leaders[_currentDfsNumber - 1] = _currentLeaderNumber;
            foreach (var dstNodeIndex in node.DestinationNodes)
            {
                var dstNode = _convertedInput[dstNodeIndex - 1];
                if (!dstNode.Explored)
                {
                    _currentDfsNumber = dstNodeIndex;
                    Dfs();
                }
            }            
        }

        private static void DfsForScc()
        {
            _currentLeaderNumber = 0;
            var maxFinishingTime = _convertedInputMax;
            for (var finishingTime = maxFinishingTime; finishingTime >= 1; finishingTime--)
            {                
                var i = _finishingTimes[finishingTime];
                if (!_convertedInput[i - 1].Explored)
                {
                    _currentLeaderNumber = finishingTime;
                    _currentDfsNumber = i;
                    PrintIntermediateResult(i);
                    Dfs();
                }
            }
        }

        private static void PrintIntermediateResult(int i)
        {
            if (i > 0 && i < 1000 && i % 100 == 0)
            {
                Console.WriteLine(i);
            }
            else if (i >= 1000 && i < 10000 && i % 1000 == 0)
            {
                Console.WriteLine(i);
            }
            else if (i >= 10000 && i % 10000 == 0)
            {
                Console.WriteLine(i);
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
