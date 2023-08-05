/*
 * PivotMDS.h
 *
 *  Created on: Jul 7, 2016
 *      Author: Michael Wegner (michael.wegner@student.kit.edu)
 */

#ifndef NETWORKIT_VIZ_PIVOT_MDS_HPP_
#define NETWORKIT_VIZ_PIVOT_MDS_HPP_

#include <networkit/viz/GraphLayoutAlgorithm.hpp>

#include <networkit/algebraic/CSRMatrix.hpp>
#include <networkit/algebraic/Vector.hpp>

#include <networkit/graph/Graph.hpp>

namespace NetworKit {

/**
 * @ingroup viz
 *
 * Implementation of PivotMDS proposed by Brandes and Pich.
 */
class PivotMDS : public GraphLayoutAlgorithm<double> {
  public:
    /**
     * Constructs a PivotMDS object for the given @a graph. The algorithm should
     * embed the graph in @a dim dimensions using @a numPivots pivots.
     * @param graph
     * @param dim
     * @param numPivots
     */
    PivotMDS(const Graph &graph, count dim, count numPivots);

    /*
     * Default destructor
     */
    virtual ~PivotMDS() = default;

    /**
     * Runs the PivotMDS algorithm.
     */
    void run() override;

  private:
    count dim;
    count numPivots;

    /**
     *  Randomly picks the pivots for the algorithm
     */
    std::vector<node> computePivots();

    /**
     * Power method to compute the largest eigenvector and eigenvalue that are
     * stored in @a eigenvector and
     * @a eigenvalue.
     */
    void powerMethod(const CSRMatrix &mat, const count n, Vector &eigenvector,
                     double &eigenvalue);
};

} /* namespace NetworKit */

#endif // NETWORKIT_VIZ_PIVOT_MDS_HPP_
