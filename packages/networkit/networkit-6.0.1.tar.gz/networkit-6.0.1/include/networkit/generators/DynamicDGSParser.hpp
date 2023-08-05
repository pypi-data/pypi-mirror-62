/*
 * DynamicDGSParser.h
 *
 *  Created on: Jun 17, 2013
 *      Author: forigem
 */

#ifndef NETWORKIT_GENERATORS_DYNAMIC_DGS_PARSER_HPP_
#define NETWORKIT_GENERATORS_DYNAMIC_DGS_PARSER_HPP_

#include <fstream>
#include <vector>
#include <unordered_map>
#include <iterator>
#include <string>

#include <networkit/generators/DynamicGraphSource.hpp>
#include <networkit/auxiliary/StringTools.hpp>
#include <networkit/structures/Partition.hpp>


namespace NetworKit {

/**
 * @ingroup generators
 */
class DynamicDGSParser: public DynamicGraphSource {
public:
    DynamicDGSParser(std::string path);

    /**
     * The generator may expect the graph to be in a certain initial state. Call this method first.
     */
    virtual void initializeGraph();


    /**
     * Perform one generative step - as defined by the implementation.
     */
    virtual void generate();

    void evaluateClusterings(const std::string path, const Partition& clustering);


protected:
    bool graphInitialized;	//!< true if initializeGraph has been called and graph has been properly initialized
    std::unordered_map<std::string, node> nodeNames;
    std::vector<std::string> nodeDates;
    std::ifstream dgsFile;
    std::vector<std::vector<std::string>> nodeCategories;


};

} /* namespace NetworKit */
#endif // NETWORKIT_GENERATORS_DYNAMIC_DGS_PARSER_HPP_
