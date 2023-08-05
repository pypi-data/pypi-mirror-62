/*
 * VDegreeIndex.cpp
 *
 *  Created on: 01.04.2015
 *      Author: Kolja Esders (kolja.esders@student.kit.edu)
 */

#include <networkit/linkprediction/VDegreeIndex.hpp>

namespace NetworKit {

double VDegreeIndex::runImpl(node, node v) {
  return G->degree(v);
}

} // namespace NetworKit
