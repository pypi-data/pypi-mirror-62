/*
* StochasticBlockmodel.h
*
*  Created on: 13.08.2014
*      Author: Christian Staudt
*/

#ifndef NETWORKIT_GENERATORS_STOCHASTIC_BLOCKMODEL_HPP_
#define NETWORKIT_GENERATORS_STOCHASTIC_BLOCKMODEL_HPP_

#include <networkit/generators/StaticGraphGenerator.hpp>

namespace NetworKit {


/**
 * @ingroup generators
 */
class StochasticBlockmodel: public StaticGraphGenerator {

public:
    /**
    * Construct a undirected regular ring lattice.
    *
    * @param nNodes 		number of nodes in target graph
    * @param n		number of blocks (=k)
    * @param membership		maps node ids to block ids (consecutive, 0 <= i < nBlocks)
    * @param affinity		matrix of size k x k with edge probabilities betweeen the blocks
    */
    StochasticBlockmodel(count n, count nBlocks, const std::vector<index>& membership, const std::vector<std::vector<double> >& affinity);

    virtual Graph generate();

protected:
        count n;
        count nBlocks;
        std::vector<index> membership;
        std::vector<std::vector<double> > affinity;

};

} /* namespace NetworKit */
#endif // NETWORKIT_GENERATORS_STOCHASTIC_BLOCKMODEL_HPP_
