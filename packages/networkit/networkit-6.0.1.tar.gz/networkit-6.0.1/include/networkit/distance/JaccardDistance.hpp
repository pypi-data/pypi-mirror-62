/*
 * JaccardDistance.h
 *
 *  Created on: 17.11.2014
 *      Author: Michael Hamann, Gerd Lindner
 */

#ifndef NETWORKIT_DISTANCE_JACCARD_DISTANCE_HPP_
#define NETWORKIT_DISTANCE_JACCARD_DISTANCE_HPP_

#include <networkit/distance/NodeDistance.hpp>
#include <networkit/graph/Graph.hpp>
#include <networkit/auxiliary/Timer.hpp>


namespace NetworKit {

/**
 * @ingroup distance
 * Jaccard distance assigns a distance value to pairs of nodes
 * according to the similarity of their neighborhoods. Note that we define the JaccardDistance as 1-JaccardSimilarity.
 */
class JaccardDistance: public NodeDistance {

public:

    /**
     * @param G The graph.
     * @param triangles Edge attribute containing the number of triangles each edge is contained in.
     */
    JaccardDistance(const Graph& G, const std::vector<count>& triangles);

    /**
     * REQ: Needs to be called before getEdgeScores delivers meaningful results.
     */
    virtual void preprocess();

    /**
     * Returns the Jaccard distance between node @a u and node @a v.
     * @return Jaccard distance between the two nodes.
     */
    virtual double distance(node u, node v);

    /**
     * Returns the Jaccard distances between all connected nodes.
     * @return Vector containing the Jaccard distances between all connected pairs of nodes.
     */
    std::vector<double> getEdgeScores();

protected:
    const std::vector<count>& triangles;
    std::vector<double> jDistance; //result vector

    inline double getJaccardDistance(count degU, count degV, count t);

};

} /* namespace NetworKit */
#endif // NETWORKIT_DISTANCE_JACCARD_DISTANCE_HPP_
