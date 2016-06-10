#include "FileWvIn.h"
#include "FileWvOut.h"
#include "Echo.h"
#include <stdlib.h> 
#include "JCRev.h"
#include <vector>
#include <string>
#include <boost/filesystem.hpp>
#include <boost/foreach.hpp>


using namespace stk;

std::vector<boost::filesystem::path> getAllOfDirectory(std::string pathToFolder){
	std::vector<boost::filesystem::path> paths;
	boost::filesystem::path targetDir( pathToFolder ); 
 
    boost::filesystem::directory_iterator it( targetDir ), eod;
 
    BOOST_FOREACH( boost::filesystem::path const &p, std::make_pair( it, eod ) ) { 
        if ( is_regular_file( p ) ){
            //std::string filename = p.string();
            
            paths.push_back(p);
        } 
    }
	return paths;
	
}

std::vector<std::string> splitString(std::string text, char where){
	std::stringstream test(text);
	std::string segment;
	std::vector<std::string> seglist;

	while(std::getline(test, segment, where)){
		seglist.push_back(segment);
	}
	
	return seglist;
	
}

std::string getPrefix(std::string path){
	std::vector<std::string> vec = splitString(path, '.');
	return vec.at(0);

}

void process(){
	std::vector<boost::filesystem::path> zeug = getAllOfDirectory("in");
	
	for (unsigned int i=0; i< zeug.size();i++){
		std::string fileName = zeug.at(i).filename().string();
		std::string outName = getPrefix(fileName) + "-r";
		std::cout << zeug.at(i).string() << std::endl;
		
		
	FileWvIn  input;
	FileWvOut output;

	

	try {
		// Load the input file
		input.openFile( zeug.at(i).string());
	}
	catch ( StkError & ) {
		exit(0);
	}

	// Set the global STK sample rate to the input file sample rate.
	Stk::setSampleRate( input.getFileRate() );

	// Reset the input file reader increment to 1.0
	input.setRate( 1.0 );
	
	

	try {
		// Define and open a 16-bit, one-channel WAV formatted output file
		output.openFile( "out/" + outName , 2, FileWrite::FILE_WAV, Stk::STK_SINT16 );
	}
	catch ( StkError & ) {
		input.closeFile();
		exit(0);
	}

	StkFloat f = 5;
	JCRev filter(f);
	//filter.setDelay(10000);
	//filter.setResonance( 1000.0, 0.999, true );  // set resonance to 1000 Hz, pole radius = 0.999, and normalize gain
	StkFrames frame( 1, 2 );                     // one frame of 2 channels

	int j;
	j = input.getSize();  // in sample frames
	while ( j-- >= 0 ) {

		try {
			StkFloat ding = input.tick();
			frame[0] = filter.tick( ding );
			frame[1] = filter.tick( ding );
			output.tick( frame );
		}
		catch ( StkError & ) {
			input.closeFile();
			output.closeFile();
			break;
    }
  }
	}
	
	

	
}

int main( int argc, char *argv[] ){
	
	process();
  

  return 0;
}
