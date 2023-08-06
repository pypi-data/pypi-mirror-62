/*
 * MatrixMarketReader.h
 *
 *  Created on: 25.07.2014
 *      Author: dhoske
 */

#ifndef NETWORKIT_IO_MATRIX_MARKET_READER_HPP_
#define NETWORKIT_IO_MATRIX_MARKET_READER_HPP_

#include <networkit/io/MatrixReader.hpp>

namespace NetworKit {

/**
 * @ingroup io
 * Reader for the matrix market file format as described in
 * http://math.nist.gov/MatrixMarket/reports/MMformat.ps.
 *
 * Only allows real, symmetric matrices.
 */
class MatrixMarketReader: public MatrixReader {
public:

  MatrixMarketReader() = default;

  virtual CSRMatrix read(const std::string& path) override;

  /** Reads the matrix in @a in. */
  CSRMatrix read(std::istream& in);
};

}
#endif // NETWORKIT_IO_MATRIX_MARKET_READER_HPP_
