/*
 * KruskalMSF.h
 *
 *  Created on: 03.09.2015
 *      Author: Henning
 */

#ifndef NETWORKIT_GRAPH_KRUSKAL_MSF_HPP_
#define NETWORKIT_GRAPH_KRUSKAL_MSF_HPP_

#include <networkit/Globals.hpp>
#include <networkit/graph/Graph.hpp>
#include <networkit/graph/SpanningForest.hpp>

namespace NetworKit {

/**
 * Creates a minimum spanning tree for each connected component.
 * @ingroup graph
 */
class KruskalMSF: public SpanningForest {
public:
    KruskalMSF(const Graph& G);
    virtual ~KruskalMSF() = default;

    /**
     * Computes for each component a minimum weight spanning tree
     * (or simply a spanning tree in unweighted graphs).
     * Uses Kruskal's algorithm.
     * Time complexity: sort(n) + n * inverse Ackermann(n, m).
     */
    virtual void run() override;
};

} /* namespace NetworKit */
#endif // NETWORKIT_GRAPH_KRUSKAL_MSF_HPP_
