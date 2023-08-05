/*
 * NeighborsMeasureIndex.h
 *
 *  Created on: 05.04.2015
 *      Author: Kolja Esders (kolja.esders@student.kit.edu)
 */

#ifndef NETWORKIT_LINKPREDICTION_NEIGHBORS_MEASURE_INDEX_HPP_
#define NETWORKIT_LINKPREDICTION_NEIGHBORS_MEASURE_INDEX_HPP_

#include <networkit/linkprediction/LinkPredictor.hpp>

namespace NetworKit {

/**
 * @ingroup linkprediction
 *
 * Implementation of the Neighbors Measure Index.
 * This index is also known as Friends Measure and simply returns
 * the number of connections between neighbors of the given nodes u and v.
 */
class NeighborsMeasureIndex : public LinkPredictor {
private:

  /**
   * Returns the number of connections between neighbors of @a u and @a v.
   * @param u First node
   * @param v Second node
   * @return the number of connections between neighbors of @a u and @a v
   */
  double runImpl(node u, node v) override;

public:
  using LinkPredictor::LinkPredictor;
  
};

} // namespace NetworKit

#endif // NETWORKIT_LINKPREDICTION_NEIGHBORS_MEASURE_INDEX_HPP_
