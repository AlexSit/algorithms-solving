using System.Collections.Generic;

namespace Dijkstra
{
    internal class Edge
    {
        public int SourceVertex { get; set; }
        public int Length { get; set; }
        public int DestinationNode { get; set; }        
    }

    internal class NodeInfo
    {
        public bool Explored { get; set; }
        public List<Edge> Edges { get; set; }
    }
}