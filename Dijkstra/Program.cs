using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace Dijkstra
{
    class Program
    {
        private static Dictionary<int, int> _pathLengths = new Dictionary<int, int>();
        private static int _numberOfNodesExplored = 0;
        private static Dictionary<int, NodeInfo> _input;
        private static int _inputCount;

        static void Main(string[] args)
        {
            Console.WriteLine("START START START");
            var basePath = "../../inputs";
            var paths = new List<string>
            {                
                //"tc1.txt",                
                //"input.txt",
                "new_testcase.txt"
            };

            foreach (var path in paths)
            {
                using (var file = File.OpenText(Path.Combine(basePath, path)))
                {
                    var text = file.ReadToEnd();

                    var input = ProcessTestCaseText(text);
                    _input = input;
                    _inputCount = input.Count;
                    var answer = ExecuteDijkstra();
                    Console.WriteLine("ANSWER: " + string.Join("\n", _pathLengths.Select(x => $"To vertex: {x.Key}, length: {x.Value}")));
                    //Console.WriteLine($"Answer is: {string.Join(",", answer)}");                    
                }
            }
            Console.WriteLine("the end");
            Console.ReadKey();
        }        

        private static Dictionary<int, NodeInfo> ProcessTestCaseText(string text)
        {
            var lines = text.Split('\n')
               .Where(x => !string.IsNullOrWhiteSpace(x))
               .ToList();

            var input = new Dictionary<int, NodeInfo>();

            for (int i = 0; i < lines.Count; i++)
            {
                var numbers = lines[i]
                    .Split('\t', ' ')
                    .Where(x => !string.IsNullOrWhiteSpace(x))
                    .ToList();

                var key = int.Parse(numbers[0]);
                if (!input.ContainsKey(key))
                {
                    input.Add(key, new NodeInfo
                    {
                        Explored = false,
                        Edges = new List<Edge>()
                    });
                }
                else
                {
                    throw new Exception("ключ не ожидался");
                }

                foreach (var n in numbers)
                {
                    if (n != numbers[0])
                    {
                        var edgeInfo = n.Split(',');
                        var dstNode = int.Parse(edgeInfo[0]);
                        var length = int.Parse(edgeInfo[1]);                        
                        input[key].Edges.Add(new Edge
                        {
                            SourceVertex = key,
                            DestinationNode = dstNode,
                            Length = length
                        });
                    }                        
                }
            }
            
            return input;
        }

        private static int[] ExecuteDijkstra()
        {
            // start with vertex 1            
            const int startVertex = 1;
            SetNodeExplored(startVertex, 0);            

            // while unexplored vertices left - area V
            while (UnexploredLeft())
            {

                // among all edges leaving X (explored area) and ending in V
                var edgesFromXtoV = GetSplitEdges();
                // choose such edge that A[r] + l(vw) is minimum; A[r] - already computed, l(vw) - chosen edge
                Edge minLengthEdge;
                int minLength;
                ChooseMinimumEdge(edgesFromXtoV, out minLength, out minLengthEdge);
                // Add w to X and set A[w] = A[v] + l(vw)                
                var shortestPath = _pathLengths[minLengthEdge.SourceVertex] + minLengthEdge.Length;
                SetNodeExplored(minLengthEdge.DestinationNode, shortestPath);                
            }
            return new int[0];
            //7,37,59,82,99,115,133,165,188,197
            //return new[]
            //{
            //    _pathLengths[7],
            //    _pathLengths[37],
            //    _pathLengths[59],
            //    _pathLengths[82],
            //    _pathLengths[99],
            //    _pathLengths[115],
            //    _pathLengths[133],
            //    _pathLengths[165],
            //    _pathLengths[188],
            //    _pathLengths[197]
            //};
        }

        private static void ChooseMinimumEdge(List<Edge> edgesFromXtoV, out int minLength, out Edge minLengthEdge)
        {
            minLength = _pathLengths[edgesFromXtoV[0].SourceVertex] + edgesFromXtoV[0].Length;
            minLengthEdge = edgesFromXtoV[0];
            for (int index = 1; index < edgesFromXtoV.Count; index++)
            {
                var edge = edgesFromXtoV[index];
                var currentLength = _pathLengths[edge.SourceVertex] + edge.Length;
                if (currentLength < minLength)
                {
                    minLength = currentLength;
                    minLengthEdge = edge;
                }
            }
        }

        private static void SetNodeExplored(int startVertex, int shortestPath)
        {
            _input[startVertex].Explored = true;
            _pathLengths[startVertex] = shortestPath;
            _numberOfNodesExplored++;
        }

        private static List<Edge> GetSplitEdges()
        {
            var splitEdges = new List<Edge>();
            foreach (var nodeInfo in _input)
            {
                if (nodeInfo.Value.Explored)
                    //nodeInfo.Value.Edges.Exists(edge => !_input[edge.DestinationNode].Explored))
                {
                    foreach (var edge in nodeInfo.Value.Edges)
                    {
                        if (!_input[edge.DestinationNode].Explored)
                        {
                            splitEdges.Add(edge);
                        }
                    }
                    //var edges = nodeInfo.Value.Edges.Where(x => !_input[x.DestinationNode].Explored);
                    //splitEdges.AddRange(edges);
                }
            }
            return splitEdges;
            //return
            //    _input
            //        .Where(x => x.Value.Explored && x.Value.Edges.Exists(edge => !_input[edge.DestinationNode].Explored))
            //        .SelectMany(x => x.Value.Edges)
            //        .Where(x=> !_input[x.DestinationNode].Explored)
            //        .ToList();
        }

        private static bool UnexploredLeft()
        {
            return _numberOfNodesExplored < _inputCount;
        }
    }
}
