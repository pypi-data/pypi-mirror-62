/*
 * GraphIO.h
 *
 *  Created on: 09.01.2013
 *      Author: Christian Staudt (christian.staudt@kit.edu)
 */

#ifndef NETWORKIT_IO_GRAPH_IO_HPP_
#define NETWORKIT_IO_GRAPH_IO_HPP_

#include <string>

#include <networkit/graph/Graph.hpp>
#include <networkit/auxiliary/Log.hpp>

namespace NetworKit {

/**
 * @ingroup io
 */
class GraphIO {
public:
    /**
     * Writes graph to text file in edge list format.
     * Keep in mind that isolated nodes are ignored.
     *
     * @param[in]	G	graph
     * @param[in]	path	file path
     *
     * Edge list format:
     * 		for each edge {u, v}:
     * 			 write line "u v"
     */
    virtual void writeEdgeList(Graph& G, std::string path);


    /**
     * Writes graph to text file in adjacency list format.
     *
     * @param[in]	G	graph
     * @param[in]	path	file path
     *
     * Adjacency list format:
     * 		for each node v:
     * 			write "v"
     * 			write " x" for each edge {v, x}
     * 			end line
     */
    virtual void writeAdjacencyList(Graph& G, std::string path);


};

} /* namespace NetworKit */
#endif // NETWORKIT_IO_GRAPH_IO_HPP_
