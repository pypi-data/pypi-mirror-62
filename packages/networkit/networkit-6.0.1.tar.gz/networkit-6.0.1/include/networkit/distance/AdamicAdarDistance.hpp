/*
 * AdamicAdarDistance.h
 *
 *  Created on: 18.11.2014
 *      Author: Michael Hamann, Gerd Lindner
 */

#ifndef NETWORKIT_DISTANCE_ADAMIC_ADAR_DISTANCE_HPP_
#define NETWORKIT_DISTANCE_ADAMIC_ADAR_DISTANCE_HPP_

#include <networkit/graph/Graph.hpp>
#include <networkit/distance/NodeDistance.hpp>

namespace NetworKit {

/**
 * @ingroup distance
 * An implementation of the Adamic Adar distance measure.
 */
class AdamicAdarDistance : public NodeDistance {

protected:
    std::vector<double> aaDistance; //result vector

    void removeNode(Graph& graph, node u);

public:

    /**
     * @param G The graph.
     */
    AdamicAdarDistance(const Graph& G);

    /**
     * Computes the Adamic Adar distances of all connected pairs of nodes.
     * REQ: Needs to be called before distance() and getEdgeScores() deliver meaningful results!
     */
    virtual void preprocess();

    /**
     * Returns the Adamic Adar distance between node @a u and node @a v.
     * @return Adamic Adar distance between the two nodes.
     */
    virtual double distance(node u, node v);

    /**
     * Returns the Adamic Adar distances between all connected nodes.
     * @return Vector containing the Adamic Adar distances between all connected pairs of nodes.
     */
    virtual std::vector<double> getEdgeScores();

};

} /* namespace NetworKit */

#endif // NETWORKIT_DISTANCE_ADAMIC_ADAR_DISTANCE_HPP_
