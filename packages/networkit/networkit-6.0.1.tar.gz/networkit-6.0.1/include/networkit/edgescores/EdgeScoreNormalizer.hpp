/*
 * EdgeScoreNormalizer.h
 *
 *  Created on: 18.11.2014
 *      Author: Michael Hamann
 */

#ifndef NETWORKIT_EDGESCORES_EDGE_SCORE_NORMALIZER_HPP_
#define NETWORKIT_EDGESCORES_EDGE_SCORE_NORMALIZER_HPP_

#include <networkit/graph/Graph.hpp>
#include <networkit/edgescores/EdgeScore.hpp>

namespace NetworKit {

template <typename A>
class EdgeScoreNormalizer : public EdgeScore<double> {

public:
    EdgeScoreNormalizer(const Graph &G, const std::vector<A> &score, bool invert = false, double lower = 0, double upper = 1.0);

    virtual double score(edgeid eid) override;
    virtual double score(node u, node v) override;
    virtual void run() override;

private:
    const std::vector<A> &input;
    bool invert;
    double lower, upper;
};

}

#endif // NETWORKIT_EDGESCORES_EDGE_SCORE_NORMALIZER_HPP_
